import json
import time
import math
import sys
import copy
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtCore import Qt, QTimer, QCoreApplication
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont, QPen, QCursor, QImage
from design_sample_1 import Ui_MainWindow

TIMER_DELAY = 0.25 #in Sekunden


class Frm_main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__(parent=None)   #Vererbungshirachie
        self.spielzustand = Spielzustand('spielkarte.txt', 'wellen_info.json')
        self.setupUi(self)  #Malt das Scoreboard
        
        #Timer, der alle 250ms alles neu zeichnen lässt
        self.timer = QTimer()
        self.timer.setInterval(int(TIMER_DELAY * 1000)) # setInterval benötigt Millisekunden
        self.timer.timeout.connect(self.animation)

        #Scoreboard Buttons (Signal/Slot)
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.turm1_button.clicked.connect(self.turm1_platzieren) 
        self.turm2_button.clicked.connect(self.turm2_platzieren)
        self.turm3_button.clicked.connect(self.turm3_platzieren)
        
        #Wird bei der Turmplatzierung verwendet
        self.tower = False       
        self.turm_beim_platzieren = None
        self.updateLabels()

    def updateLabels(self): #Updated die Labels des Scoreboards, um die aktuellen Attribute verwenden zu können
        self.geld_label.setText("Geld: " + str(self.spielzustand.geld))
        self.hp_label.setText("HP Stadt: " + str(self.spielzustand.spielkonfiguration.stadt_lebensenergie))
        self.runde_label.setText("Runde: " + str(1 + self.spielzustand.runde) + "/3")
        
        self.turm1_button.setText("RohButter" +
                                  "\nSCHADEN: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[0].schaden) + 
                                  "\nREICHWEITE: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[0].reichweite) + 
                                  "\nPREIS: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[0].preis) + 
                                  "\nFEUERRATE: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[0].feuerrate))
        
        self.turm2_button.setText("Minion" +
                                  "\nSCHADEN: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[1].schaden) + 
                                  "\nREICHWEITE: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[1].reichweite) + 
                                  "\nPREIS: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[1].preis) + 
                                  "\nFEUERRATE: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[1].feuerrate))
        
        self.turm3_button.setText("JoJo" +
                                  "\nSCHADEN: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[2].schaden) + 
                                  "\nREICHWEITE: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[2].reichweite) + 
                                  "\nPREIS: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[2].preis) + 
                                  "\nFEUERRATE: " + str(self.spielzustand.spielkonfiguration.alle_tuerme[2].feuerrate))
    
    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    #Türme werden aus der Liste kopiert, um die ursprünglichen Türme nicht nachgehend zu verändern
    def turm1_platzieren(self):
        spielkonfi = self.spielzustand.spielkonfiguration
        self.turm_beim_platzieren = copy.deepcopy(spielkonfi.alle_tuerme[0])

    def turm2_platzieren(self):
        spielkonfi = self.spielzustand.spielkonfiguration
        self.turm_beim_platzieren = copy.deepcopy(spielkonfi.alle_tuerme[1])

    def turm3_platzieren(self):
        spielkonfi = self.spielzustand.spielkonfiguration
        self.turm_beim_platzieren = copy.deepcopy(spielkonfi.alle_tuerme[2])
    
    #Updated beim Timeout das Gezeichnete, beim Ende Stopp des Programms
    def animation(self):
        game_over = self.spielzustand.next_timestep()
        self.update()
        if game_over:
            self.stop()  
        self.updateLabels()     

    def mousePressEvent(self, event):   #Trackt die Maus
        if event.button() == Qt.MouseButton.LeftButton:
            #Mausposition in Spielfeldkoordinaten
            maus_x = event.pos().x()
            maus_y = event.pos().y()
            spielfeld_x = int(maus_x // (720 / 8))
            spielfeld_y = int(maus_y // (720 / 8))

            if self.turm_beim_platzieren is not None:   #Turm ausgewählt?
                if self.ist_gueltige_platzierung(spielfeld_x, spielfeld_y) == True: #Feldplatzierung legal?
                    self.turm_beim_platzieren.position = (spielfeld_y, spielfeld_x) #Turmkoordianten 
                    self.spielzustand.spielkonfiguration.tuerme.append(self.turm_beim_platzieren)   #Turm ins Spielfeld
                    self.spielzustand.geld -= self.turm_beim_platzieren.preis   #Turmkosten werden abgezogen
                    self.setze_turm(self.turm_beim_platzieren, spielfeld_x, spielfeld_y)    #Setzt Turm auf die Map (schriftlich)
                    self.updateLabels()
                    self.turm_beim_platzieren = None  #Zurücksetzung des aktuellen Turms
        self.update()
        self.updateLabels()

    def ist_gueltige_platzierung(self, spielfeld_x, spielfeld_y):   #Legal, wenn Grün und keine Schulden
        if self.spielzustand.spielkonfiguration.spielfeld.spielkarte[spielfeld_y][spielfeld_x] == "#" and self.spielzustand.geld - self.turm_beim_platzieren.preis >= 0:
            return True
        return False

    def setze_turm(self, turm, y, x):   #Verändert das # zu dem Kürzel des jeweiligen Turms auf der Map
        if turm.name == "RohButter":
            self.spielzustand.spielkonfiguration.spielfeld.spielkarte[x][y] = "R"
        elif turm.name == "Minion":
            self.spielzustand.spielkonfiguration.spielfeld.spielkarte[x][y] = "M"
        else:
            self.spielzustand.spielkonfiguration.spielfeld.spielkarte[x][y] = "J"

    def paintEvent(self, event):    #Malt Spielkarte, Türme und Angreifer
        spielkarte = self.spielzustand.spielkonfiguration.spielfeld.spielkarte
        painter = QPainter(self)

        #Malt Spielkarte
        for y in range(len(spielkarte)):
            for x in range(len(spielkarte[y])):
                if spielkarte[y][x] == "S":
                    square_color = QColor(220,20,60)  #Rot
                    painter.setBrush(square_color)
                elif spielkarte[y][x] == "#":
                    square_color = QColor(50,205,50)  #Grün
                    painter.setBrush(square_color)
                elif spielkarte[y][x] == "E":
                    square_color = QColor(106,90,205)   #Blau
                    painter.setBrush(square_color)
                else:
                    square_color = QColor(85,85,85)     #Grau
                    painter.setBrush(QColor(200,200,200))

                painter.setPen(square_color)
                z = int(720/8)
                painter.drawRect(z*x,z*y,z,z)

                #Malt Turm
                if spielkarte[y][x] == "R":
                    square_color = QColor(50,205,50)
                    bild = QImage('RohButter.png')
                    vergroessertes_bild = bild.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    painter.drawImage(z*x, z*y, vergroessertes_bild)
                    self.update()
                elif spielkarte[y][x] == "M":
                    square_color = QColor(50,205,50)
                    bild = QImage('Minion.png')
                    vergroessertes_bild = bild.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    painter.drawImage(z*x, z*y, vergroessertes_bild)
                    self.update()
                elif spielkarte[y][x] == "J":
                    square_color = QColor(50,205,50)
                    bild = QImage('JoJo.png')
                    vergroessertes_bild = bild.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    painter.drawImage(z*x, z*y, vergroessertes_bild)
                    self.update()
        
        #Stoppt hier schonmal, wenn alle Runden überlebt wurden
        if self.spielzustand.runde >= len(self.spielzustand.spielkonfiguration.runden):
            quit()
        
        #Malt Angreifer
        a_painter = QPainter(self)
        n = 0
        while True:
            liste_angreifer = self.spielzustand.spielkonfiguration.runden[self.spielzustand.runde]
            if n == len(liste_angreifer):
                break
            angreifer = liste_angreifer[n]
            position = angreifer.position
            if position == (0,0):
                n += 1
                continue
            if angreifer.name == "Stein/r":
                square_color = QColor(255,0,0)
            elif angreifer.name == "Stein/gr":
                square_color = QColor(0,255,0)
            else:
                square_color = QColor(0,0,255)
            n += 1

            a_painter.setBrush(square_color)
            a_painter.setPen(square_color)
            z = int(720/8)
            a_painter.drawRect(z * angreifer.position[1] + 19, z * angreifer.position[0] + 19, 50, 50)
            a_pos_x = z * angreifer.position[1] + 35
            a_pos_y = z * angreifer.position[0] + 85    
            a_painter.drawText(a_pos_x, a_pos_y, str(angreifer.lebensenergie))

class Spielzustand:
    def __init__(self, spielkarte, wellen_info):    #Konstruktor ruft Spielkonfi auf und initialisiert die 3 Hauptattribute des Programms
        self.spielkonfiguration = SpielKonfiguration(spielkarte, wellen_info)
        self.geld = 300
        self.runde = 0
        self.time = 0
    
    def next_timestep(self):    #Führt den 250ms Sprung des Programms durch
        self.time += TIMER_DELAY

        #Platziert die Angreifer mit Delay
        liste_angreifer = self.spielkonfiguration.runden[self.runde]
        belegte_positionen = set()
        for angreifer in liste_angreifer:
            angreifer_x, angreifer_y = angreifer.position
            if (angreifer_x, angreifer_y) in belegte_positionen:
                #angreifer.time += TIMER_DELAY
                self.next_timestep
            else:
                if angreifer.is_active == False and angreifer_x == 3 and angreifer_y == 0:
                    angreifer.is_active = True
                else:
                    angreifer.time += TIMER_DELAY
                belegte_positionen.add((angreifer_x, angreifer_y))

        if len(self.spielkonfiguration.runden[self.runde]) <= 0:    #Wenn kein Angreifer mehr da ist, runden_update()
            self.runden_update()
            for turm in self.spielkonfiguration.tuerme:     #Türme haben bei Rundenwechsel erst wieder geschossen, als ein Neuer plaziert wurde
                turm.zeit_letzer_schuss = -1
            if self.runde == len(self.spielkonfiguration.runden):   #Aktuelle Runde = letzte Runde?
                return True
            return False
        game_over = self.position_angreifer() #Angreifer aktualisieren
        self.turm_in_range()    #Türme überprüfen
        return game_over    #Returnt True, wenn Spiel vorbei

    def position_angreifer(self):
        if self.runde == len(self.spielkonfiguration.runden):   #Alle Runden überlebt == True
            return True
        
        #Bewegt die Angreifer zur jeweiligen Zeit
        liste_angreifer = self.spielkonfiguration.runden[self.runde]
        for angreifer in liste_angreifer:
            geschwindigkeit = angreifer.geschwindigkeit
            strecke = int(geschwindigkeit * angreifer.time)
            if strecke >= len(self.spielkonfiguration.spielfeld.angreifer_weg): #Trifft Stadt, macht Schaden
                self.stadt_getroffen()
                self.spielkonfiguration.runden[self.runde].remove(angreifer)
                continue
            angreifer.position = self.spielkonfiguration.spielfeld.angreifer_weg[strecke]

    def turm_in_range(self):    #Wenn der Angreifer in die Range des Turms kommmt, schießt er, wenn er kann
        liste_tuerme = self.spielkonfiguration.tuerme
        liste_angreifer = self.spielkonfiguration.runden[self.runde]
        for turm in liste_tuerme:
            for angreifer in liste_angreifer:
                if self.distanz(turm, angreifer):
                    if self.turm_kann_schiessen(turm) == True:
                        self.turm_schuss(turm, angreifer)

    def turm_schuss(self, turm, angreifer):
        angreifer.lebensenergie -= turm.schaden
        if angreifer.lebensenergie > 0:
            return None
        else:
            self.geld_update(angreifer)
            if len(self.spielkonfiguration.runden[self.runde]) <= 0:    #Wenn alle Gegner tot sind, nächste Runde
                self.runden_update()
        self.spielkonfiguration.runden[self.runde].remove(angreifer)    #Tote Angreifer werden aus der Liste entfernt

    def turm_kann_schiessen(self, turm):
        if (1/turm.feuerrate) <= (self.time - turm.zeit_letzer_schuss): #Berechnet Zeitspanne seit letztem Schuss
            turm.zeit_letzer_schuss = self.time #Aktualisiert Attribut
            return True
        return False

    def distanz(self, turm, angreifer):
        distanz = math.sqrt(((angreifer.position[0] - turm.position[0]) ** 2) + ((angreifer.position[1] - turm.position[1]) ** 2)) #Berechnet Distanz mit dem euklidischen Abstand
        if distanz <= turm.reichweite:  #Wenn Distanz in Reichweite, Schuss
            return True
        return False

    def stadt_getroffen(self):
        self.spielkonfiguration.stadt_lebensenergie -= 10   #Verliert bei Treffer 10 Lp
        if self.spielkonfiguration.stadt_lebensenergie <= 0:    #Niederlage, wenn Stadt keine Lp mehr hat
            quit()

    def geld_update(self, angreifer):   #Gewinn des Geldwertes eines Gegners
        self.geld += angreifer.spielgeld_wert

    def runden_update(self):    #Erhöt Runde
        self.runde += 1
        self.time = 0

class SpielKonfiguration:
    def __init__(self, spielkarte, wellen_info):    #Konstruktor ruft Spielfeld auf und lädt durch die Funktionen alle wichtigen Infos ins Programm
        self.spielfeld = Spielfeld(spielkarte)
        self.wellen_info = wellen_info
        self.tuerme = []
        self.alle_tuerme = self.lade_tuerme()
        self.angreifer = self.lade_angreifer()
        self.runden = self.lade_runden()
        self.stadt_lebensenergie = self.lade_stadt()

    def lade_angreifer(self):   #Liest die verschiedenen Angreifer mit ihren Eigenschaften aus und erstellt daraus eine Liste
        with open(self.wellen_info, 'r') as file:
            data = json.load(file)
            if "angreifer" in data:
                angreifer = data["angreifer"]
                angreifer_info = []
                for attackers in angreifer:
                    name = attackers["name"]
                    geschwindigkeit = attackers["geschwindigkeit"]
                    spielgeld_wert = attackers["spielgeld_wert"]
                    lp = attackers["lp"]
                    aktueller_angreifer = Angreifer(name, geschwindigkeit, spielgeld_wert, lp)
                    angreifer_info.append(aktueller_angreifer)
                return angreifer_info
            else:
                return None
    
    def lade_tuerme(self):  #Liest die verschiedenen Türme mit ihren Eigenschaften aus und erstellt daraus eine Liste
        with open(self.wellen_info, 'r') as file:
            data = json.load(file)
            if "tuerme" in data:
                tuerme = data["tuerme"]
                tuerme_info = []
                for turm in tuerme:
                    name = turm["name"]
                    schaden = turm["schaden"]
                    reichweite = turm["reichweite"]
                    feuerrate = turm["feuerrate"]
                    preis = turm["preis"]
                    aktueller_turm = Turm(name, reichweite, feuerrate, preis, schaden)
                    tuerme_info.append(aktueller_turm)
                return tuerme_info
            else:
                return None

    def lade_runden(self):  #Liest die verschiedenen Runden mit der Anzahl der Angreifer aus und erstellt daraus eine Liste
        with open(self.wellen_info, 'r') as file:
                data = json.load(file)
                if "wellen" in data:
                    runden = data["wellen"]
                    runden_info = []
                    for n in runden:
                        runden_info.append(runden[n])
        #Für jede Runde Angreiferzahl von jedem Angreifer auslesen und jeden Angreifer als Listenelement mit Angreifer Objekten
                    liste_angreifer_gesamt = []
                    for n in range(len(runden_info)):
                        liste_angreifer_runde = []
                        for j in range(len(runden_info[n])):
                            for key,value in runden_info[n][j].items():
                                angreifer = key
                                anzahl = value
                                for geladener_angreifer in self.angreifer:
                                    if geladener_angreifer.name == angreifer:
                                        for i in range(anzahl):
                                            liste_angreifer_runde.append(copy.deepcopy(geladener_angreifer))
                        liste_angreifer_gesamt.append(liste_angreifer_runde)
                    return liste_angreifer_gesamt
                else:
                    return None

    def lade_stadt(self):   #Lädt die Lp der Stadt und gibt sie als Dictionary aus
        with open(self.wellen_info, 'r') as file:
            data = json.load(file)
            stadt_info = []
            if "stadt" in data:
                stadt_info = data['stadt']
                lp = stadt_info["lp"]
                return lp
            else:
                return None

class Spielfeld:
    
    def __init__(self, dateiname):  #Nimmt Spielfelddatei entgegen und nutzt die Funktionen
        self.dateiname = dateiname
        self.spielkarte = self.lade_karte()
        self.start = self.finde_startpunkt()
        self.angreifer_weg = self.finde_weg_von_start()

    def lade_karte(self):   #Lädt die Karte mithilfe der Spielfelddatei und erstellt daraus eine Spielfeldmatrix
     with open(self.dateiname, 'r') as datei:
            inhalt = list(line.strip() for line in datei)
            for n in range(len(inhalt)):
                inhalt[n] = list(inhalt[n])
            return inhalt

    def finde_startpunkt(self): #Findet den Startpunkt S des Spielfelds
        for x in range(len(self.spielkarte)):
            for y in range(len(self.spielkarte[x])):
                if self.spielkarte[x][y] == "S":
                    return (x,y)
        return None

    def finde_weg_von_start(self):  #Findet den Weg vom Start S bis zum Endpunkt E des Spielfelds und speichert diesen als Liste von Tupeln
        (x,y) = self.start
        weg = []
        while True:
            aktuelle_kachel = self.spielkarte[x][y]
            if aktuelle_kachel == 'E':
                weg.append((x,y))
                break
            weg.append((x,y))
            if aktuelle_kachel == '1':
                x -= 1
            elif aktuelle_kachel == '2' or aktuelle_kachel == 'S':
                y += 1
            elif aktuelle_kachel == '3':
                x += 1
            elif aktuelle_kachel == '4':
                y -= 1
        return weg

class Angreifer:
    def __init__(self, name, geschwindigkeit, spielgeld_wert, lebensenergie):
        self.name = name
        self.geschwindigkeit = geschwindigkeit
        self.spielgeld_wert = spielgeld_wert
        self.lebensenergie = lebensenergie
        self.position = (-1,-1)
        self.time = 0
        self.is_active = False

class Turm:
    def __init__(self, name, reichweite, feuerrate, preis, schaden):
        self.name = name
        self.reichweite = reichweite
        self.feuerrate = feuerrate
        self.preis = preis
        self.schaden = schaden
        self.zeit_letzer_schuss = -1
        self.position = (-1000, -1000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    frm_main = Frm_main()
    frm_main.show()
    app.exec()
