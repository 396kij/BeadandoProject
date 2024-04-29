import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date

class Szoba:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, ar=10000)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, ar=15000)

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaad(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                    foglalas = Foglalas(szoba, datum)
                    self.foglalasok.append(foglalas)
                    return foglalas
        return None

    def foglalas_lemondas(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            messagebox.showinfo("Lemondás", "Foglalás sikeresen törölve.")
        else:
            messagebox.showwarning("Lemondás", "A foglalás nem található.")

    def foglalasok_listazasa(self):
        if self.foglalasok:
            messagebox.showinfo("Foglalások listázása", "\n".join([f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}" for foglalas in self.foglalasok]))
        else:
            messagebox.showinfo("Foglalások listázása", "Nincsenek foglalások.")

class SzallodaGUI:
    def __init__(self, master):
        self.szalloda = Szalloda("Hidden leaf szálloda")
        self.szalloda.szoba_hozzaad(EgyagyasSzoba("101"))
        self.szalloda.szoba_hozzaad(EgyagyasSzoba("103"))
        self.szalloda.szoba_hozzaad(KetagyasSzoba("201"))
        self.szalloda.foglalas("101", "2024-05-30")
        self.szalloda.foglalas("103", "2024-05-19")
        self.szalloda.foglalas("201", "2024-06-02")
        self.szalloda.foglalas("201", "2024-07-22")
        self.szalloda.foglalas("101", "2024-09-12")


        self.master = master
        master.title("Szálloda Foglalás")

        self.label = tk.Label(master, text="Válasszon műveletet:")
        self.label.pack()

        self.button_foglalas = tk.Button(master, text="Foglalás", command=self.foglalas)
        self.button_foglalas.pack()

        self.button_lemondas = tk.Button(master, text="Lemondás", command=self.lemondas)
        self.button_lemondas.pack()

        self.button_listazas = tk.Button(master, text="Foglalások listázása", command=self.listazas)
        self.button_listazas.pack()

        self.button_quit = tk.Button(master, text="Kilépés", command=master.quit)
        self.button_quit.pack()

    def foglalas(self):
        top = tk.Toplevel()
        top.title("Foglalás")

        label_szoba = tk.Label(top, text="Szoba száma:")
        label_szoba.grid(row=0, column=0)

        entry_szoba = tk.Entry(top)
        entry_szoba.grid(row=0, column=1)

        label_datum = tk.Label(top, text="Dátum:")
        label_datum.grid(row=1, column=0)

        entry_datum = tk.Entry(top)
        entry_datum.grid(row=1, column=1)

        def foglalas_meghatarozas():
            szobaszam = entry_szoba.get()
            datum_str = entry_datum.get()
            try:
                datum = datetime.strptime(datum_str,
                                          '%Y-%m-%d')
                if datum.date() < date.today():
                    messagebox.showwarning("Foglalás", "A megadott dátum nem lehet a mai napnál korábbi.")
                    return
            except ValueError:
                messagebox.showwarning("Foglalás",
                                       "Érvénytelen dátumformátum. Kérlek, használj 'ÉÉÉÉ-HH-NN' formátumot.")
                return
            foglalas = self.szalloda.foglalas(szobaszam, datum)
            if foglalas:
                messagebox.showinfo("Foglalás", f"Foglalás készült a {foglalas.szoba.szobaszam} számú szobára {foglalas.datum} dátumra.")
            else:
                messagebox.showwarning("Foglalás", "Nincs ilyen szobaszám a szállodában.")

        button_foglalas = tk.Button(top, text="Foglalás", command=foglalas_meghatarozas)
        button_foglalas.grid(row=2, columnspan=2)

    def lemondas(self):
        top = tk.Toplevel()
        top.title("Lemondás")

        label_szoba = tk.Label(top, text="Szoba száma:")
        label_szoba.grid(row=0, column=0)

        entry_szoba = tk.Entry(top)
        entry_szoba.grid(row=0, column=1)

        label_datum = tk.Label(top, text="Dátum:")
        label_datum.grid(row=1, column=0)

        entry_datum = tk.Entry(top)
        entry_datum.grid(row=1, column=1)

        def lemondas_meghatarozas():
            szobaszam = entry_szoba.get()
            datum = entry_datum.get()
            foglalas = None
            for fogl in self.szalloda.foglalasok:
                if fogl.szoba.szobaszam == szobaszam and fogl.datum == datum:
                    foglalas = fogl
                    break
            if foglalas:
                self.szalloda.foglalas_lemondas(foglalas)
            else:
                messagebox.showwarning("Lemondás", "Nincs ilyen foglalás a megadott szobaszámmal és dátummal.")

        button_lemondas = tk.Button(top, text="Lemondás", command=lemondas_meghatarozas)
        button_lemondas.grid(row=2, columnspan=2)

    def listazas(self):
        self.szalloda.foglalasok_listazasa()

root = tk.Tk()
my_gui = SzallodaGUI(root)
root.mainloop()
