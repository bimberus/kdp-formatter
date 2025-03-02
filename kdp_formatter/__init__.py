"""KDP Formatter - A tool for formatting books according to Amazon KDP standards."""

__version__ = "0.1.0"

from .processors.text_processor import TextProcessor
from .processors.image_processor import ImageProcessor
from .processors.pdf_processor import PDFProcessor
from .cli.main import main

__all__ = ['TextProcessor', 'ImageProcessor', 'PDFProcessor', 'main']