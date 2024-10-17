from pdf_template_manager import PdfTemplateManager
from colors import TailwindColors

content = [
    {
        "type": "line",
        "args": {
            "x1": 3,
            "x2": 7,
            "y1": 99,
        }
    },
    {
        "type": "text",
        "args": {
            "lines": ["DaumDigital", "Julius Daum", "Olshausenstr. 11", "24118 Kiel"],
            "one_line": True,
            "w": 80,
            "y": 50,
            "size": 7,
            "color": TailwindColors.SLATE_600.value
        }
    },
    {
        "type": "text",
        "args": {
            "lines": [
                "DaumDigital",
                "Julius Daum", 
                "Olshausenstr. 11", 
                "24118 Kiel", 
                "Tel: +49 (0) 1523 7702533", 
                "daum.julius256@gmail.com", 
                "www.daumdigital.de", 
                "St.-Nr.: 2005403217"
            ],
            "x": 23,
            "y": 10,
            "align": "R",
            "size": 9
        }
    },
    {
        "type": "text",
        "args": {
            "lines": ["DaumDigital", "Julius Daum", "Olshausenstr. 11", "24118 Kiel"],
            "y": 60,
            "w":80
        }
    },
    {
        "type": "text",
        "args": {
            "lines": ["Rechnung 230282-287"],
            "y": 92,
            "x": 23,
            "size": 12,
            # "color": TailwindColors.PINK_600.value,
            "color": TailwindColors.INDIGO_600.value,
            "style": "B",
            "pb": 5
        }
    },
    {
        "type": "text",
        "args": {
            "lines": ["Datum: 16.10.2024", "Bearbeiter: Julius Daum"],
            "y": 92,
            "x": 23,
            "align": "R",
            "pb": 5
        }
    },
    {
        "type": "text",
        "args": {
            "lines": ["Vielen Dank für Ihr Vertrauen in unsere Leistungen.", "Wir erlauben uns folgendes in Rechnung zu stellen:"],
            "pb": 5
        }
    },
    {
        "type": "table",
        "args": {
            "table_items": [
                ("Beschreibung", "Einzelpreis", "Menge", "Einheit", "Summe"),
                ("Yamaha CFX Konzertflügel\n\nBitte registrieren Sie Ihr Instrument innerhalb von 6 Monaten nach dem Kaufdatum und Sie erhalten eine Garantieverlängerung von 2 auf 5 Jahre. https://de.yamaha.com/de/support/warranty/index.", "150000,00 €", "1", "Stk.", "150000,00 €"),
                ("Yamaha Clavinova Digitalpiano Modell: CLP - 775 Ausführung: Rosenholz", "3249,00 €", "1,00", "Stk.", "3249,00 €"),
                ("Hochwertige Sitzbank Ausführung: Rosenholz", "170,00 €", "1,00", "Stk.","170,00 €"),
                ("Notenständer - Verstellbar und klappbar", "45,00 €", "2,00", "Stk.", "90,00 €"),
                ("Anfertigung von maßgeschneiderten Notenständern mit eingebauter LED-Beleuchtung, ideal für Musiker, die bei schwachem Licht spielen. Inklusive 2 Jahre Garantie auf alle Teile.", "189,00 €", "1,00", "Stk.", "189,00 €"),
                ("Premium Klavierpflege-Set mit Reinigungsmittel, Tuch und Bürste", "30,00 €", "1,00", "Set", "30,00 €"),
                ("Konzertflügel-Service (Stimmen und Reinigen)", "350,00 €", "1,00", "Service", "350,00 €"),
                ("Handgefertigter Flügelhocker aus Mahagoni-Holz, gepolstert mit hochwertigem Lederbezug, für höchsten Sitzkomfort. Perfekt für lange Übungsstunden und Auftritte.", "299,00 €", "1,00", "Stk.", "299,00 €"),
                ("Transport eines Konzertflügels innerhalb Deutschlands", "500,00 €", "1,00", "Psch.", "500,00 €"),
                ("Leihgabe eines Digitalpianos für 3 Monate", "600,00 €", "1,00", "Psch.", "600,00 €"),
                ("Mietservice für Klavierbänke (6 Monate)", "180,00 €", "6,00", "Monat", "180,00 €")
            ],
            "col_widths": (85, 25, 15, 15, 24),
            "padding": (1,0,1,0),
            "borders_layout": "HORIZONTAL_LINES",
            # "borders_layout": "NONE",
            "text_align": ("LEFT", "RIGHT", "CENTER", "CENTER", "RIGHT"), 
            "cell_fill_color": TailwindColors.GRAY_50.value,
            "pb": 5,
            "line_color": TailwindColors.PINK_400.value,
            # "cell_fill_mode": "ROWS",
            # "cell_fill_mode": "EVEN_ROWS",
            # "headings_style": FontFace(emphasis="Bold", fill_color=TailwindColors.GRAY_200.value)
        }
    },
    {
        "type": "table",
        "args": {
            "table_items": [
                ("", "Zwischensumme (EUR)", "2873,11 €"),
                ("", "19% MWSt.", "545,89 €"),
                ("", "Individueller Rabatt", "-341,99 €"),
                ("", "Gesamtsumme (EUR)", "3419,89 €"),
            ],
            "unbreakable": True,
            "borders_layout": "NONE",
            "first_row_as_headings": False,
            "col_widths": (85, 39.5, 39.5),
            "text_align": ("LEFT", "LEFT", "RIGHT"),
            "gutter_width": 0,
            "padding": (1,0,1,0),
            "cell_formats": {
                "3.1": {
                    # "bg_color": TailwindColors.PINK_600.value,
                    "bg_color": TailwindColors.INDIGO_600.value,
                    "color": (255,255,255),
                    # "style": "B",
                },
                "3.2": {
                    # "bg_color": TailwindColors.PINK_600.value,
                    "bg_color": TailwindColors.INDIGO_600.value,
                    "color": (255,255,255),
                    # "style": "B",
                }
            }, 
            "pb": 10,
        }
    },
    {
        "type": "text",
        "args": {
            "lines": [
                "Vielen Dank für Ihren Auftrag!",
                "In dieser Rechnung ist gemäß §19(1) UStG keine Umsatzsteuer enthalten.",
            ],
            "pb": 20
        }
    },
    {
        "type": "text",
        "args": {
            "lines": ["Bitte nutzen Sie für die Überweisung folgende Daten:"],
            "y": 240,
            "style": "B"
        },
    },
    {
        "type": "text",
        "args": {
            "lines": ["Institut: C24 Bank", "IBAN: DE08 2501 0030 0000 2893 04", "Inhaber: Julius Daum", "BIC: DEXXXX"],
        },
    },
]

if __name__ == "__main__":
    pdf = PdfTemplateManager()
    pdf.render(content, "example.pdf")