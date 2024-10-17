import unittest
from unittest import skip
from pdf_template_manager import PdfTemplateManager, formats

from datetime import datetime


class TestTemplateManagerInitialization(unittest.TestCase):
    """
    Simply tests the function to set the typography.
    """
    pdf = PdfTemplateManager()

    # Check the margins of the default document
    def test_top_margin(self):
        mt, ph = formats["my"], formats["ph"]
        self.assertEqual(self.pdf.t_margin, mt+ph)

    def test_left_margin(self):
        ml = formats["mx"]
        self.assertEqual(self.pdf.l_margin, ml)

    def test_right_margin(self):
        mr = formats["mx"]
        self.assertEqual(self.pdf.r_margin, mr)

    def test_bottom_margin(self):
        mb, pf = formats["my"], formats["pf"]
        self.assertEqual(self.pdf.b_margin, mb + pf)

    # Testing the typography configurations after initializing the object
    def test_correct_font_family(self):
        self.assertEqual(self.pdf.font_family, formats["typography"]["family"].lower())
    
    def test_correct_font_style(self):
        self.assertEqual(self.pdf.font_style, formats["typography"]["style"].lower())
    
    def test_correct_font_size(self):
        self.assertEqual(self.pdf.font_size_pt, formats["typography"]["size"])

    def test_correct_font_size(self):
        self.assertEqual(self.pdf.text_color.colors255, formats["typography"]["color"])
    
    # Testing the props of the class, which uses the values for the formats
    def test_correct_height(self):
        self.assertEqual(self.pdf.HEIGHT, 297)

    def test_correct_width(self):
        self.assertEqual(self.pdf.WIDTH, 210)

    def test_correct_margin_left_and_right(self):
        self.assertEqual(self.pdf.marginX, formats["mx"])

    def test_correct_margin_top_and_bottom(self):
        self.assertEqual(self.pdf.marginY, formats["my"])

    def test_correct_padding_for_header(self):
        self.assertEqual(self.pdf.paddingHeader, formats["ph"])

    def test_correct_padding_for_footer(self):
        self.assertEqual(self.pdf.paddingFooter, formats["pf"])

    def test_correct_line_height(self):
        self.assertEqual(self.pdf.line_height, self.pdf.font_size * formats["line_height"])

    def test_correct_primary_color(self):
        self.assertEqual(self.pdf.primary_main_color, formats["primary_color"])

    def test_correct_primary_contrast_color(self):
        self.assertEqual(self.pdf.primary_contrast_text, formats["primary_contrast_color"])

    def test_correct_secondary_color(self):
        self.assertEqual(self.pdf.secondary_color, formats["secondary_color"])


class TestPdfTemplateManagerUtilities(unittest.TestCase):
    pdf = PdfTemplateManager()

    def test_setting_sepcific_font_family(self):
        family = "helvetica"
        self.pdf.set_typography(family=family)
        self.assertEqual(self.pdf.font_family, family)

    def test_setting_sepcific_font_style(self):
        style = "I"
        self.pdf.set_typography(style=style)
        self.assertEqual(self.pdf.font_style, style)

    def test_setting_sepcific_font_size(self):
        size = 16
        self.pdf.set_typography(size=size)
        self.assertEqual(self.pdf.font_size_pt, size)

    def test_setting_sepcific_font_color(self):
        color = (123, 231, 7)
        self.pdf.set_typography(color=color)
        self.assertEqual(self.pdf.text_color.colors255, color)
    
    def test_next_line(self):
        y_val = self.pdf.get_y()
        self.pdf.next_line()
        self.assertEqual(self.pdf.get_y(), y_val + self.pdf.line_height)

    def test_next_line_custom_y_val(self):
        y_val = self.pdf.get_y()
        center = self.pdf.HEIGHT / 2
        self.pdf.next_line(center)
        self.assertEqual(self.pdf.get_y(), center)
    
    @skip
    def test_merge_formats(self):
        # TODO: Test the application of formats
        new_color = (1,2,3)
        formats2 = dict(**formats)
        formats2["typography"]["color"] = new_color
        self.pdf.apply_formats(formats2)
        self.assertEqual(self.pdf.formats["typography"]["color"], new_color)

    def test_reset_draw_color_after_line_rendering(self):
        x1, x2, y1, y2 = 10, 15, 10, 10
        color = (255,0,0)
        self.pdf.render_line(x1, y1, x2, y2, color=color)
        self.assertNotEqual(self.pdf.draw_color, color)

    def test_reset_line_width_after_line_rendering(self):
        x1, x2, y1, y2 = 10, 15, 10, 10
        line_width = 2
        self.pdf.render_line(x1, y1, x2, y2, line_width=line_width)
        self.assertNotEqual(self.pdf.line_width, line_width)

    def test_set_meta_data_title(self):
        title = "My Document"
        self.pdf.set_meta_data(title=title)
        self.assertEqual(self.pdf.title, title)

    def test_set_meta_data_author(self):
        author = "John Doe"
        self.pdf.set_meta_data(author=author)
        self.assertEqual(self.pdf.author, author)

    def test_set_meta_data_subject(self):
        subject = "Demo"
        self.pdf.set_meta_data(subject=subject)
        self.assertEqual(self.pdf.subject, subject)

    def test_set_meta_data_creator(self):
        creator = "Jane Doe"
        self.pdf.set_meta_data(creator=creator)
        self.assertEqual(self.pdf.creator, creator)

    @skip
    def test_set_meta_data_date(self):
        # TODO: Fix the testing for the date
        date = datetime.now()
        self.pdf.set_meta_data()
        self.assertAlmostEqual(self.pdf.creation_date, date)
