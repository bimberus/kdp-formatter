"""KDP Formatter - A tool for formatting books according to Amazon KDP standards."""

__version__ = "0.1.0"

from .processors.text_processor import TextProcessor
from .processors.image_processor import ImageProcessor
from .processors.pdf_processor import PDFProcessor
from .cli.main import main as cli_main
from .gui.app import main as gui_main

def main(use_gui=True):
    """Launch KDP Formatter.
    
    Args:
        use_gui (bool): If True, launches GUI interface, otherwise launches CLI.
    """
    if use_gui:
        gui_main()
    else:
        cli_main()

__all__ = [
    'TextProcessor',
    'ImageProcessor',
    'PDFProcessor',
    'main',
    'cli_main',
    'gui_main'
]