import network, socket, time as t, json, wifi_config, _thread, ntptime, machine, uos, gc, errno
from machine import Pin
from max6675 import MAX6675

log_lock = _thread.allocate_lock()
sensor_lock = _thread.allocate_lock()
TIMEZONE_OFFSET = 2 * 3600
sensor = MAX6675(spi_id=1, cs_pin=5, sck_pin=18, miso_pin=19, mosi_pin=5)
relay = Pin(33, Pin.OUT)
relay.value(0)

history = []
all_tasks = {}
current_profile = "A"
profiles = ["A", "B", "C", "D", "E", "F"]
sim_running = False
sim_abort = False
mode = 1
sim_status = {"temperature": 20.0, "current_task": 0, "hold_start": None, "last_log": 0, "error": None, "energy": 0.0, "total_energy": 0.0}
keep_running = True

def load_energy():
    global sim_status
    try:
        with open("energy.json", "r") as f:
            data = json.load(f)
            sim_status["total_energy"] = data.get("total", 0.0)
            if "connected_load" in data: wifi_config.CONNECTED_LOAD = data["connected_load"]
    except: pass

def save_energy():
    try:
        with open("energy.json", "w") as f:
            json.dump({"total": sim_status["total_energy"], "connected_load": wifi_config.CONNECTED_LOAD}, f)
    except: pass

load_energy()

def safe_read_temp():
    with sensor_lock:
        try:
            temp = sensor.read_temperature()
            if temp is not None and temp > 1020:
                return 9999.0 # Signal limit
            return temp
        except: return None

def write_log(*args):
    text = " ".join(str(arg) for arg in args)
    lt = t.localtime(t.time() + TIMEZONE_OFFSET)
    entry = "{:02}:{:02}:{:02} - {}\n".format(lt[3], lt[4], lt[5], text)
    print(text)
    try:
        with log_lock:
            with open("/log.txt", "a") as f: f.write(entry)
            if uos.stat("/log.txt")[6] > 10000:
                uos.remove("/log.txt")
                with open("/log.txt", "w") as f: f.write("Log reset\n")
    except: pass

def load_tasks():
    global all_tasks
    try:
        with open("tasks.json", "r") as f: data = json.load(f)
        for p in profiles:
            if p in data:
                if isinstance(data[p], list): all_tasks[p] = {"name": "Prog "+p, "tasks": data[p]}
                else: all_tasks[p] = data[p]
            else: all_tasks[p] = {"name": "Prog "+p, "tasks": []}
    except:
        for p in profiles: all_tasks[p] = {"name": "Prog "+p, "tasks": []}

def save_tasks():
    try:
        with open("tasks.json", "w") as f: json.dump(all_tasks, f)
    except: pass

def get_tasks(): return all_tasks[current_profile]["tasks"]

def log_history(temp, task=0):
    lt = t.localtime(t.time() + TIMEZONE_OFFSET)
    time_str = "{:02}:{:02}".format(lt[3], lt[4])
    history.append((time_str, round(temp, 1), int(task), 1 if sim_status["hold_start"] else 0))
    if len(history) > 500: history.pop(0)

PWM_WINDOW = 5.0
pid_i, pid_last_error = 0, 0

def control_temperature_pid(target):
    global pid_i, pid_last_error, sim_abort
    temp = safe_read_temp()
    if temp is None:
        write_log("❌ SENSOR FEHLER: Kein Thermoelement erkannt!")
        sim_status["error"] = "SENSOR FEHLER (Kabelbruch?)"
        sim_abort = True
        relay.value(0)
        return False
    
    # Fehler loeschen wenn Sensor wieder okay
    if sim_status["error"] == "SENSOR FEHLER (Kabelbruch?)":
        sim_status["error"] = None

    if temp >= 9000: # Limit reached (9999.0)
        write_log("🔥 ÜBERHITZUNG / SENSOR LIMIT!")
        sim_status["error"] = "SENSOR LIMIT > 1024°C"
        sim_abort = True
        relay.value(0)
        return False
    err = target - temp
    if abs(err) < 50: pid_i = max(-50, min(50, pid_i + err))
    der = err - pid_last_error
    pid_last_error = err
    out = (1.2 * err) + (0.02 * pid_i) + (5.0 * der)
    duty = max(0, min(PWM_WINDOW, out))
    
    # Energie erfassen: (An/3600h) * kW
    kwh = (duty / 3600.0) * (wifi_config.CONNECTED_LOAD / 1000.0)
    sim_status["energy"] += kwh
    sim_status["total_energy"] += kwh
    
    if duty > 0: relay.value(1); t.sleep(duty)
    if duty < PWM_WINDOW: relay.value(0); t.sleep(PWM_WINDOW - duty)
    sim_status["temperature"] = round(temp, 1)
    if t.time() - sim_status["last_log"] >= 60:
        log_history(temp, sim_status["current_task"])
        sim_status["last_log"] = t.time()
        write_log("P:{} T#{} IST:{:.1f} SOLL:{:.1f} L:{:.0f}% E:{:.2f}kWh".format(current_profile, sim_status["current_task"], temp, target, (duty/PWM_WINDOW)*100, sim_status["energy"]))
        save_energy()
    return True

def run_program(selected_task=None):
    global sim_running, sim_abort, mode, pid_i, pid_last_error
    if sim_running: return
    sim_running, sim_abort, mode = True, False, 3
    pid_i, pid_last_error = 0, 0
    sim_status["energy"] = 0.0 # Session Energie zuruecksetzen
    write_log("🚀 Start " + all_tasks[current_profile]["name"])
    try:
        tl = sorted(get_tasks(), key=lambda x: x["task_nr"])
        if selected_task: tl = [x for x in tl if x["task_nr"] >= selected_task]
        for task in tl:
            if sim_abort: break
            tgt, rate, hold = float(task["temperature"]), float(task.get("rate", 0)), float(task.get("hold_time", 0))
            sim_status["current_task"] = task["task_nr"]
            start_t = safe_read_temp() or 20.0
            dir = 1 if tgt > start_t else -1
            write_log("▶ Task {} -> {}°C ({}°/h)".format(task["task_nr"], tgt, rate))
            st_time = t.time()
            while not sim_abort:
                cur_tgt = tgt if rate <= 0 else start_t + (dir * (rate / 3600.0) * (t.time() - st_time))
                if (dir == 1 and cur_tgt >= tgt) or (dir == -1 and cur_tgt <= tgt): cur_tgt = tgt
                control_temperature_pid(cur_tgt)
                real = safe_read_temp()
                if real is not None:
                    if (rate > 0 and cur_tgt == tgt and abs(real-tgt) < 2) or (rate <= 0 and abs(real-tgt) < 1): break
            if hold > 0 and not sim_abort:
                write_log("⏱ Halten {}m".format(hold))
                sim_status["hold_start"] = t.time()
                while t.time() - sim_status["hold_start"] < (hold * 60) and not sim_abort: control_temperature_pid(tgt)
                sim_status["hold_start"] = None
            write_log("✅ Task {} beendet. Aktueller Verbrauch: {:.2f} kWh".format(task["task_nr"], sim_status["energy"]))
            save_energy()
        write_log("🏁 Ende. Gesamtverbrauch dieser Sitzung: {:.2f} kWh".format(sim_status["energy"]))
    except Exception as e: write_log("❗ Fehler: " + str(e))
    finally: relay.value(0); sim_running, mode = False, 1; save_energy()

def monitor_temperature():
    while keep_running:
        if not sim_running:
            temp = safe_read_temp()
            if temp is not None:
                sim_status["temperature"] = round(temp, 1)
                # Fehler loeschen wenn Sensor wieder okay
                if sim_status["error"] == "SENSOR FEHLER (Kabelbruch?)":
                    sim_status["error"] = None
                
                if t.time() - sim_status["last_log"] >= 120:
                    log_history(temp)
                    sim_status["last_log"] = t.time()
            else:
                sim_status["temperature"] = None # Signalisiert "--" im UI
                sim_status["error"] = "SENSOR FEHLER (Kabelbruch?)"
        t.sleep(10); gc.collect()
    write_log("Update Modus: Monitor gestoppt")

def response_json(cl, data):
    gc.collect()
    cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n" + json.dumps(data))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF); wlan.active(True); wlan.connect(wifi_config.SSID, wifi_config.PASSWORD)
    while not wlan.isconnected(): t.sleep(1)
    try: ntptime.settime()
    except: pass
    return wlan.ifconfig()[0]

ip = connect_wifi(); load_tasks(); _thread.start_new_thread(monitor_temperature, ())
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(("0.0.0.0", 80)); s.listen(5)
write_log("🌐 Server: http://" + ip)

while keep_running:
    try:
        gc.collect(); s.settimeout(1.0)
        try: cl, addr = s.accept(); cl.settimeout(5.0)
        except: continue
        # ... rest remains inside loop ...
        raw_req = cl.recv(1024).decode()
        if not raw_req: cl.close(); continue
        
        lines = raw_req.split("\r\n")
        method, path = lines[0].split(" ")[0:2]
        
        body = ""
        if "\r\n\r\n" in raw_req:
            body = raw_req.split("\r\n\r\n")[1]

        if method == "GET" and path == "/status":
            lt = t.localtime(t.time() + TIMEZONE_OFFSET)
            h_dur = "{:d}:{:02d}".format(int(t.time()-sim_status["hold_start"])//60, int(t.time()-sim_status["hold_start"])%60) if sim_status["hold_start"] else None
            response_json(cl, {
                "mode": mode, 
                "current_task": sim_status["current_task"], 
                "temperature": sim_status["temperature"] if sim_status["temperature"] < 9000 else 1024, 
                "running": sim_running, 
                "readable_time": "{:02}:{:02}".format(lt[3], lt[4]), 
                "hold_duration": h_dur, 
                "profile": current_profile, 
                "profile_name": all_tasks[current_profile]["name"], 
                "error": sim_status.get("error"),
                "energy": round(sim_status["energy"], 2),
                "total_energy": round(sim_status["total_energy"], 2),
                "connected_load": wifi_config.CONNECTED_LOAD
            })

        elif method == "GET" and path.startswith("/config/load/"):
            try:
                load = int(path.split("/")[-1])
                wifi_config.CONNECTED_LOAD = load
                save_energy()
                response_json(cl, {"ok": True})
            except Exception as e: response_json(cl, {"err": str(e)})
        
        elif method == "GET" and path == "/system/update":
            write_log("⚠️ UPDATE MODUS AKTIVIERT")
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Update-Modus aktiv</h1><p>Server gestoppt. REPL bereit fuer mpremote cp.</p></body></html>")
            cl.close()
            keep_running = False
            sim_abort = True
            break
        
        elif method == "POST" and path == "/tasks/add":
            try:
                # Falls Body im ersten Block fehlte, Rest nachladen (selten)
                if not body and "Content-Length" in raw_req:
                    body = cl.recv(512).decode()
                
                data = json.loads(body)
                t_nr = int(data["task_nr"])
                curr_tasks = all_tasks[current_profile]["tasks"]
                # Update oder Add
                new_list = [t for t in curr_tasks if t["task_nr"] != t_nr]
                new_list.append({"task_nr": t_nr, "temperature": float(data["temperature"]), "hold_time": float(data["hold_time"]), "rate": float(data.get("rate", 0))})
                all_tasks[current_profile]["tasks"] = sorted(new_list, key=lambda x: x["task_nr"])
                save_tasks()
                response_json(cl, {"ok": True})
            except Exception as e:
                response_json(cl, {"err": str(e)})

        elif method == "GET" and path.startswith("/tasks/delete/"):
            try:
                t_nr = int(path.split("/")[-1])
                all_tasks[current_profile]["tasks"] = [t for t in all_tasks[current_profile]["tasks"] if t["task_nr"] != t_nr]
                save_tasks()
                response_json(cl, {"ok": True})
            except Exception as e: response_json(cl, {"err": str(e)})
        elif method == "GET" and path == "/history":
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n[")
            for i in range(0, len(history), 10):
                if i > 0: cl.send(",")
                cl.send(",".join([json.dumps(e) for e in history[i:i+10]]))
            cl.send("]")
        elif method == "GET" and path == "/tasks": response_json(cl, get_tasks())
        elif method == "GET" and path.startswith("/profile/select/"):
            p = path.split("/")[3].upper()
            if p in profiles: current_profile = p; response_json(cl, {"ok": True})
        elif method == "GET" and path.startswith("/profile/rename/"):
            p, name = path.split("/")[3], path.split("/")[4].replace("%20", " ")
            if p in profiles: all_tasks[p]["name"] = name; save_tasks(); response_json(cl, {"ok": True})
        elif method == "GET" and path.startswith("/start/"):
            t_id = int(path.split("/")[2])
            _thread.start_new_thread(run_program, (t_id,)); response_json(cl, {"ok": True})
        elif method == "GET" and path == "/abort": sim_abort = True; response_json(cl, {"ok": True})
        elif method == "GET" and path == "/log/delete": uos.remove("/log.txt"); response_json(cl, {"ok": True})
        elif method == "GET" and path == "/log":
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n")
            with open("/log.txt", "r") as f:
                while True:
                    c = f.read(512)
                    if not c: break
                    cl.send(c)
        elif method == "GET" and path == "/":
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            with open("index.html", "r") as f:
                while True:
                    c = f.read(512)
                    if not c: break
                    cl.send(c)
        cl.close()
    except Exception as e: print("Err: ", e)
