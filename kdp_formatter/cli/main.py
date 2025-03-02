"""Command line interface for KDP formatter."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional
from ..processors.text_processor import TextProcessor
from ..processors.image_processor import ImageProcessor
from ..processors.pdf_processor import PDFProcessor

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Format books and images according to Amazon KDP standards"
    )

    parser.add_argument(
        "input",
        help="Input file or directory"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file path"
    )

    parser.add_argument(
        "--type",
        choices=["text", "image", "pdf", "coloring"],
        required=True,
        help="Type of processing to perform"
    )

    parser.add_argument(
        "--format",
        choices=["epub", "mobi", "pdf", "kpf"],
        help="Output format for text processing"
    )

    parser.add_argument(
        "--page-size",
        choices=["letter", "a4"],
        default="letter",
        help="Page size for PDF output"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Target DPI for image processing"
    )

    parser.add_argument(
        "--color-space",
        choices=["rgb", "cmyk"],
        default="rgb",
        help="Color space for image processing"
    )

    parser.add_argument(
        "--mirror-pages",
        action="store_true",
        help="Create mirror pages for coloring books"
    )

    return parser

def process_text(
    input_path: Path,
    output_path: Optional[Path],
    format: str = "epub"
) -> str:
    """Process text files according to KDP standards."""
    try:
        processor = TextProcessor(str(input_path), format)
        processor.read_content()
        processor.format_content()
        toc = processor.generate_toc()
        return processor.save(str(output_path) if output_path else None)
    except Exception as e:
        print(f"Error processing text: {e}", file=sys.stderr)
        sys.exit(1)

def process_image(
    input_path: Path,
    output_path: Optional[Path],
    target_dpi: int = 300,
    to_cmyk: bool = False
) -> str:
    """Process images according to KDP standards."""
    try:
        processor = ImageProcessor(str(input_path))
        processor.load_image()
        processor.adjust_resolution(target_dpi)
        processor.convert_color_profile(to_cmyk)
        processor.optimize_size()
        return processor.save(str(output_path) if output_path else None)
    except Exception as e:
        print(f"Error processing image: {e}", file=sys.stderr)
        sys.exit(1)

def process_coloring_page(
    input_path: Path,
    output_path: Optional[Path],
    mirror_pages: bool = False
) -> str:
    """Create coloring book pages from images."""
    try:
        processor = ImageProcessor(str(input_path))
        processor.load_image()
        processor.create_coloring_page()
        processor.optimize_size()
        
        result_path = processor.save(str(output_path) if output_path else None)
        
        if mirror_pages:
            mirror_processor = processor.create_mirror_copy()
            mirror_path = Path(result_path).with_stem(f"{Path(result_path).stem}_mirror")
            mirror_processor.save(str(mirror_path))
            
        return result_path
    except Exception as e:
        print(f"Error creating coloring page: {e}", file=sys.stderr)
        sys.exit(1)

def process_pdf(
    input_path: Path,
    output_path: Optional[Path],
    page_size: str = "letter"
) -> str:
    """Process PDF according to KDP standards."""
    try:
        processor = PDFProcessor(str(input_path))
        text_content = "\\n".join(processor.extract_text())
        
        # Extract images to temporary directory
        temp_dir = Path("temp_images")
        temp_dir.mkdir(exist_ok=True)
        images = [(path, None) for path in processor.extract_images(str(temp_dir))]
        
        # Create print-ready PDF
        result = processor.create_print_ready_pdf(
            text_content,
            images,
            str(output_path) if output_path else str(input_path.with_suffix('.kdp.pdf')),
            page_size
        )
        
        # Cleanup temporary files
        for image_path, _ in images:
            Path(image_path).unlink()
        temp_dir.rmdir()
        
        return result
    except Exception as e:
        print(f"Error processing PDF: {e}", file=sys.stderr)
        sys.exit(1)

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(args)

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        if args.type == "text":
            if not args.format:
                print("Output format is required for text processing", file=sys.stderr)
                return 1
            result = process_text(input_path, output_path, args.format)
        
        elif args.type == "image":
            result = process_image(
                input_path,
                output_path,
                args.dpi,
                args.color_space == "cmyk"
            )
        
        elif args.type == "coloring":
            result = process_coloring_page(
                input_path,
                output_path,
                args.mirror_pages
            )
        
        elif args.type == "pdf":
            result = process_pdf(
                input_path,
                output_path,
                args.page_size
            )
        
        print(f"Processing complete. Output saved to: {result}")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())