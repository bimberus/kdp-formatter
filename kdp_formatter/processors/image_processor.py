"""Image processing module for KDP formatting."""

import os
from pathlib import Path
from typing import Tuple, Optional, List
import cv2
import numpy as np
from PIL import Image, ImageOps
import cairosvg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class ImageProcessor:
    """Handles image processing and formatting according to KDP standards."""

    SUPPORTED_FORMATS = {
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'png': 'PNG',
        'tif': 'TIFF',
        'tiff': 'TIFF',
        'bmp': 'BMP',
        'gif': 'GIF',
        'svg': 'SVG',
        'webp': 'WEBP'
    }

    MIN_DPI = 300
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB KDP limit

    def __init__(self, input_file: str):
        """Initialize image processor with input file."""
        self.input_path = Path(input_file)
        self.image = None
        self._validate_input()

    def _validate_input(self) -> None:
        """Validate input file format and existence."""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
        
        if self.input_path.suffix.lower()[1:] not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image format: {self.input_path.suffix}")

    def load_image(self) -> None:
        """Load image from file."""
        if self.input_path.suffix.lower() == '.svg':
            self._load_svg()
        else:
            self.image = Image.open(self.input_path)

    def _load_svg(self) -> None:
        """Convert SVG to PNG and load it."""
        output_path = self.input_path.with_suffix('.png')
        if self.input_path.suffix.lower() == '.svg':
            cairosvg.svg2png(url=str(self.input_path), write_to=str(output_path))
            self.image = Image.open(output_path)
            os.remove(output_path)

    def check_resolution(self) -> Tuple[float, float]:
        """Check image DPI and return (x_dpi, y_dpi)."""
        if not self.image:
            self.load_image()
        
        try:
            dpi = self.image.info.get('dpi', (72, 72))
            return dpi
        except Exception:
            return (72, 72)  # Default assumption if DPI info not available

    def adjust_resolution(self, target_dpi: int = MIN_DPI) -> None:
        """Adjust image resolution to meet KDP standards."""
        if not self.image:
            self.load_image()

        current_dpi = self.check_resolution()
        if current_dpi[0] < target_dpi or current_dpi[1] < target_dpi:
            scale_factor = target_dpi / min(current_dpi)
            new_size = tuple(int(dim * scale_factor) for dim in self.image.size)
            self.image = self.image.resize(new_size, Image.Resampling.LANCZOS)
            self.image.info['dpi'] = (target_dpi, target_dpi)

    def convert_color_profile(self, to_cmyk: bool = False) -> None:
        """Convert image between RGB and CMYK color spaces."""
        if not self.image:
            self.load_image()

        if to_cmyk and self.image.mode != 'CMYK':
            self.image = self.image.convert('CMYK')
        elif not to_cmyk and self.image.mode != 'RGB':
            self.image = self.image.convert('RGB')

    def optimize_size(self, max_size: int = MAX_FILE_SIZE) -> None:
        """Optimize image size while maintaining quality."""
        if not self.image:
            self.load_image()

        quality = 95
        temp_output = self.input_path.with_suffix('.tmp.jpg')

        while quality > 50:
            self.image.save(temp_output, quality=quality, optimize=True)
            if os.path.getsize(temp_output) <= max_size:
                break
            quality -= 5

        if os.path.exists(temp_output):
            os.remove(temp_output)

    def create_coloring_page(self, edge_detection: str = 'canny') -> None:
        """Convert image to a coloring book page."""
        if not self.image:
            self.load_image()

        # Convert to grayscale
        img_array = np.array(self.image.convert('L'))

        if edge_detection == 'canny':
            edges = cv2.Canny(img_array, 100, 200)
        else:  # Sobel
            sobel_x = cv2.Sobel(img_array, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(img_array, cv2.CV_64F, 0, 1, ksize=3)
            edges = np.sqrt(sobel_x**2 + sobel_y**2)
            edges = np.uint8(edges)

        # Invert and enhance edges
        edges = 255 - edges
        edges = cv2.GaussianBlur(edges, (3, 3), 0)
        
        self.image = Image.fromarray(edges)

    def remove_background(self) -> None:
        """Remove background from image for coloring books."""
        if not self.image:
            self.load_image()

        # Convert to RGBA if not already
        if self.image.mode != 'RGBA':
            self.image = self.image.convert('RGBA')

        # Create mask using alpha channel
        mask = self.image.split()[3]
        mask = mask.point(lambda p: p > 128 and 255)
        
        # Apply mask
        self.image.putalpha(mask)

    def create_mirror_copy(self) -> 'ImageProcessor':
        """Create a mirror copy of the image for coloring books."""
        if not self.image:
            self.load_image()

        mirrored = ImageOps.mirror(self.image)
        new_processor = ImageProcessor(str(self.input_path))
        new_processor.image = mirrored
        return new_processor

    def save(self, output_path: Optional[str] = None, format: Optional[str] = None) -> str:
        """Save processed image to output file."""
        if not self.image:
            raise RuntimeError("No image loaded to save")

        if not output_path:
            suffix = format.lower() if format else self.input_path.suffix
            output_path = self.input_path.with_suffix(f'.processed{suffix}')
        else:
            output_path = Path(output_path)

        format = format or self.SUPPORTED_FORMATS.get(
            output_path.suffix.lower()[1:],
            'PNG'
        )

        self.image.save(
            output_path,
            format=format,
            quality=95,
            optimize=True,
            dpi=self.check_resolution()
        )

        return str(output_path)

    def get_image_info(self) -> dict:
        """Get information about the image."""
        if not self.image:
            self.load_image()

        return {
            'format': self.image.format,
            'mode': self.image.mode,
            'size': self.image.size,
            'dpi': self.check_resolution(),
            'file_size': os.path.getsize(self.input_path)
        }