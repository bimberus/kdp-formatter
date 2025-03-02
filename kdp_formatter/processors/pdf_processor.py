"""PDF processing module for KDP formatting."""

import os
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import PyPDF2
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import portrait, landscape

class PDFProcessor:
    """Handles PDF processing and formatting according to KDP standards."""

    SUPPORTED_PAGE_SIZES = {
        'letter': letter,
        'a4': A4
    }

    KDP_MARGINS = {
        'top': 1.0 * inch,
        'bottom': 1.0 * inch,
        'left': 0.75 * inch,
        'right': 0.75 * inch,
        'gutter': 0.125 * inch
    }

    def __init__(self, input_file: Optional[str] = None):
        """Initialize PDF processor with optional input file."""
        self.input_path = Path(input_file) if input_file else None
        self.pdf_reader = None
        self.pages = []
        self.metadata = {}
        
        if input_file:
            self._validate_input()
            self.load_pdf()

    def _validate_input(self) -> None:
        """Validate input file format and existence."""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
        
        if self.input_path.suffix.lower() != '.pdf':
            raise ValueError(f"Not a PDF file: {self.input_path}")

    def load_pdf(self) -> None:
        """Load PDF file and initialize reader."""
        with open(self.input_path, 'rb') as file:
            self.pdf_reader = PyPDF2.PdfReader(file)
            self.metadata = self.pdf_reader.metadata or {}

    def extract_text(self) -> List[str]:
        """Extract text from all pages of the PDF."""
        if not self.pdf_reader:
            raise RuntimeError("No PDF loaded")

        return [page.extract_text() for page in self.pdf_reader.pages]

    def extract_images(self, output_dir: str) -> List[str]:
        """Extract images from PDF pages and save them."""
        if not self.pdf_reader:
            raise RuntimeError("No PDF loaded")

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert PDF pages to images
        images = convert_from_path(str(self.input_path))
        saved_paths = []

        for i, image in enumerate(images):
            output_path = output_dir / f"page_{i+1}.png"
            image.save(output_path, "PNG")
            saved_paths.append(str(output_path))

        return saved_paths

    def create_print_ready_pdf(
        self,
        content: str,
        images: List[Tuple[str, Optional[str]]],
        output_path: str,
        page_size: str = 'letter',
        orientation: str = 'portrait'
    ) -> str:
        """Create a print-ready PDF with proper formatting for KDP."""
        if page_size.lower() not in self.SUPPORTED_PAGE_SIZES:
            raise ValueError(f"Unsupported page size: {page_size}")

        page_size = self.SUPPORTED_PAGE_SIZES[page_size.lower()]
        if orientation == 'landscape':
            page_size = landscape(page_size)
        else:
            page_size = portrait(page_size)

        output_path = Path(output_path)
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=page_size,
            rightMargin=self.KDP_MARGINS['right'],
            leftMargin=self.KDP_MARGINS['left'],
            topMargin=self.KDP_MARGINS['top'],
            bottomMargin=self.KDP_MARGINS['bottom']
        )

        # Create styles
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30
        )

        # Build document elements
        elements = []
        
        # Add content
        if content:
            elements.append(Paragraph(content, normal_style))
            elements.append(Spacer(1, 12))

        # Add images
        for img_path, caption in images:
            if os.path.exists(img_path):
                img = Image(img_path)
                # Scale image to fit page with margins
                available_width = page_size[0] - self.KDP_MARGINS['left'] - self.KDP_MARGINS['right']
                available_height = page_size[1] - self.KDP_MARGINS['top'] - self.KDP_MARGINS['bottom']
                img.drawHeight = min(img.drawHeight, available_height)
                img.drawWidth = min(img.drawWidth, available_width)
                elements.append(img)
                
                if caption:
                    elements.append(Spacer(1, 6))
                    elements.append(Paragraph(caption, normal_style))
                elements.append(Spacer(1, 12))

        # Build the document
        doc.build(elements)
        return str(output_path)

    def create_coloring_book(
        self,
        images: List[str],
        output_path: str,
        page_size: str = 'letter',
        include_mirror_pages: bool = False
    ) -> str:
        """Create a coloring book PDF with one image per page."""
        if page_size.lower() not in self.SUPPORTED_PAGE_SIZES:
            raise ValueError(f"Unsupported page size: {page_size}")

        output_path = Path(output_path)
        page_size = self.SUPPORTED_PAGE_SIZES[page_size.lower()]
        
        # Create PDF
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=page_size,
            rightMargin=self.KDP_MARGINS['right'],
            leftMargin=self.KDP_MARGINS['left'],
            topMargin=self.KDP_MARGINS['top'],
            bottomMargin=self.KDP_MARGINS['bottom']
        )

        elements = []
        
        for img_path in images:
            if os.path.exists(img_path):
                # Add original image
                img = Image(img_path)
                available_width = page_size[0] - self.KDP_MARGINS['left'] - self.KDP_MARGINS['right']
                available_height = page_size[1] - self.KDP_MARGINS['top'] - self.KDP_MARGINS['bottom']
                img.drawHeight = min(img.drawHeight, available_height)
                img.drawWidth = min(img.drawWidth, available_width)
                elements.append(img)
                elements.append(PageBreak())

                # Add mirror page if requested
                if include_mirror_pages:
                    img = Image(img_path)
                    img.drawHeight = min(img.drawHeight, available_height)
                    img.drawWidth = min(img.drawWidth, available_width)
                    img._image.transpose(Image.FLIP_LEFT_RIGHT)  # Mirror the image
                    elements.append(img)
                    elements.append(PageBreak())

        # Build the document
        doc.build(elements)
        return str(output_path)

    def get_pdf_info(self) -> Dict:
        """Get information about the PDF."""
        if not self.pdf_reader:
            raise RuntimeError("No PDF loaded")

        return {
            'page_count': len(self.pdf_reader.pages),
            'metadata': self.metadata,
            'file_size': os.path.getsize(self.input_path) if self.input_path else None
        }