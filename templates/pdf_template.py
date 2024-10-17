import os
from fpdf import FPDF, XPos, YPos, Template, FontFace
from fpdf.enums import VAlign
from colors import TailwindColors
from datetime import datetime
from typing import List


formats = {
    "mx": 23,
    "my": 10,
    "pf": 10,
    "ph": 10,
    "line_height": 1.4,
    "primary_color": (79, 70, 229),
    "secondary_color": (71, 85, 105),
    "primary_contrast_color": (255,255,255),
    "typography": {
        "family": "Roboto",
        "style": "",
        "size": 10,
        "color": (30, 41, 59)
    },
    "footer": {
        "show_page_number": True,
        "align": "R",
        "show_on_first_page": True,
        "typography": {
            "style": "B"
        }
    },
    "fold_marks": [
        {
            "y": 99,
            "pl": 3,
            "color": (30, 41, 59),
            "length": 5
        }
    ]
}



class PdfTemplateManager(FPDF):
    """
    For our purpose, its not enough to use the built-in template engine.
    Furthermore, we need to use customized elements such as tables and much more.
    This class provides basic features to use.
    Inheriting classes will only affect the visuability of the content.
    Here, we will declare the very basic appearance of all templates and building blocks.
    """

    def __init__(self, elements: dict=None, filename: str="") -> None:
        """
        Initialize the pdf file as default din4 document and take some
        required meta data.
        Args:
            elements (dict): The dictionary of the items we want to display on our document.
                The dictionary contains the actual data as well as data related to formatting and/or 
                meta data of the file.
            filename (str): The name of the document.
        """
        super().__init__(orientation="P", format="A4")
        # Loading the default formats into this template
        self.formats = formats
        # Start loading and setting the correct data
        self.load_fonts()
        self.set_typography()
        self.add_page()
        self.filename = filename
        self.blocks = elements
        self.set_auto_page_break(True, self.marginY + self.paddingFooter)
    
    def footer(self) -> None:
        if not self.formats["footer"]["show_page_number"]:
            return
        
        y = self.HEIGHT - self.my
        self.set_y(y)
        self.render_text(
            [f"Seite {self.page_no()} von {{nb}}"], 
            size=8, 
            style=self.formats["footer"]["typography"]["style"], 
            align=self.formats["footer"]["align"]
        )
        self.set_typography()

    """
    Here, we provide some basic functions / properties of the class
    that can later on be utilized such as the document height and width 
    of the DIN4 format standard.
    More information of the DIN4 standard, checkout the following source:
    https://www.adobe.com/de/creativecloud/design/discover/a4-format.html
    """
    # ==== Basic props ====
    @property
    def HEIGHT(self) -> int:
        return 297
    
    @property 
    def WIDTH(self) -> int:
        return 210
    
    @property
    def marginX(self) -> float:
        return self.formats["mx"]

    @property
    def marginY(self) -> float:
        return self.formats["my"]

    @property
    def paddingHeader(self) -> float:
        return self.formats["ph"]

    @property
    def paddingFooter(self) -> float:
        return self.formats["pf"]
    
    @property
    def line_height(self) -> float:
        return self.font_size * self.formats["line_height"]
    
    @property
    def primary_color(self) -> tuple:
        return self.formats["primary_color"]
    
    @property
    def primary_contrast_color(self) -> tuple:
        return self.formats["primary_color"]

    @property
    def secondary_color(self) -> tuple:
        return self.formats["secondary_color"]

    # ==== Utils ====
    def load_fonts(self) -> None:
        """
        Simply loads all existing fonts we have installed.
        For better performance, we simply have them hardcoded.
        """
        # Roboto
        self.add_font("Roboto", fname=f"{os.getcwd()}/fonts/Roboto/Roboto-Regular.ttf")
        self.add_font("Roboto", style="B", fname=f"{os.getcwd()}/fonts/Roboto/Roboto-Bold.ttf")
        self.add_font("Roboto", style="I", fname=f"{os.getcwd()}/fonts/Roboto/Roboto-Italic.ttf")
        # Poppins
        self.add_font("Poppins", fname=f"{os.getcwd()}/fonts/Poppins/Poppins-Regular.ttf")
        self.add_font("Poppins", style="B", fname=f"{os.getcwd()}/fonts/Poppins/Poppins-Bold.ttf")
        self.add_font("Poppins", style="I", fname=f"{os.getcwd()}/fonts/Poppins/Poppins-Italic.ttf")
        # # Inter
        # self.add_font("Inter", fname=f"{os.getcwd()}/fonts/Roboto/Roboto-Regular.ttf")
        # self.add_font("Inter", style="B", fname=f"{os.getcwd()}/fonts/Roboto/Roboto-Bold.ttf")
        # self.add_font("Inter", style="I", fname=f"{os.getcwd()}/fonts/Roboto/Roboto-Italic.ttf")
        # Montserrat
        self.add_font("Montserrat", fname=f"{os.getcwd()}/fonts/Montserrat/static/Montserrat-Regular.ttf")
        self.add_font("Montserrat", style="B", fname=f"{os.getcwd()}/fonts/Montserrat/static/Montserrat-Bold.ttf")
        self.add_font("Montserrat", style="I", fname=f"{os.getcwd()}/fonts/Montserrat/static/Montserrat-Italic.ttf")

    def render_next_line(self, new_y: float|None=None) -> None:
        """
        Sets the cursor to the next line of the document. This function
        takes the prop `line_height` as grounding truth.
        When using this function, the next line will always set the pointer 
        for the x value to the left margin.
        Args:
            new_y (float): Optional value for the next line.
        """
        if new_y is not None:
            self.set_xy(self.l_margin, new_y)
        else:
            self.set_xy(self.l_margin, self.get_y() + self.line_height)

    def fold_marks(
            self, 
            pl: int|None=3, 
            y: float|None=99, 
            color: tuple|None=TailwindColors.SLATE_900.value,
            length: float|None=4,
            w: float|None=.1
        ) -> None:
        """
        Allows to enter / draw fold marks into our document.
        Args:
            pl (int): Optional left padding. If not set, default values is 4.
            y (float): Optional value for the y position of the line. Default is 99.
            color (tuple): Optional value for the color. Default is SLATE_900.
            length (float): Optional value for the length of the line. Default is 4.
            w (float): Optionla value for the width (actually the height) of the line. Default value is 0.1.
        """
        prev_line_color, prev_line_width = self.draw_color, self.line_width
        self.set_draw_color(color)
        self.set_line_width(w)
        self.line(pl, y, pl + length, y)
        self.set_draw_color(prev_line_color)
        self.set_line_width(prev_line_width)
    
    def set_typography(self, family: str="Roboto", style: str="", size: float=10, color: tuple|None=None) -> None:
        """
        This function leverages the built-in `set_font` and `set_text_color` functions to set directly all values at once.
        Args:
            family (str): The font family we want to use. Default value is the `Roboto` font.
            style (str): The style of the font. Choose between no style (empty string), bold (B), italic (I), underline (U) and bold-italic (BI). 
                Default value is `regular` | no formatting.
            size (float): The font size. Default value is 10.
            color (tuple): The color of the font. Default value is SLATE900 by tailwind color palette.
        """
        if color is not None:
            self.set_text_color(*color)
        else:
            self.set_text_color(*self.formats["typography"]["color"])
        self.set_font(family=family, style=style, size=size)

    def render_line(
            self, 
            x1: float|None=None, 
            y1: float|None=None, 
            x2: float|None=None, 
            y2: float|None=None, 
            w: float|None=0.1, 
            color: tuple|None=TailwindColors.SLATE_900.value
        ) -> None:
        """
        Renders a line with given color and width.
        Args:
            x1 (float): Starting x coordinate of the line.
            y1 (float): Starting y coordinate of the line.
            x2 (float): Ending x coordinate of the line.
            y2 (float): Ending y coordinate of the line.
            w (float): The width (height) of the line.
            color (tuple): The color of the line.
        """
        if x2 is None:
            x2 = x1
        if y2 is None:
            y2 = y1
        p_c, p_w = self.draw_color, self.line_width
        self.set_draw_color(color)
        self.set_line_width(w)
        self.line(x1, y1, x2, y2)
        self.set_draw_color(p_c)
        self.set_line_width(p_w)

    def render_formatting_data(
            self,
            line_height: float=1.4,
            font_family: str="Roboto",
            font_style: str="",
            font_size: float=10,
            font_color: tuple=TailwindColors.SLATE_800.value,
            mx: float=23,
            my: float=10
        ) -> None:
        """
        Takes as input formatting data such as the default typography, margins and paddings.
        Args:
            line_height (float): Default value for all line_heights.
            font_family (str): Value for the font family.
            font_style (str): Value for the formatting of the font.
            font_size (float): Value (in points) for the font size.
            font_color (tuple): Color of the font.
            mx (float): Value for the left and right margin.
            my (float): Value for the top and bottom margin.
        """
        self.set_typography(font_family, font_style, font_size, font_color)
        self.mx = mx
        self.my = my
        self.set_margin(my)
        self.set_left_margin(mx)
        self.set_right_margin(mx)
        self.default_line_height_multiplicator = line_height

    def render_meta_data(self, title: str="", author: str="", subject: str="", creator: str="") -> None:
        """
        Takes as argument the meta data of the document and sets them.
        Args:
            title (str): The title of the document.
            author (str): The name of the author.
            subject (str): Subject matter of the document.
            creator (str): The creator of the document.
        """
        # Adding the meta data
        self.set_title(title)
        self.set_author(author)
        self.set_subject(subject)
        self.set_creator(creator)
        self.set_creation_date(datetime.now())

    def render_signature_area(
            self, 
            w: float=60, 
            x: float|None=None, 
            y: float|None=None, 
            pb: float|None=None,
            text: str="",
            line_width: float|None=None,
            line_color: tuple|None=None,
        ) -> None:
        """
        Provides an area to enter a signature or something similar.
        Args:
            w (float): Optional length of the line in mm.
            x (float): Optional x coordinate of the line.
            y (float): Optional y coordinate of the line.
            pb (float): Optional bottom padding of the line (space between line and text).
            text (str): Optinoal text to render below the line.
            line_width (float): Optional width (actually height) of the line.
            line_color (tuple): Optional color of the line.
        """
        if x is not None or y is not None:
            x = x if x is not None else self.get_x()
            y = y if y is not None else self.get_y()
            self.set_xy(x,y)
        prev_line_width, prev_line_color = self.line_height, self.draw_color
        if line_width is not None:
            self.set_line_width(line_width)
        if line_color is not None:
            self.set_draw_color(line_color)
        x,y = self.get_x(), self.get_y()
        self.line(x, y, x+w, y)
        self.next_line(y+self.line_height * .35)
        self.render_text([text],x=x)
        self.set_line_width(prev_line_width)
        self.set_draw_color(prev_line_color)


    def render_text(
            self, 
            lines: list, 
            x: float|None=None, 
            y: float|None=None, 
            w: float=0,
            align: str="L", 
            separator: str="•",
            one_line: bool=False,
            pt: float=0,
            pb: float=0,
            **kwargs,
        ) -> None:
        """
        Renders text with optional settings such as the typography or the absolute position on the document.
        Args:
            lines (list): A list of strings we want to render as new-starting lines.
            x (float): Absolute value of the x coordinate to start.
            y (float): Absolute value of the y coordinate to start.
            w (float): The width of the text block.
            align (str): The alignment of the text. 
                For more information check out the documentation: 
                https://py-pdf.github.io/fpdf2/fpdf/enums.html#fpdf.enums.Align
            separator (str): A string which can be used to seperate the items or the `lines` argument.
                Only takes action, if the flag one_line is set.
            one_line (bool): A boolean flag, to render the entire content in one line.
            kwrags (typography): Provide values for the typography such as family, style, size and color.
        """
        self.set_typography(**kwargs)
        if x is not None or y is not None:
            x = x if x is not None else self.get_x()
            y = y if y is not None else self.get_y()
            self.set_xy(x,y)

        self.render_next_line(self.get_y() + pt)
        if one_line:
            ln = f" {separator} ".join(lines)
            self.multi_cell(w=w, h=self.line_height, text=ln, new_x=XPos.LEFT, new_y=YPos.NEXT, align=align)
        else:
            for ln in lines:
                self.multi_cell(w=w, h=self.line_height, text=ln, new_x=XPos.LEFT, new_y=YPos.NEXT, align=align)
        # self.render_next_line()
        self.render_next_line(self.get_y() + pb)
        self.set_typography()

    def render_cell(self, bg_color: tuple=(255,255,255), **kwargs: dict) -> None:
        """
        If given, applies customized settings for each cell such as typography, bg color or something else.
        Args:
            bg_color (tuple): The background color of the current cell.
            kwargs (dict): Typography props.
        """
        self.set_fill_color(bg_color)
        self.set_typography(**kwargs)

    def __estimate_number_of_table_rows(self, items: List[tuple], col_widths: tuple=None) -> int:
        """
        Based on given parameters, this function estimates the number of rows of our table.
        The number of rows is the number, which is actually printed on the pdf document.
        Args:
            items (list): A nested list of table items, where the entire list represents all rows
                and each item inside the nested lists represents a single cell of the table.
            col_widths (tuple): Optional tuple containing the splitting for each column of the table.
        """
        num_of_items = len(items)
        if col_widths is None:
            col_widths = (self.WIDTH - self.l_margin - self.r_margin) / num_of_items
        # Using temporary values for the x and y to compute the actual number of lines later on
        tmp_x, tmp_y = self.get_x(), self.get_y()
        # Also holding a maximum y value
        max_y = tmp_y
        num_of_rows = 0
        with self.offset_rendering() as dummy:
            for row in items:
                for index, col in enumerate(row):
                    # Here, we iterate over each cell of the table and use the dummy to render them all
                    # at the very beginning of the current line.
                    # When some cell extends the current maximum (has more than one line), it updates the 
                    # maximum. Otherwise, it does not.
                    dummy.set_x(tmp_x)
                    dummy.set_y(tmp_y)
                    dummy.multi_cell(w=col_widths[index], text=col, h=self.line_height)

                    if max_y < dummy.get_y():
                        max_y = dummy.get_y()
                # Add the estimated number of rows to the total number
                num_of_rows += (max_y - tmp_y) / self.line_height
                tmp_y = max_y
        return int(round(num_of_rows))

    def estimate_table_height(
            self, 
            table_items: list,
            padding: tuple=(0,0,0,0), 
            gutter_height: float=0, 
            col_widths: tuple|None=None,
            **kwargs: dict
        ) -> float:
        """
        This function calculates the height of a table.
        This function can be used to make sure, that some tables are renderd on the same page.
        Args:
            num_of_items (int): The number of table items.
            padding (tuple): Optional value for padding of each cell. (Top, right, bottom, left).
            gutter_height (float): Optional vertical space between rows.
        """
        num_of_lines = self.__estimate_number_of_table_rows(table_items, col_widths)
        # Use the current y value as starting point and add the top and bottom padding
        height = self.get_y()
        height += num_of_lines * (self.line_height)
        height += len(table_items) * (padding[0] + padding[2])
        height += num_of_lines * gutter_height
        return height

    def render_table(
            self, 
            table_items: list,
            v_align=VAlign.T,
            line_color: tuple=(0,0,0),
            line_width: float=0.2,
            pt: float=0,
            pb: float=0,
            unbreakable: bool=False,
            cell_formats: dict={},
            **kwargs,
        ) -> None:
        """
        Leverages the built-in table function to create a customized table.
        For more information about the table in fpdf2, checkout the following documentation:
            https://py-pdf.github.io/fpdf2/Tables.html
        """
        self.render_next_line(self.get_y() + pt)
        if "line_height" not in kwargs:
            kwargs["line_height"] = self.line_height
        kwargs["v_align"] = v_align
        prev_line_color, prev_line_width = self.draw_color, self.line_width
        self.set_draw_color(line_color)
        self.set_line_width(line_width)

        # If the estimated table height extends the threshold for the printable area,
        # we force here a new page
        table_height = self.__estimate_table_height(table_items, pt=pt, pb=pb, **kwargs)
        print(f"Current y: {self.get_y()}; Table height: {table_height}")
        if unbreakable and table_height >= self.HEIGHT - self.marginY - self.paddingFooter:
            print(f"Apply page break!")
            self.add_page()
        
        print(f"y-value before table: {self.get_y()}")
        # Make the entire table unbreakable
        with self.table(**kwargs) as table:
            for row_index, data_row in enumerate(table_items):
                row = table.row()
                for cell_index, datum in enumerate(data_row):
                    key = f"{row_index}.{cell_index}"
                    if key in cell_formats:
                        args = cell_formats[key]
                        self.render_cell(**args)
                    row.cell(datum)
                    if key in cell_formats:
                        self.render_cell()
        print(f"y-value after table: {self.get_y()}={table_height}")

        self.set_draw_color(prev_line_color)
        self.set_line_width(prev_line_width)
        self.render_next_line(self.get_y() + pb)

    def render(self, content: dict, formats: dict|None=None) -> None:
        """
        Based on the `blocks`, this function takes the content we want to fill and inserts the content
        to their corresponding positions.
        After rendering, this function also creates the pdf file and stores it under the `filename` name.
        """
        if formats is not None:
            self.render_formatting_data(**formats)
        else:
            self.render_formatting_data()

        for item in content:
            type, args = item["type"], item["args"]
            if type == "text":
                self.render_text(**args)
                continue
            elif type == "line":
                self.render_line(**args)
                continue
            elif type == "table":
                self.render_table(**args)
                continue
        
        self.output(self.filename)


# invoice_template = [
#     {
#         "type": "text",
#         "x1": 
#     },
#     {},
#     {},
# ]
# formats = {
#     "mx": 50,
#     "my": 50
# }
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
            "color": TailwindColors.PINK_600.value,
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
                ("Transport eines Konzertflügels innerhalb Deutschlands", "500,00 €", "1,00", "Pauschal", "500,00 €"),
                ("Leihgabe eines Digitalpianos für 3 Monate", "600,00 €", "1,00", "Pauschal", "600,00 €"),
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
                    "bg_color": TailwindColors.PINK_600.value,
                    "color": (255,255,255),
                    # "style": "B",
                },
                "3.2": {
                    "bg_color": TailwindColors.PINK_600.value,
                    "color": (255,255,255),
                    # "style": "B",
                }
            }, 
            "pb": 10,
        }
    },
    # {
    #     "type": "text",
    #     "args": {
    #         "lines": [
    #             "Vielen Dank für Ihren Auftrag!",
    #             "In dieser Rechnung ist gemäß §19(1) UStG keine Umsatzsteuer enthalten.",
    #         ],
    #         "pb": 20
    #     }
    # },
    # {
    #     "type": "text",
    #     "args": {
    #         "lines": ["Bitte nutzen Sie für die Überweisung folgende Daten:"],
    #         "y": 260,
    #         "style": "B"
    #     },
    # },
    # {
    #     "type": "text",
    #     "args": {
    #         "lines": ["Institut: C24 Bank", "IBAN: DE08 2501 0030 0000 2893 04", "Inhaber: Julius Daum", "BIC: DEXXXX"],
    #     },
    # },
]

if __name__ == "__main__":
    pdf = PdfTemplateManager(filename="template.pdf")
    pdf.render(content)
    # pdf.render_text(["Hello World"])
    # pdf.render_table(table_items=(("Name", "Preis", "Stück"), ("MacBook Pro M1", "1400 €", "3"), ("Sprottenwasser", "1.45 €", "9"),))
    # pdf.render(pdf.filename)