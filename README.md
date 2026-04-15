# 🏺 Brennofensteuerung

👉 Temp 0-1000C, ep32, Max6675, Micropython, WIFI

Eine leistungsstarke, MicroPython-basierte Steuerung für private Brennöfen und Experimentalsysteme mit intelligenter PID-Regelung, flexibler Profilsteuerung und modernem Web-Interface.

👉 **Entwickelt für Maker, Hobby-Keramiker und DIY-Projekte**, bei denen Temperaturprofile exakt eingehalten werden sollen.

<p>
  <img src="bilder/webseite_temp_verlauf.png?v=99" style="width:250px;">
  <img src="bilder/temp_verlauf_200c.png?v=99" style="width:250px;">
</p>

## 🚀 Warum dieses Projekt?

Dieses System bietet Hobby-Anwendern eine smarte, flexible und erweiterbare Lösung für private Projekte:

* 🎯 **Exakte Temperaturführung** dank hochpräzisem PID-Regler.
* 🔄 **Komplexe Brennkurven** voll automatisierbar (Ramp → Hold → Cooldown).
* 🌐 **Steuerung per Browser** – volle Kontrolle von jedem Endgerät, kein extra Display nötig.
* 📊 **Volle Transparenz** durch Live-Daten-Visualisierung **Web-Interface** am PC oder Smartphone & detailliertes Logging.

---

# 🔥 Keramikbrennen & erweiterte Ofennutzung im Hobbybereich

## 1. Grundlagen: Steuerung eines Brennofens

Ein moderner (elektrischer) Brennofen lässt sich programmieren über:

* **Aufheizrate (°C/h)** → beeinflusst Spannungen im Material  
* **Haltezeit (Soak)** → ermöglicht vollständige chemische Prozesse  
* **Abkühlkurve** → entscheidend für Struktur und Haltbarkeit  

👉 Wichtig: Jedes Material benötigt eine eigene Brennkurve.

---

## 2. Keramik: Schrühbrand vs. Glattbrand

### 🔹 Schrühbrand (Biscuit firing)

* Temperatur: **850–950 °C**
* Ziel: Entfernen von Wasser & organischen Stoffen  

Typische Kurve:

* 0–200 °C: sehr langsam (50–80 °C/h)
* 200–600 °C: moderat
* 600–900 °C: schneller
* kurze Haltezeit

---

### 🔹 Glattbrand (Glasurbrand)

* Temperatur: **1000–1300 °C** (je nach Ton/Glasur)
* Glasur schmilzt und verbindet sich mit dem Scherben  

Wichtig:

* gleichmäßige Temperaturverteilung  
* Haltezeit bei Endtemperatur (10–30 min)  
* kontrolliertes Abkühlen  

---

## 3. Glasieren & Glas schmelzen

### Keramikglasuren

* Silikatbasierte Materialien
* schmelzen zu einer glasartigen Oberfläche  
* benötigen exakte Endtemperatur  

---

### Glasbearbeitung

**Fusing (Verschmelzen):**

* 750–850 °C  

**Slumping (Absenken in Form):**

* 600–700 °C  

⚠️ Wichtig:

* langsames Abkühlen (Annealing bei ~500 °C)
* verhindert Spannungsrisse  

---

## 4. Erweiterte Nutzung: Metall & Formen

### 🔨 Messerschmieden (Härten)

**Austenitisieren:**

* 750–1100 °C (je nach Stahl)

**Probleme:**

* Oxidation/Zunder ohne Schutzatmosphäre  

**Lösungen:**

* Edelstahlfolie (Wrap)
* Schutzgas (wenn verfügbar)

**Anlassen:**

* 150–300 °C → reduziert Sprödigkeit  

---

### 🧱 Ausbrennen von Gießformen (Lost Wax)

Ablauf:

1. Wachsmodell in Gips einbetten  
2. Ofenprogramm:
   * 100–200 °C → Wachs schmilzt  
   * 300–500 °C → Rückstände verbrennen  
   * 600–750 °C → Form stabilisieren  

👉 Wichtig:

* gute Belüftung  
* langsames Aufheizen  

---

## 5. Weitere Anwendungen

* **Glas schmelzen:** bis ~900–1100 °C  
* **Emaille:** 750–850 °C  
* **Porzellan:** bis 1400 °C (nur Hochtemperaturofen)

---

## 6. Sicherheits- & Praxisregeln

* ❗ feuchte Keramik nie schnell erhitzen  
* ❗ Dämpfe vermeiden → gut lüften  
* ❗ Ofen nicht für Lebensmittel verwenden  
* ❗ Thermoelement regelmäßig prüfen  
* ❗ Brennplatten sauber halten  

---

## 🧠 Fazit

Ein Brennofen im Hobbybereich ist vielseitig einsetzbar:

* Keramik (Schrüh- & Glattbrand)  
* Glasuren & Glasbearbeitung  
* Metallhärten (eingeschränkt)  
* Gießformen ausbrennen  
* Materialexperimente  

👉 Entscheidend ist das Verständnis von Temperaturverläufen und Materialreaktionen.

## ⚠️ LEBENSWICHTIGER SICHERHEITSHINWEIS

**Eine Brennofensteuerung muss immer über eine zweite, autarke Übertemperaturabschaltung verfügen.**

Dieses Projekt ist eine reine Software-Steuerung auf Basis eines Mikrocontrollers. Elektronik kann versagen (z.B. hängendes Relais, Software-Hänger). Betreiben Sie einen Ofen **niemals** ohne einen unabhängigen, mechanischen Sicherheitstemperaturbegrenzer (STB), der die Stromzufuhr im Fehlerfall physisch trennt!

---

## ⚡ Key Features

### 🧠 Intelligente PID-Regelung

* **Präzision:** Verhindert Überschwingen und schützt empfindliches Material.
* **Sanftanlauf:** Kontrolliertes Anfahren für materialschonende Aufheizphasen.
* **Stabilität:** Sicherer Betrieb auch bei trägen Hobby-Öfen.

### 📊 Energie-Erfassung & Kostenkontrolle (Neu!)

Behalten Sie den Stromverbrauch Ihres Ofens immer im Blick:

* **Echtzeit-Verbrauch:** Anzeige des aktuellen Verbrauchs (kWh) der laufenden Sitzung im Web-Interface.
* **Gesamtverbrauch:** Speicherung des kumulierten Verbrauchs über alle Brände hinweg (restitent gegen Neustarts).
* **Anpassbar:** Die Anschlussleistung des Ofens (z.B. 3kW) kann direkt über die Webseite konfiguriert werden, um präzise Berechnungen für verschiedene Ofenmodelle zu ermöglichen.
* **Protokollierung:** Automatischer Eintrag des Verbrauchs in das Logfile bei jedem Task-Wechsel und am Programmende.

### 🔄 Flexible Task- & Profilsteuerung

Das Herzstück für perfekte Ergebnisse im Hobby-Keller:

* 🔥 **Ramp-Up:** Frei definierbare Aufheizgeschwindigkeit in °C/h.
* ⏱️ **Hold-Time:** Exakte Haltezeiten für chemische oder physikalische Prozesse.
* ❄️ **Cooldown:** Kontrolliertes Abkühlen zur Vermeidung von Spannungsrissen.

**Highlights:**

* 5 speicherbare Profile (A–F) mit unbegrenzten Task-Listen.
* Wiederverwendbare Prozessabläufe für reproduzierbare Ergebnisse.
* Ideal für Keramik, Glas-Fusing, Metallhärtung und private Experimente.

### 🌐 Modernes Web-Interface (SPA)

Keine App-Installation notwendig – läuft direkt im Browser auf PC, Tablet oder Smartphone.

* **Echtzeit-Dashboard:** Live-Temperaturkurve mit Chart.js Integration.
* **Responsive Design:** Optimiert für alle Bildschirmgrößen.
* **Interaktiv:** Profile bearbeiten, Tasks hinzufügen und Prozesse in Echtzeit starten/stoppen.

---

## 🛡️ Sicherheit & Zuverlässigkeit

* ❗ **Not-Halt:** Sofortiger Abbruch und Zwangsabschaltung des Relais jederzeit möglich.
* 🔥 **Sensor-Limit-Abschaltung:** Der MAX6675 ist auf 1024 °C begrenzt. Das System schaltet bei Erreichen von **1020 °C** automatisch das Relais ab, bricht das Programm ab und gibt eine Warnmeldung aus.
* 🔌 **Sensor-Wächter:** Erkennt Thermoelement-Ausfälle (Kabelbruch) sofort über das MAX6675-Protokoll.
* ⚠️ **Fail-Safe:** Automatische Abschaltung bei unplausiblen Messwerten oder Verbindungsverlust zum Sensor.

---

## 🛠️ Technische Details

<p>
  <img src="bilder/hardware_aufbau.jpeg?v=99" style="width:250px;">
</p>

### Sensorik: MAX6675 & K-Typ Thermoelement

* **Thermoelement (K-Typ):** Misst physikalisch bis ca. 1300 °C.
* **Controller (MAX6675):** Funktioniert ausschließlich mit K-Typ Thermoelementen und begrenzt den Messbereich elektronisch auf **maximal 1024 °C** (mit 12-Bit Auflösung in 0,25 °C Schritten).
* **Sicherheits-Stopp:** Automatische Abschaltung bei > 1020 °C zum Schutz vor unkontrolliertem Heizen außerhalb des Messbereichs.
* **Kaltstellenkompensation:** Integriert für höchste Genauigkeit.
* **Implementierung:** Direkte SPI-Auslesung mit Bit-Masking zur Fehlererkennung (Bit D2 Check).

### PID-Algorithmus

Die Regelung nutzt ein 4-Sekunden PWM-Fenster.

* **P (0.2):** Aggressivität der Reaktion auf Abweichungen.
* **I (-1.02):** Eliminiert stationäre Regelabweichungen (begrenzt auf +/- 50 gegen Wind-up).
* **D (4.0):** Dämpft die Annäherung an den Zielwert zur Vermeidung von Überschwingen.
* **Formel:** `Stellgröße = (P * Error) + (I * Integral) + (D * Derivativ)`

---

## 🧩 Typische Anwendungsfälle

* 🏺 **Keramikbrennen:** Präzise Steuerung von Schrüh- und Glatbrand im Hobbybereich.
* 🔬 **Private Experimente:** Laborähnliche Bedingungen für Werkstoffprüfungen zu Hause.
* 🛠️ **DIY-Ofensteuerungen:** Upgrade für alte Analog-Öfen.

---

## ⚠️ Wichtiger Hinweis (Disclaimer)

**Nutzung auf eigene Gefahr:**
Dieses System ist ein **reines Hobbyprojekt** für den privaten Gebrauch. Es ist ausdrücklich **nicht** für industrielle Anwendungen zertifiziert. Die Nutzung erfolgt auf eigene Gefahr. Bei der Steuerung von Heizelementen besteht akute Brandgefahr. Sorgen Sie zwingend für eine zusätzliche, unabhängige thermische Absicherung und lassen Sie das System niemals unbeaufsichtigt in Betrieb.

---

## 📦 Installation & Setup

0. WLAN in `wifi_config.py` eintragen.
1. Dateien auf den ESP32 flashen (z.B. mit Thonny).
2. Browser öffnen und die IP des ESP32 aufrufen.
3. **Updates im laufenden Betrieb:**
    * Klicken Sie im Web-Interface auf **Update**.
    * Bestätigen Sie die Sicherheitsabfrage.
    * Der ESP32 beendet alle Threads und kehrt zum REPL zurück.
    * Nun können Sie bequem mit `mpremote cp main.py :` neue Dateien übertragen, ohne den Controller vorher manuell löschen zu müssen.
    * Nach dem Update ist ein manueller Reset (Hardware-Taste oder `mpremote soft-reset`) erforderlich.
4. Viel Erfolg beim ersten Brand in Brennofen!
