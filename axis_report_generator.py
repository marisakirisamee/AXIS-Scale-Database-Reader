import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import enums
from tkinter import filedialog
import os
import shutil

CSV_PATH = None


APP_DIR = os.path.join(
    os.path.dirname(__file__),
    "config"
)

os.makedirs(APP_DIR, exist_ok=True)

KLUCZ_PATH = os.path.join(
    APP_DIR,
    "klucz_najemców.csv"
)

def wybierz_klucz():

    plik = filedialog.askopenfilename(
        title="Wybierz klucz najemców",
        filetypes=[("CSV", "*.csv")]
    )

    if not plik:
        return

    shutil.copy2(
        plik,
        KLUCZ_PATH
    )

    lbl_klucz.config(
        text="✓ Klucz zapisany"
    )

    messagebox.showinfo(
        "Gotowe",
        "Klucz najemców został zapisany."
    )

def wybierz_csv():
    global CSV_PATH

    CSV_PATH = filedialog.askopenfilename(
        title="Wybierz CSV",
        filetypes=[("CSV", "*.csv")]
    )

    lbl_plik.config(text=CSV_PATH)


def generuj_pdf():
    if not os.path.exists(KLUCZ_PATH):

        messagebox.showerror(
            "Brak klucza",
            "Najpierw wczytaj plik klucz_najemców.csv"
        )

        return   
    if not CSV_PATH:
        messagebox.showerror("Błąd", "Wybierz plik CSV")
        return

    try:

        df = pd.read_csv(
            CSV_PATH,
            header=None
        )

        df.columns = [
    "id",
    "data",
    "godzina",
    "nr",
    "masa",
    "masa2",
    "roznica",
    "jednostka",
    "yes",
    "kod_odpadu",
    "lokal",
    "tmp"
]


        klucz_path = os.path.join(
            os.path.dirname(__file__),
            "klucz_najemców.csv"
        )

        mapa = pd.read_csv(
            KLUCZ_PATH,
            encoding="utf-8"
        )

        mapa.columns = ["lokal", "najemca"]

        mapa["lokal"] = (
            mapa["lokal"]
            .astype(str)
            .str.strip()
        )

        df["lokal"] = (
            df["lokal"]
            .astype(str)
            .str.strip()
        )

        df = df.merge(
            mapa,
            on="lokal",
            how="left"
        )

        df["data"] = pd.to_datetime(
            df["data"],
            dayfirst=True,
            errors="coerce"
        )

        data_od = pd.to_datetime(
            entry_od.get(),
            dayfirst=True
        )

        data_do = pd.to_datetime(
            entry_do.get(),
            dayfirst=True
        )

        df = df[
            (df["data"] >= data_od) &
            (df["data"] <= data_do)
        ]

        df = df[df["masa"] > 0]

        podsumowanie = (
            df.groupby("kod_odpadu")["masa"]
            .sum()
            .round(2)
            .reset_index()
        )

        najemcy = (
            df.groupby(["najemca", "kod_odpadu"])["masa"]
            .sum()
            .round(2)
            .reset_index()
        )

        pdf_path = filedialog.asksaveasfilename(
        title="Zapisz raport PDF",
        defaultextension=".pdf",
        filetypes=[("PDF", "*.pdf")],
        initialfile="Raport_Odpadow.pdf"
        )

        if not pdf_path:
            return

        pdf = SimpleDocTemplate(pdf_path)

        styles = getSampleStyleSheet()

        story = []

        title = Paragraph(
            "RAPORT ODPADÓW",
            styles["Title"]
        )

        story.append(title)

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"Okres: {data_od.strftime('%d.%m.%Y')} - {data_do.strftime('%d.%m.%Y')}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "PODSUMOWANIE",
                styles["Heading2"]
            )
        )

        tabela = [["Kod odpadu", "Masa [kg]"]]

        for _, row in podsumowanie.iterrows():
            tabela.append([
                str(row["kod_odpadu"]),
                f"{row['masa']:.2f}"
            ])

        tab = Table(
            tabela,
            colWidths=[150, 150]
        )

        tab.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#163A5F")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
        ]))

        story.append(tab)

        story.append(PageBreak())

        for najemca in sorted(df["najemca"].dropna().unique()):

            dane = najemcy[
                najemcy["najemca"] == najemca
            ]

            story.append(
                Paragraph(
                    str(najemca),
                    styles["Heading2"]
                )
            )

            dane_tab = [
                ["Kod odpadu", "Masa [kg]"]
            ]

            suma = 0

            for _, row in dane.iterrows():

                dane_tab.append([
                    str(row["kod_odpadu"]),
                    f"{row['masa']:.2f}"
                ])

                suma += row["masa"]

            dane_tab.append([
                "RAZEM",
                f"{suma:.2f}"
            ])

            t = Table(
                dane_tab,
                colWidths=[150, 150]
            )

            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#163A5F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold")
            ]))

            story.append(t)
            story.append(Spacer(1, 15))

        pdf.build(story)

        messagebox.showinfo(
        "Gotowe",
        f"Raport zapisano:\n{pdf_path}"
        )

    except Exception as e:
        messagebox.showerror(
            "Błąd",
            str(e)
        )


root = Tk()
root.title("Generator Raportów Odpadów")
root.geometry("700x450")
root.resizable(False, False)

# ===== Tytuł =====

Label(
    root,
    text="Generator Raportów Odpadów",
    font=("Segoe UI", 18, "bold")
).pack(pady=(20, 10))

# ===== Ramka pliku =====

frame_csv = LabelFrame(
    root,
    text="Źródło danych",
    padx=15,
    pady=15
)

frame_csv.pack(fill="x", padx=20, pady=10)

Button(
    frame_csv,
    text="📂 Wybierz plik CSV",
    font=("Segoe UI", 10),
    command=wybierz_csv
).pack(anchor="w")

lbl_plik = Label(
    frame_csv,
    text="Nie wybrano pliku",
    fg="gray",
    wraplength=600,
    justify="left"
)

lbl_plik.pack(anchor="w", pady=(10, 0))

Button(
    frame_csv,
    text="🏢 Zmień klucz najemców",
    font=("Segoe UI", 10),
    command=wybierz_klucz
).pack(anchor="w", pady=(10, 0))

if os.path.exists(KLUCZ_PATH):
    status = "✓ Klucz załadowany"
else:
    status = "Brak klucza"

lbl_klucz = Label(
    frame_csv,
    text=status,
    fg="darkgreen"
)

lbl_klucz.pack(anchor="w", pady=(5, 0))

# ===== Ramka okresu =====

frame_okres = LabelFrame(
    root,
    text="Zakres raportu",
    padx=15,
    pady=15
)

frame_okres.pack(fill="x", padx=20, pady=10)

Label(
    frame_okres,
    text="Data od:"
).grid(row=0, column=0, sticky="w")

entry_od = Entry(
    frame_okres,
    width=15,
    font=("Segoe UI", 10)
)

entry_od.insert(0, "01.06.2026")
entry_od.grid(row=0, column=1, padx=10)

Label(
    frame_okres,
    text="Data do:"
).grid(row=0, column=2, sticky="w")

entry_do = Entry(
    frame_okres,
    width=15,
    font=("Segoe UI", 10)
)

entry_do.insert(0, "30.06.2026")
entry_do.grid(row=0, column=3, padx=10)

# ===== Generowanie =====

Button(
    root,
    text="📄 Generuj PDF",
    font=("Segoe UI", 12, "bold"),
    bg="#163A5F",
    fg="white",
    padx=20,
    pady=10,
    command=generuj_pdf
).pack(pady=30)

# ===== Stopka =====

Label(
    root,
    text="CSV → PDF | Raport odpadów",
    fg="gray"
).pack(side="bottom", pady=10)

root.mainloop()
