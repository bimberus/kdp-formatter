"""Text processing module for KDP formatting."""

import os
from pathlib import Path
from typing import Dict, List, Optional
import pypandoc
from docx import Document
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
import PyPDF2

class TextProcessor:
    """Handles text processing and formatting according to KDP standards."""

    SUPPORTED_FORMATS = {
        'txt': 'text',
        'docx': 'docx',
        'doc': 'doc',
        'md': 'markdown',
        'html': 'html',
        'htm': 'html',
        'rtf': 'rtf',
        'odt': 'odt',
        'epub': 'epub',
        'pdf': 'pdf'  # Added PDF support
    }

    KDP_MARGINS = {
        'top': 1.0,  # inches
        'bottom': 1.0,
        'left': 0.75,
        'right': 0.75,
        'gutter': 0.125
    }

    def __init__(self, input_file: str, output_format: str = 'epub'):
        """Initialize text processor with input file and desired output format."""
        self.input_path = Path(input_file)
        self.output_format = output_format
        self.content = None
        self.metadata = {}
        self._validate_input()

    def _validate_input(self) -> None:
        """Validate input file format and existence."""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
        
        if self.input_path.suffix.lower()[1:] not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported input format: {self.input_path.suffix}")

    def read_content(self) -> None:
        """Read content from input file based on its format."""
        input_format = self.SUPPORTED_FORMATS[self.input_path.suffix.lower()[1:]]
        
        if input_format == 'epub':
            self._read_epub()
        elif input_format == 'pdf':
            self._read_pdf()
        else:
            try:
                self.content = pypandoc.convert_file(
                    str(self.input_path),
                    'html',
                    format=input_format
                )
            except Exception as e:
                raise RuntimeError(f"Error converting file: {e}")

    def _read_epub(self) -> None:
        """Read content from EPUB file."""
        book = epub.read_epub(str(self.input_path))
        content_parts = []
        
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content_parts.append(item.get_content().decode('utf-8'))
        
        self.content = '\n'.join(content_parts)
        self.metadata = book.get_metadata('DC', {})

    def _read_pdf(self) -> None:
        """Read content from PDF file."""
        with open(self.input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content_parts = []
            
            # Extract text from each page
            for page in reader.pages:
                content_parts.append(page.extract_text())
            
            self.content = '\n'.join(content_parts)
            
            # Get metadata if available
            self.metadata = reader.metadata if reader.metadata else {}

            # Convert content to HTML format for consistent processing
            self.content = f"<html><body>{self.content}</body></html>"

    def format_content(self) -> None:
        """Apply KDP formatting standards to content."""
        if not self.content:
            self.read_content()

        soup = BeautifulSoup(self.content, 'html.parser')
        self._format_headings(soup)
        self._format_paragraphs(soup)
        self._format_lists(soup)
        self.content = str(soup)

    def _format_headings(self, soup: BeautifulSoup) -> None:
        """Format headings according to KDP standards."""
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                heading['class'] = heading.get('class', []) + [f'kdp-h{i}']

    def _format_paragraphs(self, soup: BeautifulSoup) -> None:
        """Format paragraphs according to KDP standards."""
        for p in soup.find_all('p'):
            p['class'] = p.get('class', []) + ['kdp-paragraph']

    def _format_lists(self, soup: BeautifulSoup) -> None:
        """Format lists according to KDP standards."""
        for list_tag in soup.find_all(['ul', 'ol']):
            list_tag['class'] = list_tag.get('class', []) + ['kdp-list']

    def generate_toc(self) -> List[Dict[str, str]]:
        """Generate table of contents from content."""
        if not self.content:
            self.read_content()

        soup = BeautifulSoup(self.content, 'html.parser')
        toc = []

        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(heading.name[1])
            toc.append({
                'title': heading.get_text(),
                'level': level,
                'id': heading.get('id', f'heading_{len(toc)}')
            })
            if not heading.get('id'):
                heading['id'] = toc[-1]['id']

        return toc

    def save(self, output_path: Optional[str] = None) -> str:
        """Save formatted content to output file."""
        if not output_path:
            output_path = self.input_path.with_suffix(f'.kdp.{self.output_format}')
        else:
            output_path = Path(output_path)

        if self.output_format == 'epub':
            self._save_epub(output_path)
        else:
            pypandoc.convert_text(
                self.content,
                self.output_format,
                format='html',
                outputfile=str(output_path),
                extra_args=['--toc', '--toc-depth=3']
            )

        return str(output_path)

    def _save_epub(self, output_path: Path) -> None:
        """Save content as EPUB file."""
        book = epub.EpubBook()
        
        # Set metadata
        book.set_title(self.metadata.get('title', ['Untitled'])[0][0] if isinstance(self.metadata.get('title', []), list) else 'Untitled')
        book.set_language('en')
        
        # Create chapters
        soup = BeautifulSoup(self.content, 'html.parser')
        sections = soup.find_all(['h1', 'h2', 'p'])
        
        if not sections:
            # If no sections found, create a single chapter
            chapter = epub.EpubHtml(
                title='Chapter 1',
                file_name='chap_1.xhtml',
                content=self.content
            )
            book.add_item(chapter)
            book.toc = [(epub.Section('Chapter 1'), chapter)]
            book.spine = ['nav', chapter]
        else:
            # Create chapters based on sections
            current_chapter = []
            chapters = []
            chapter_count = 0
            
            for section in sections:
                if section.name in ['h1', 'h2']:
                    # Save previous chapter if exists
                    if current_chapter:
                        chapter_count += 1
                        chapter = epub.EpubHtml(
                            title=current_chapter[0].get_text(),
                            file_name=f'chap_{chapter_count}.xhtml',
                            content=''.join(str(tag) for tag in current_chapter)
                        )
                        book.add_item(chapter)
                        chapters.append(chapter)
                        current_chapter = []
                
                current_chapter.append(section)
            
            # Add last chapter
            if current_chapter:
                chapter_count += 1
                chapter = epub.EpubHtml(
                    title=current_chapter[0].get_text() if current_chapter[0].name in ['h1', 'h2'] else f'Chapter {chapter_count}',
                    file_name=f'chap_{chapter_count}.xhtml',
                    content=''.join(str(tag) for tag in current_chapter)
                )
                book.add_item(chapter)
                chapters.append(chapter)
            
            # Add navigation
            book.toc = [(epub.Section(chapter.title), chapter) for chapter in chapters]
            book.spine = ['nav'] + chapters

        # Add required elements
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # Write epub
        epub.write_epub(str(output_path), book)