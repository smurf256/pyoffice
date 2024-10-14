import os

from typing import Literal
from fpdf import FPDF, FontFace, XPos, YPos
from fpdf.enums import VAlign
from lib.colors import TailwindColors

# Bullet point seperator
BULLETPOINT_SEPERATOR = "•"

class PdfTemplate(FPDF):
    """
    Set the margin of the document.
    Set, where we want to have the page numbers.
    Set auto page break
    """
    def __init__(self, orientation: Literal[''] | Literal['portrait'] | Literal['p'] | Literal['P'] | Literal['landscape'] | Literal['l'] | Literal['L'] = "portrait", unit: float | Literal['pt'] | Literal['mm'] | Literal['cm'] | Literal['in'] = "mm", format: tuple[float, float] | Literal[''] | Literal['a3'] | Literal['A3'] | Literal['a4'] | Literal['A4'] | Literal['a5'] | Literal['A5'] | Literal['letter'] | Literal['Letter'] | Literal['legal'] | Literal['Legal'] = "A4", font_cache_dir: Literal['DEPRECATED'] = "DEPRECATED") -> None:
        super().__init__(orientation, unit, format, font_cache_dir)
        self.load_fonts()
        self.set_font("Roboto")
        # Set the default values for pdf files
        self.marginX = 23
        self.marginY = 10
        self.set_margin(self.marginY)
        self.set_left_margin(self.marginX)
        self.set_right_margin(self.marginX)
         # Default values for the margin after the header
        # and before the footer
        self.marginHeader = 20
        self.marginFooter = 20
        # Set the values for the fold marks
        self.default_first_foldmark = 99
        self.default_second_foldmark = 198
        # Setting the font configs
        self.default_font_style = ""
        self.default_font_size = 9
        self.default_font_color = TailwindColors.SLATE_800.value
        self.set_font_configs(size=self.default_font_size, color=self.default_font_color)
        self.add_page()
        # TODO: Determine which threshold might be useful.
        # https://py-pdf.github.io/fpdf2/fpdf/fpdf.html#fpdf.fpdf.FPDF.set_auto_page_break
        self.set_auto_page_break(auto=True, margin=self.marginY + self.marginFooter)

    def header(self) -> None:
        # TODO: Built-in function and override it
        if self.page_no() == 1:
            self.fold_marks()
        # Always call the folding marks
        # self.add_fold_marks()
        # self.set_top_margin(self.marginY)
        # self.set_left_margin(self.marginX)
        # self.set_right_margin(self.marginX)

    def footer(self) -> None:
        """
        Overrides the built-in function `footer` and allows to add
        customized content to the end of the page.
        Per default, it shows the current page number.
        """
        # TODO: Add logic to decide, which pages should include page numbers.
        y_val = self.HEIGHT - (self.marginY)
        self.set_y(y_val)
        self.set_font_configs(size=self.default_font_size - 2, color=TailwindColors.GRAY_500.value)
        self.cell(center=True, text=f"Seite {self.page_no()} von {{nb}}")
        self.reset_font_configs()

    def set_default_configs(self) -> None:
        """
        This function is called after creating a new pdf document.
        We initialize some values regarding to appearance of the document.
        """
        # Set the default values for pdf files
        self.marginX = 23
        self.marginY = 10
        self.set_margin(self.marginY)
        self.set_left_margin(self.marginX)
        self.set_right_margin(self.marginX)
        # Default values for the margin after the header
        # and before the footer
        self.marginHeader = 20
        self.marginFooter = 20
        # Boolean flag, whether the current page number should be displayed on each page.
        self.page_no_on_each_page: bool = False

    @property
    def HEIGHT(self) -> int:
        # Normalized height of DIN4 pages.
        return 297
    
    @property
    def WIDTH(self) -> int:
        # Normalized width of DIN4 pages.
        return 210
    
    @property
    def line_height(self) -> float:
        return self.font_size * 1.4
    
    def load_fonts(self) -> None:
        """ Loading fonts to allow custom usage of them. """
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

    def next_line(self, new_y: float|None=None) -> None:
        """
        Takes an optional value to set the values for the next 
        line in the pdf document.
        If not given, use the default values for the line_height.
        The x value is also given and is always set to be the marginX value.
        """
        if new_y is not None:
            self.set_xy(self.l_margin, new_y)
        else:
            self.set_xy(self.l_margin, self.get_y() + self.line_height)

    def fold_marks(self) -> None:
        """
        Provides the folding marks for a pdf document to make it 
        ready for mail.
        TODO: Allow configs such as: all three, only first and middle or only top.
        TODO: Either make the fold marks starting at the left border directly or with padding of 1.1cm.
        """
        left_padding = 3
        fold_positions: list = [99, 198]    # practical values for the fold marks
        middle_mark: float = self.HEIGHT / 2
        self.set_draw_color(TailwindColors.SLATE_900.value)
        prev_line_width = self.line_width
        self.set_line_width(.1)
        for y in fold_positions:
            self.line(left_padding, y, left_padding + 4, y)
        # Adding the mark for the middle of the page
        self.line(left_padding, middle_mark, left_padding + 6, middle_mark)
        self.set_line_width(prev_line_width)

    def render_text(
            self, 
            lines: list, 
            x: float|None=None, 
            y: float|None=None, 
            w: float=0, 
            align: str="L",
            font_family: str|None=None,
            font_style: str|None=None,
            font_size: int|None=None,
            font_color: tuple=None
        ) -> None:
        """
        This function provides an interface to render text.
        Leverages the built in function `multicell`.
        For more information, checkout the documentation:
        https://py-pdf.github.io/fpdf2/Text.html#multi_cell
        """
        if font_style is None:
            font_style = ""
        if font_size is None:
            font_size = self.default_font_size
        if font_color is None:
            font_color = self.default_font_color
        self.set_font_configs(family=font_family, style=font_style, size=font_size, color=font_color)
        if x is not None or y is not None:
            x = x if x is not None else self.get_x()
            y = y if y is not None else self.get_y()
            self.set_xy(x,y)
        # Use font configs
        for ln in lines:
            self.multi_cell(w=w, h=self.line_height, text=ln, new_x=XPos.LEFT, new_y=YPos.NEXT, align=align)
        self.next_line()
        self.reset_font_configs()

    def render_signature_area(
            self, 
            w:int=60,
            x:float|None=None,
            y:float|None=None, 
            text:str|None=None,
            line_width:float|None=None,
            line_color:tuple|None=None,
            ) -> None:
        """
        Renders a block to leave a signature on the document.
        Below the signature line, there will also be rendered a text.
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
        
        

    def set_font_configs(self, family: str|None=None, style:str="", size: int|None=None, color: tuple|None=None) -> None:
        """
        Here, we can set the configs for the font including the font family, the style of the font
        the size and the color of the text.
        Note that the font needs to be installed / loaded, before using it.
        Args:
            family (str|None): The familiy we want to use.
            style (str|None): The style choosing between italic, bold and regular|default.
            size (int): The size we want to use.
            color (tuple): Set the color of the font.
        """
        if color is not None:
            self.set_text_color(*color)
        if size is None:
            size = self.default_font_size
        self.set_font(family=family,style=style, size=size)

    def reset_font_configs(self) -> None:
        """ Resets the font settings. """
        self.set_font_configs(style=self.default_font_style, size=self.default_font_size, color=self.default_font_color)

    def render_table(
            self, 
            items: list,
            num_of_row_filled:int=-1,
            row_fill_color:tuple|None=None,
            **kwargs
            ) -> None:
        """
        Renders a table and utilizes the built-in table.
        For the tables, checkout important resources for handling the 
            Table Border Layout: 
            https://py-pdf.github.io/fpdf2/fpdf/enums.html#fpdf.enums.TableBordersLayout

            Tables:
            https://py-pdf.github.io/fpdf2/Tables.html
        Args:
            items (list): List of all data items and the heading is the very first row.
            num_of_row_filled (int): The index of the row we want to fill entirely. Default set to -1.
            row_fill_color (tuple): The color we want to fill the desired row with.
            kwargs: The optional parameters for the fpdf2 table. 
        """
        # Adding a bottom line 
        # self.set_draw_color(TailwindColors.GRAY_200.value)
        # prev_line_width = self.line_height
        # self.set_line_width(.5)
        with self.table(
            line_height=self.line_height,   # using the customized line height of this class
            # borders_layout="NONE",   # only apply with the border bottom after the heading
            v_align=VAlign.T,
            # Add color for every second row
            # cell_fill_color=TailwindColors.GRAY_50.value, 
            # cell_fill_mode="ROWS",
            # gutter_height=2,
            **kwargs
        ) as table:
            # Set the correct values for the data items inside the table
            self.set_font_configs(color=TailwindColors.SLATE_700.value)
            for index, data_row in enumerate(items):
                row = table.row()
                fill_color = self.fill_color
                for datum in data_row:
                    if row_fill_color is not None and num_of_row_filled == index and len(datum) > 0:
                        self.set_fill_color(row_fill_color)
                        self.set_font_configs(style="B")
                    row.cell(datum)
                    if row_fill_color is not None and num_of_row_filled == index and len(datum) > 0:
                        self.set_fill_color(fill_color)
                        self.set_font_configs(style="", color=self.default_font_color)
        # self.set_line_width(prev_line_width)