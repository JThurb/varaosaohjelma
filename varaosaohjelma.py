# r5
# Turpeinen Janne


import sqlite3
import csv

# ALV veron määrä. Globaali muuttuja jota voidaan käyttää ohjelmassa kaikkialla. 
global vero
vero = 1.255 # 25.5 %

# Luodaan luokka Varaosa
class Varaosa:
    def __init__(self, varaosanumero, nimi, maara, verollinen_hinta, veroton_hinta):
        self.varaosanumero = varaosanumero
        self.nimi = nimi
        self.maara = maara
        self.verollinen_hinta = round(verollinen_hinta, 2)
        self.veroton_hinta = round(verollinen_hinta / vero, 2)   # Rivin viimeinen numero "2" kertoo desimaalien luvun round() metodissa
    
    # Tämä on metodi varaosan tulostukseen
    def __str__(self):
        return f"{self.varaosanumero}: {self.nimi}: {self.maara} kpl, Hinta: {self.verollinen_hinta} €, ({self.veroton_hinta} ALV 0 %)"

# Yhdistä tietokantaan (luo uusi tietokanta, jos sitä ei ole olemassa)
connect = sqlite3.connect("varaosa_data.db")
cursor = connect.cursor()

# Luo taulun tietokantaan, jos sitä ei ole olemassa
cursor.execute('''CREATE TABLE IF NOT EXISTS varaosa_data (
          varaosanumero TEXT NOT NULL,
          nimi TEXT NOT NULL,
          maara INTEGER NOT NULL,
          verollinen_hinta REAL NOT NULL,
          veroton_hinta REAL NOT NULL
          )''')

# Tallenna uusi varaosa
def tallenna_varaosa(varaosa):
    cursor.execute("INSERT INTO varaosa_data (varaosanumero, nimi, maara, verollinen_hinta, veroton_hinta) VALUES (?, ?, ?, ?, ?)", 
              (varaosa.varaosanumero, varaosa.nimi, varaosa.maara, varaosa.verollinen_hinta, varaosa.veroton_hinta))
    connect.commit()

# Hae kaikki varaosat
def hae_varaosat():
    cursor.execute("SELECT * FROM varaosa_data")
    varaosat = cursor.fetchall()
    tulokset = []
    for varaosa in varaosat:
        varaosa_olio = Varaosa(varaosa[0], varaosa[1], varaosa[2], varaosa[3], varaosa[4])
        tulokset.append(str(varaosa_olio))
    return tulokset

# Muokataan olemassa olevaa varaosaa
def muokkaa(varaosanumero, uusi_nimi=None, uusi_maara=None, uusi_verollinen_hinta=None):
    cursor.execute("SELECT * FROM varaosa_data WHERE varaosanumero = ?", (varaosanumero,))
    varaosa = cursor.fetchone()

    if varaosa:
        # Tässä muokataan varaosan tietoja. Jos tekstikenttä jätetään tyhjäksi, arvoksi tallennetaan olemassa oleva, eli vanha arvo
        uusi_nimi = uusi_nimi or varaosa[1]
        uusi_maara = uusi_maara if uusi_maara is not None else varaosa[2]
        uusi_verollinen_hinta = uusi_verollinen_hinta if uusi_verollinen_hinta is not None else varaosa[3]
        uusi_veroton_hinta = round(float(uusi_verollinen_hinta)/vero, 2)

        # Päivitetään tietokantaan uudet tiedot
        cursor.execute('''UPDATE varaosa_data 
                     SET nimi = ?, maara = ?, verollinen_hinta = ?, veroton_hinta = ?
                     WHERE varaosanumero = ?''',
                  (uusi_nimi, uusi_maara, uusi_verollinen_hinta, uusi_veroton_hinta, varaosanumero))
        connect.commit()

# funktio poistaa varaosan tietokannasta, jos se sieltä löytyi
def poista_varaosa():
    varaosanumero = input("Anna poistettavan varaosan numero: ").strip().upper()
    cursor.execute("DELETE FROM varaosa_data WHERE varaosanumero = ?", (varaosanumero,))
    connect.commit()
    print(f"Varaosa {varaosanumero} poistettu (jos löytyi).")

def vie_csv(tiedostonimi):
    cursor.execute("SELECT * FROM varaosa_data")
    rivit = cursor.fetchall()

    with open(tiedostonimi, mode="w", newline='', encoding='utf-8') as tiedosto:
        kirjoittaja = csv.writer(tiedosto)
        # Otsikkorivi
        kirjoittaja.writerow(["varaosanumero", "nimi", "maara", "verollinen_hinta", "veroton_hinta"])
        # Data
        for rivi in rivit:
            kirjoittaja.writerow(rivi)
    print(f"Tiedot tallennettu tiedostoon {tiedostonimi}")

connect = None
cursor = None

def yhdista_tietokantaan():
    # Tämä yhdistää ohjelman SQL tietokantaan. Kun main_gui() käynnistetään, tätä funkiota kutsutaan ensimmäisenä
    global connect, cursor                          # Luodaan muuttujista connect ja cursor globaaleja muuttujia, eli niitä voidaan käyttää ohjelmassa muuallakin
    connect = sqlite3.connect("varaosa_data.db")    # yhdistetään sql tietokanta
    cursor = connect.cursor()                       # Cursor on olio joka mahdollistaa kyselyiden suorittamisen tietokannan sisällä
    cursor.execute('''CREATE TABLE IF NOT EXISTS varaosa_data (
        varaosanumero TEXT NOT NULL,
        nimi TEXT NOT NULL,
        maara INTEGER NOT NULL,
        verollinen_hinta REAL NOT NULL,
        veroton_hinta REAL NOT NULL
    )''')
    connect.commit()

def sulje_tietokanta():
    global connect
    if connect:
        connect.close()
