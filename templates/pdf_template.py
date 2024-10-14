import os
from fpdf import FPDF, XPos, YPos
from fpdf.enums import VAlign
from colors import TailwindColors
from datetime import datetime


pdf_document = {
    "meta": {},
    "formatting": {
        "line_height": 1.2,
        "typography": {
            "family": "Roboto",
            "style": "",
            "size": 12,
            "color": None
        },
        "footer": {
            "show_page_number": True,
            "page_number_align": "C",
            "page_number_on_first_page": False,
            "page_number_typography": {},
        },
        "fold_marks": [
            {
                "y": 99,
                "pl": 3,
                "color": None,
                "length": 5
            }
        ]
    }
}



class PdfTemplate(FPDF):
    """
    For our purpose, its not enough to use the built-in template engine.
    Furthermore, we need to use customized elements such as tables and much more.
    This class provides basic features to use.
    Inheriting classes will only affect the visuability of the content.
    Here, we will declare the very basic appearance of all templates and building blocks.
    """
    # Some default values we use later on in this class
    default_line_height_multiplicator = 1.4
    # Values for the margin
    default_marginX = 23
    default_marginY = 10


    def __init__(self, elements: dict=None, filename: str="", title: str="", author: str="", subject: str="", creator: str="") -> None:
        """
        Initialize the pdf file as default din4 document and take some
        required meta data.
        Args:
            elements (dict): The dictionary of the items we want to display on our document.
                The dictionary contains the actual data as well as data related to formatting and/or 
                meta data of the file.
            filename (str): The name of the document.
            title (str): The title of the document.
            author (str): The name of the author.
            subject (str): Subject matter of the document.
            creator (str): The creator of the document.
        """
        super().__init__(orientation="P", format="A4")
        # TODO: set the tile, author, subject and creator of the document!
        # Adding the meta data
        self.set_title(title)
        self.set_author(author)
        self.set_subject(subject)
        self.set_creator(creator)
        self.set_creation_date(datetime.now())
        self.load_fonts()
        self.set_typography()
        self.add_page()
        self.filename = filename
        self.doc_data = elements
    
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
    def line_height(self) -> float:
        return self.font_size * self.default_line_height_multiplicator

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
    
    def set_typography(self, family: str="Roboto", style: str="", size: float=10, color: tuple=TailwindColors.SLATE_800.value) -> None:
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
        self.set_font(family=family, style=style, size=size)

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
            kwrags (typography): Provide values for the typography such as family, style, size and color.
        """
        self.set_typography(**kwargs)
        if x is not None or y is not None:
            x = x if x is not None else self.get_x()
            y = y if y is not None else self.get_y()
            self.set_xy(x,y)
        for ln in lines:
            self.multi_cell(w=w, h=self.line_height, text=ln, new_x=XPos.LEFT, new_y=YPos.NEXT, align=align)
        self.render_next_line()
        self.set_typography()

    def render_table(
            self, 
            table_items: list,
            v_align=VAlign.T,
            **kwargs,
        ) -> None:
        """
        Leverages the built-in table function to create a customized table.
        For more information about the table in fpdf2, checkout the following documentation:
            https://py-pdf.github.io/fpdf2/Tables.html
        """
        if "line_height" not in kwargs:
            kwargs["line_height"] = self.line_height
        with self.table() as table:
            for row_index, data_row in enumerate(table_items):
                row = table.row()
                for cell_index, datum in enumerate(data_row):
                    row.cell(datum)

    """
    Here, we provide some custom functionalities for all extending documents.
    The functionalities includes formatting, content blocks and more.
    """


if __name__ == "__main__":
    pdf = PdfTemplate(filename="template.pdf")
    pdf.render_text(["Hello World"])
    pdf.render_table(table_items=(("Name", "Preis", "Stück"), ("MacBook Pro M1", "1400 €", "3"), ("Sprottenwasser", "1.45 €", "9"),))
    pdf.output(pdf.filename)