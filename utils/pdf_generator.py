"""Utility to generate simple PDF files."""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_pdf(lines: list[str], path: str) -> None:
    """Generate a basic PDF document with the provided text lines."""
    c = canvas.Canvas(path, pagesize=A4)
    y = A4[1] - 50
    for line in lines:
        c.drawString(50, y, line)
        y -= 20
    c.save()
