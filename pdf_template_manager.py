import os
from datetime import datetime
from typing import List

from fpdf import FPDF, XPos, YPos
from fpdf.enums import VAlign

from colors import TailwindColors


# Providing the default formats for our template manager
formats = {
    "mx": 23,
    "my": 10,
    "pf": 10,
    "ph": 10,
    "line_height": 1.4,
    "primary_color": TailwindColors.INDIGO_600.value,
    "secondary_color": TailwindColors.SLATE_600.value,
    "primary_contrast_color": (255,255,255),    # using white for more contrast
    "typography": {
        "family": "Roboto",
        "style": "",
        "size": 10,
        "color": TailwindColors.SLATE_800.value,
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
            "color": TailwindColors.SLATE_800.value,
            "length": 5
        }
    ]
}


class PdfTemplateManager(FPDF):
    """
    Pdf document generation class.
    Takes as input a template consisting of several basic building blocks and 
    outputs the corresponding pdf file.
    """
    def __init__(self, orientation = "portrait", format = "A4"):
        super().__init__(orientation=orientation, format=format)
        self.formats = formats
        self.apply_formats()
        self.load_fonts()
        self.set_typography()
        self.add_page()
    
    @property
    def HEIGHT(self) -> int:
        return 297
    
    @property
    def WIDTH(self) -> int:
        return 210
    
    @property
    def marginX(self) -> int:
        return self.formats["mx"]
    
    @property
    def marginY(self) -> int:
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
    def primary_main_color(self) -> tuple:
        return self.formats["primary_color"]
    
    @property
    def primary_contrast_text(self) -> tuple:
        return self.formats["primary_contrast_color"]
    
    @property
    def secondary_color(self) -> tuple:
        return self.formats["secondary_color"]
    
    # ==== Overriding the built-in functions ====
    def header(self) -> None:
        pass

    def footer(self) -> None:
        if not self.formats["footer"]["show_page_number"]:
            return
        
        y = self.HEIGHT - self.marginY
        self.set_y(y)
        self.render_text(
            [f"Seite {self.page_no()} von {{nb}}"], 
            size=8, 
            style=self.formats["footer"]["typography"]["style"], 
            align=self.formats["footer"]["align"]
        )
        self.set_typography()

    # ==== Utility functions ==== #
    def set_meta_data(self, title: str="", author: str="", subject: str="", creator: str="") -> None:
        """
        Takes as argument the meta data of the document and sets them.
        Sets automatically the current date as date for the document.
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

    def merge(self, source, destination):
        """
        Merges two dictionaries with each other.
        Found here: https://stackoverflow.com/a/20666342/22250877
        """
        for key, value in source.items():
            if isinstance(value, dict):
                # get node or create one
                node = destination.setdefault(key, {})
                self.merge(value, node)
            else:
                destination[key] = value
        return destination

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

    def apply_formats(self, formats: dict|None=None) -> None:
        """
        This function applies the formats of the template. Either use the built-in formats or 
        take an optional argument for new formats and apply them.
        If the new `formats` does not contain all values, simply merge them with the existing
        formats.
        Args:
            formats (dict): A dictionary containing customized values for the formats.
        
        TODO: Testing this function!!!
        """
        if formats is not None:
            self.formats = self.merge(dict(self.formats), formats)

        self.set_top_margin(self.marginY + self.paddingHeader)
        self.set_left_margin(self.marginX)
        self.set_right_margin(self.marginX)
        self.set_auto_page_break(True, self.marginY + self.paddingFooter)

    def set_typography(self, family: str|None=None, style: str="", size: int|None=None, color: tuple|None=None) -> None:
        """
        Simply applies settings to the text styling such as font family, the style and the font size.
        Also changes the color of the text.
        If nothing is given, it loads the default configs from the `formats`.
        Args:
            family (str): The name of the font family.
            style (str): The styling of texts. Choose between normal (""), bold ("B"), italic ("I"), 
                underline ("U") or bold-italic ("BI").
            size (int): The size of the font. 
            color (tuple): Color of the text.
        """
        if family is None:
            family = self.formats["typography"]["family"]

        if size is None:
            size = self.formats["typography"]["size"]

        if color is None:
            color = self.formats["typography"]["color"]
        
        self.set_text_color(*color)
        self.set_font(family=family, style=style, size=size)
    
    def next_line(self, new_y: float|None=None) -> None:
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
    
    # ==== Functions to render content blocks in the document ==== #
    def render_line(
            self, 
            x1: float|None=None, 
            y1: float|None=None, 
            x2: float|None=None, 
            y2: float|None=None, 
            line_width: float|None=0.1, 
            color: tuple|None=None
        ) -> None:
        """
        Renders a line with given color and width.
        Args:
            x1 (float): Starting x coordinate of the line.
            y1 (float): Starting y coordinate of the line.
            x2 (float): Ending x coordinate of the line.
            y2 (float): Ending y coordinate of the line.
            line_width (float): The width (height) of the line.
            color (tuple): The color of the line.
        
        TODO: Write a test for setting x2=x1 and y2=y1
        """
        if x2 is None:
            x2 = x1
        if y2 is None:
            y2 = y1
        if color is None:
            color = TailwindColors.SLATE_900.value

        p_c, p_w = self.draw_color, self.line_width
        self.set_draw_color(color)
        self.set_line_width(line_width)
        self.line(x1, y1, x2, y2)
        self.set_draw_color(p_c)
        self.set_line_width(p_w)
    
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

        self.next_line(self.get_y() + pt)
        if one_line:
            ln = f" {separator} ".join(lines)
            self.multi_cell(w=w, h=self.line_height, text=ln, new_x=XPos.LEFT, new_y=YPos.NEXT, align=align)
        else:
            for ln in lines:
                self.multi_cell(w=w, h=self.line_height, text=ln, new_x=XPos.LEFT, new_y=YPos.NEXT, align=align)
        # self.render_next_line()
        self.next_line(self.get_y() + pb)
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
        self.next_line(self.get_y() + pt)
        if "line_height" not in kwargs:
            kwargs["line_height"] = self.line_height
        kwargs["v_align"] = v_align
        prev_line_color, prev_line_width = self.draw_color, self.line_width
        self.set_draw_color(line_color)
        self.set_line_width(line_width)

        # If the estimated table height extends the threshold for the printable area,
        # we force here a new page
        table_height = self.estimate_table_height(table_items, pt=pt, pb=pb, **kwargs)
        if unbreakable and table_height >= self.HEIGHT - self.marginY - self.paddingFooter:
            self.add_page()
        
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

        self.set_draw_color(prev_line_color)
        self.set_line_width(prev_line_width)
        self.next_line(self.get_y() + pb)

    def render(self, content: dict, filename: str) -> None:
        """
        Takes a content dictionary as input and applies on them the primitive building blocks
        such as texts, lines, images, boxes or tables.
        Args:
            content (dict): A dictionary containing the entire data to render into the document.
        """
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
        
        self.output(filename)

if __name__ == "__main__":
    pdf = PdfTemplateManager()
    pdf.render_text(["Hello World", "This is my very first pdf document!"])
    pdf.output("./example.pdf")