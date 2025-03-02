# KDP Formatter

A Python tool for automatically formatting books according to Amazon Kindle Direct Publishing (KDP) standards.

## Features

- Supports multiple input formats (txt, docx, pdf, md, html, etc.)
- Handles various image formats (jpg, png, tiff, svg, etc.)
- Converts to KDP-compatible formats (EPUB, MOBI, PDF)
- Automatic text formatting according to KDP standards
- Image processing and optimization
- Special features for coloring books
- Support for both e-books and print-ready formats

## Installation

```bash
pip install -e .
```

## Requirements

- Python 3.8 or higher
- Pandoc (for document conversion)
- ImageMagick (for image processing)

## Usage

```bash
kdp-format input_file [options]
```

For detailed usage instructions and examples, see the documentation.

## Features

### Text Processing
- Automatic table of contents generation
- Header formatting
- Margin and spacing adjustment
- Page numbering
- Font compatibility checking

### Image Processing
- Resolution adjustment (300 DPI minimum)
- Format conversion
- Size optimization
- Color profile management (CMYK/RGB)
- Special coloring book features

### Output Formats
- EPUB
- MOBI (Kindle)
- Print-ready PDF
- KPF (Kindle Package Format)

## License

MIT License