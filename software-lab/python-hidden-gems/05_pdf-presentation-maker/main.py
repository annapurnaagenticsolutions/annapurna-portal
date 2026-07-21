"""
Project 05: PDF Presentation Maker

Hidden Gem: `fpdf2` — clean, modern PDF generation without reportlab's complexity.

What it does: Generates a PDF slide deck from a simple text-based format.
Each slide has a title and bullet points. Outputs a polished presentation.
"""
from fpdf import FPDF
import os


class SlidePDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Slide {self.page_no()}", align="C")


def add_slide(pdf, title, bullets, bg_color=(240, 245, 250)):
    """Add a single slide to the PDF."""
    pdf.add_page()

    # Background
    pdf.set_fill_color(*bg_color)
    pdf.rect(0, 0, pdf.w, pdf.h, style="F")

    # Title bar
    pdf.set_fill_color(30, 60, 120)
    pdf.rect(0, 0, pdf.w, 40, style="F")

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(15, 12)
    pdf.cell(0, 20, title, align="L")

    # Bullets
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(40, 40, 40)
    y = 60
    for bullet in bullets:
        pdf.set_xy(20, y)
        pdf.cell(10, 10, "•", align="L")
        pdf.set_xy(30, y)
        pdf.multi_cell(0, 8, bullet)
        y += 20

    # Footer accent
    pdf.set_fill_color(30, 60, 120)
    pdf.rect(0, pdf.h - 10, pdf.w, 10, style="F")


def parse_slides(text):
    """Parse simple text format into slides.

    Format:
    # Slide Title
    - Bullet point 1
    - Bullet point 2
    """
    slides = []
    current_title = None
    current_bullets = []

    for line in text.strip().split("\n"):
        line = line.strip()
        if line.startswith("# "):
            if current_title:
                slides.append((current_title, current_bullets))
            current_title = line[2:]
            current_bullets = []
        elif line.startswith("- "):
            current_bullets.append(line[2:])

    if current_title:
        slides.append((current_title, current_bullets))

    return slides


SAMPLE_DECK = """
# Introduction to Hidden Gems
- Python has 400,000+ packages on PyPI
- Most developers use the same 10 packages
- This project showcases lesser-known libraries

# Why fpdf2?
- Simpler API than reportlab
- Active maintenance
- Pure Python — no C dependencies
- Unicode font support

# What We Built
- A slide deck generator from text
- Title bar with accent color
- Bullet points with wrapping
- Page numbers in footer

# Get Started
- pip install fpdf2
- Edit the slides in this script
- Run: python main.py
"""


def main():
    print("--- PDF Presentation Maker ---")
    slides = parse_slides(SAMPLE_DECK)
    print(f"Parsed {len(slides)} slides from text input.")

    pdf = SlidePDF()
    pdf.set_auto_page_break(False)

    for title, bullets in slides:
        add_slide(pdf, title, bullets)

    output = "presentation.pdf"
    try:
        pdf.output(output)
        size_kb = os.path.getsize(output) / 1024
        print(f"PDF generated: {output} ({size_kb:.1f} KB)")
        print(f"Slides: {len(slides)}")
    except Exception as e:
        print(f"Error generating PDF: {e}")


if __name__ == "__main__":
    main()
