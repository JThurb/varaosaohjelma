# r5
# Turpeinen Janne


import tkinter as tk
from tkinter import messagebox
from varaosaohjelma import (
    hae_varaosat,
    muokkaa,
    poista_varaosa,
    vie_csv,
    yhdista_tietokantaan,
    sulje_tietokanta,
    tallenna_varaosa,
    Varaosa,
    vero
)

# Tätä funktiota kutsutaan, kun halutaan lisätä uusi varaosa
def lisaa_varaosa():
    lisaa_ikkuna = tk.Toplevel()
    lisaa_ikkuna.title("Lisää varaosa")
    lisaa_ikkuna.geometry("300x300")

    # Varaosanumeron syöttökenttä
    tk.Label(lisaa_ikkuna, text="Varaosanumero:").pack()
    entry_numero = tk.Entry(lisaa_ikkuna, bg="#FFF5D4")
    entry_numero.pack()

    # Nimen syöttökenttä
    tk.Label(lisaa_ikkuna, text="Nimi:").pack()
    entry_nimi = tk.Entry(lisaa_ikkuna, bg="#FFF5D4")
    entry_nimi.pack()

    # Kappalemäärän syöttökenttä
    tk.Label(lisaa_ikkuna, text="Määrä:").pack()
    entry_maara = tk.Entry(lisaa_ikkuna, bg="#FFF5D4")
    entry_maara.pack()

    # Verollisen hinnan syöttökenttä
    tk.Label(lisaa_ikkuna, text="Verollinen hinta:").pack()
    entry_hinta = tk.Entry(lisaa_ikkuna, bg="#FFF5D4")
    entry_hinta.pack()

    # Sisäinen funktio, joka suoritetaan kun käyttäjä klikkaa "Tallenna"
    def tallenna():
        try:
            numero = entry_numero.get().strip().upper()  # .strip().upper()  poistetaan turhat välilyönnit ja muutetaan kaikki merkit isoiksi kirjaimiksi
            nimi = entry_nimi.get().strip().upper()
            maara = int(entry_maara.get())
            hinta = float(entry_hinta.get())

            # Luo uuden Varaosa-olion käyttäjän syötteistä
            varaosa = Varaosa(numero, nimi, maara, hinta, round(hinta / vero, 2)) 

            # Täällä kutsutaan funktiota tallenna_varaosa, joka on toisessa tiedostossa "varaosaohjelma"
            tallenna_varaosa(varaosa) 

            # Ponnahdusikkuna, joka kertoo onnistuiko varaosan lisäys vai ei
            messagebox.showinfo("Onnistui", f"Varaosa {numero} lisätty!")
            lisaa_ikkuna.destroy()
        except Exception as e:
            messagebox.showerror("Virhe", f"Tapahtui virhe: {e}")

    # Tallenna painike kutsuu funktiota tallenna()
    tk.Button(lisaa_ikkuna, text="Tallenna", bg="#fff5d4", command=tallenna).pack(pady=10)

# Funktio luo ikkunan johon tulostetaan kaikki varaosat tietokannasta
def selaa_varaosat():
    selaa_ikkuna = tk.Toplevel()
    selaa_ikkuna.title("Varaosaluettelo")
    selaa_ikkuna.geometry("600x400")

    # Luodaan scrollbar
    scrollbar = tk.Scrollbar(selaa_ikkuna)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    lista = tk.Listbox(selaa_ikkuna, yscrollcommand=scrollbar.set, width=100)
    lista.pack(padx=10, pady=10)

    for rivi in hae_varaosat():
        lista.insert(tk.END, rivi)

    scrollbar.config(command=lista.yview)

def poista_varaosa_gui():
    poista_ikkuna = tk.Toplevel()
    poista_ikkuna.title("Poista varaosa")
    poista_ikkuna.geometry("300x150")

    tk.Label(poista_ikkuna, text="Anna varaosanumero:").pack()
    entry = tk.Entry(poista_ikkuna, bg="#FFF5D4")
    entry.pack()

    def poista():
        numero = entry.get().strip().upper()
        poista_varaosa(numero)
        messagebox.showinfo("Valmis", f"Varaosa {numero} poistettu (jos löytyi).")
        poista_ikkuna.destroy()

    tk.Button(poista_ikkuna, text="Poista", bg="#FFF5D4", command=poista).pack(pady=10)

def muokkaa_varaosaa_gui():
    muokkaa_ikkuna = tk.Toplevel()
    muokkaa_ikkuna.title("Muokkaa varaosaa")
    muokkaa_ikkuna.geometry("300x300")

    tk.Label(muokkaa_ikkuna, text="Jätä tyjäksi jos haluat tallentaa vanhan tiedon").pack()
    tk.Label(muokkaa_ikkuna, text="Anna varaosanumero:").pack()
    entry_numero = tk.Entry(muokkaa_ikkuna, bg="#FFF5D4")
    entry_numero.pack()

    tk.Label(muokkaa_ikkuna, text="Uusi nimi:").pack()
    entry_nimi = tk.Entry(muokkaa_ikkuna, bg="#FFF5D4")
    entry_nimi.pack()

    tk.Label(muokkaa_ikkuna, text="Uusi määrä:").pack()
    entry_maara = tk.Entry(muokkaa_ikkuna, bg="#FFF5D4")
    entry_maara.pack()

    tk.Label(muokkaa_ikkuna, text="Uusi verollinen hinta:").pack()
    entry_hinta = tk.Entry(muokkaa_ikkuna, bg="#FFF5D4")
    entry_hinta.pack()

    def muokkaa_aloitus():
        numero = entry_numero.get().strip().upper()
        nimi = entry_nimi.get().strip().upper()
        maara = entry_maara.get().strip()
        hinta = entry_hinta.get().strip()

        # Tyhjät kentät säilyttävät vanhan arvon
        uusi_nimi = nimi if nimi else None
        uusi_maara = int(maara) if maara else None
        uusi_hinta = float(hinta) if hinta else None

        muokkaa(numero, uusi_nimi, uusi_maara, uusi_hinta)
        messagebox.showinfo("Valmis", f"Varaosa {numero} päivitetty (jos löytyi).")
        muokkaa_ikkuna.destroy()

    tk.Button(muokkaa_ikkuna, text="Muokkaa", bg="#FFF5D4", command=muokkaa_aloitus).pack(pady=10)

def vie_csv_gui():
    # Tämä funktio mahdollistaa varaosalistan tallentamisen csv tiedostona omalle koneelle. Tiedoston tallennuspaikan saa valita itse
    from tkinter import filedialog
    try:
        # kysytään mihin tallennetaan ja voidaan antaa oma nimi tiedostolle.
        polku = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Tallenna CSV-tiedosto"
        )
        if polku:
            vie_csv(polku) # Kutsutaan funktiota tiedostosta "varaosaohjelma"
            messagebox.showinfo("Onnistui", "CSV tiedoston luonti onnistui!")
    # Jos tiedoston luonti ei onnistu, virheilmoitus kaapataan ja näytetään käyttäjälle. Tarkempi viesti "{e}"    
    except Exception as e:
        messagebox.showerror("Virhe", f"CSV-tiedoston luonti epäonnistui:\n{e}")

def main_gui():
    yhdista_tietokantaan()  # Ohjelma alkaa sillä, että yhdistetään se SQL tietokantaan

    window = tk.Tk()
    window.title("Varaosien hallinta")
    window.geometry("450x450")

    otsikko = tk.Label(window, text="Varaosien hallintaohjelma", font=("Helvetica", 18), bg="#EBD2A7", height=3, width=25,)
    otsikko.pack(pady=20)

    tk.Button(window, text="Lisää varaosa", width=30, bg="#fff5d4", cursor="hand2", command=lisaa_varaosa).pack(pady=5)
    tk.Button(window, text="Selaa varaosia", width=30, bg="#FFF5D4", cursor="hand2", command=selaa_varaosat).pack(pady=5)
    tk.Button(window, text="Muokkaa varaosaa", width=30, bg="#FFF5D4", cursor="hand2", command=muokkaa_varaosaa_gui).pack(pady=5)
    tk.Button(window, text="Poista varaosa", width=30, bg="#FFF5D4", cursor="hand2", command=poista_varaosa_gui).pack(pady=5)
    tk.Button(window, text="Vie CSV-tiedostoon", width=30, bg="#FFF5D4", cursor="hand2", command=vie_csv_gui).pack(pady=5)
    tk.Button(window, text="Sulje", width=30, bg="#FFF5D4", cursor="hand2", command=lambda: (sulje_tietokanta(), window.destroy())).pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    main_gui()
