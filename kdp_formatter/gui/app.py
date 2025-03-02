"""GUI interface for KDP formatter."""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from threading import Thread
import queue

from ..processors.text_processor import TextProcessor
from ..processors.image_processor import ImageProcessor
from ..processors.pdf_processor import PDFProcessor

class KDPFormatterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KDP Formatter")
        self.root.geometry("800x600")
        
        # Status queue for communication between processing thread and GUI
        self.status_queue = queue.Queue()
        
        self._create_widgets()
        self._setup_layout()
        self._configure_styles()
        
        # Start monitoring the status queue
        self.root.after(100, self._check_status_queue)

    def _create_widgets(self):
        """Create all GUI widgets."""
        # Input file section
        self.input_frame = ttk.LabelFrame(self.root, text="Plik wejściowy", padding="10")
        self.input_path = tk.StringVar()
        self.input_entry = ttk.Entry(self.input_frame, textvariable=self.input_path, width=50)
        self.browse_btn = ttk.Button(self.input_frame, text="Przeglądaj...", command=self._browse_input)

        # Processing options
        self.options_frame = ttk.LabelFrame(self.root, text="Opcje przetwarzania", padding="10")
        
        # Process type selection
        self.type_var = tk.StringVar(value="text")
        self.type_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.type_frame, text="Typ przetwarzania:").pack(side=tk.LEFT)
        for text, value in [
            ("Tekst", "text"),
            ("Obraz", "image"),
            ("PDF", "pdf"),
            ("Kolorowanka", "coloring")
        ]:
            ttk.Radiobutton(self.type_frame, text=text, value=value, 
                           variable=self.type_var, command=self._update_options).pack(side=tk.LEFT, padx=5)

        # Format options (for text processing)
        self.format_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.format_frame, text="Format wyjściowy:").pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value="epub")
        self.format_combo = ttk.Combobox(self.format_frame, textvariable=self.format_var,
                                       values=["epub", "pdf", "mobi"], state="readonly")
        self.format_combo.pack(side=tk.LEFT, padx=5)

        # Image options
        self.image_frame = ttk.Frame(self.options_frame)
        # DPI
        ttk.Label(self.image_frame, text="DPI:").pack(side=tk.LEFT)
        self.dpi_var = tk.StringVar(value="300")
        self.dpi_entry = ttk.Entry(self.image_frame, textvariable=self.dpi_var, width=5)
        self.dpi_entry.pack(side=tk.LEFT, padx=5)
        # Color space
        ttk.Label(self.image_frame, text="Przestrzeń kolorów:").pack(side=tk.LEFT, padx=5)
        self.color_var = tk.StringVar(value="rgb")
        self.color_combo = ttk.Combobox(self.image_frame, textvariable=self.color_var,
                                      values=["rgb", "cmyk"], state="readonly")
        self.color_combo.pack(side=tk.LEFT, padx=5)
        # Mirror pages option
        self.mirror_var = tk.BooleanVar(value=False)
        self.mirror_check = ttk.Checkbutton(self.image_frame, text="Strony lustrzane",
                                          variable=self.mirror_var)
        self.mirror_check.pack(side=tk.LEFT, padx=5)

        # PDF options
        self.pdf_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.pdf_frame, text="Rozmiar strony:").pack(side=tk.LEFT)
        self.page_size_var = tk.StringVar(value="letter")
        self.page_size_combo = ttk.Combobox(self.pdf_frame, textvariable=self.page_size_var,
                                          values=["letter", "a4"], state="readonly")
        self.page_size_combo.pack(side=tk.LEFT, padx=5)

        # Output file section
        self.output_frame = ttk.LabelFrame(self.root, text="Plik wyjściowy", padding="10")
        self.output_path = tk.StringVar()
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_path, width=50)
        self.save_btn = ttk.Button(self.output_frame, text="Zapisz jako...", 
                                 command=self._browse_output)

        # Progress section
        self.progress_frame = ttk.LabelFrame(self.root, text="Postęp", padding="10")
        self.status_var = tk.StringVar(value="Gotowy do przetwarzania")
        self.status_label = ttk.Label(self.progress_frame, textvariable=self.status_var)
        self.progress = ttk.Progressbar(self.progress_frame, mode='indeterminate')

        # Process button
        self.process_btn = ttk.Button(self.root, text="Rozpocznij przetwarzanie",
                                    command=self._start_processing)

    def _setup_layout(self):
        """Arrange widgets in the window."""
        # Input section
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.browse_btn.pack(side=tk.LEFT, padx=5)

        # Options section
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        self.type_frame.pack(fill=tk.X, pady=5)
        self.format_frame.pack(fill=tk.X, pady=5)
        self.image_frame.pack(fill=tk.X, pady=5)
        self.pdf_frame.pack(fill=tk.X, pady=5)

        # Output section
        self.output_frame.pack(fill=tk.X, padx=10, pady=5)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # Progress section
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        self.status_label.pack(fill=tk.X, padx=5, pady=5)
        self.progress.pack(fill=tk.X, padx=5, pady=5)

        # Process button
        self.process_btn.pack(pady=10)

        self._update_options()

    def _configure_styles(self):
        """Configure widget styles."""
        style = ttk.Style()
        style.configure('TLabelframe', padding=5)
        style.configure('TButton', padding=5)

    def _update_options(self):
        """Show/hide options based on selected processing type."""
        process_type = self.type_var.get()
        
        # Hide all option frames first
        for frame in [self.format_frame, self.image_frame, self.pdf_frame]:
            for widget in frame.winfo_children():
                widget.pack_forget()
            frame.pack_forget()

        # Show relevant options
        if process_type == "text":
            self.format_frame.pack(fill=tk.X, pady=5)
            for widget in self.format_frame.winfo_children():
                widget.pack(side=tk.LEFT, padx=5)
        
        elif process_type in ["image", "coloring"]:
            self.image_frame.pack(fill=tk.X, pady=5)
            for widget in self.image_frame.winfo_children():
                widget.pack(side=tk.LEFT, padx=5)
            
            # Only show mirror option for coloring
            self.mirror_check.pack_forget()
            if process_type == "coloring":
                self.mirror_check.pack(side=tk.LEFT, padx=5)
        
        elif process_type == "pdf":
            self.pdf_frame.pack(fill=tk.X, pady=5)
            for widget in self.pdf_frame.winfo_children():
                widget.pack(side=tk.LEFT, padx=5)

    def _browse_input(self):
        """Open file dialog for input file selection."""
        filetypes = []
        process_type = self.type_var.get()
        
        if process_type == "text":
            filetypes = [
                ("Wszystkie obsługiwane", "*.txt;*.docx;*.doc;*.md;*.html;*.htm;*.rtf;*.odt"),
                ("Dokumenty tekstowe", "*.txt"),
                ("Dokumenty Word", "*.docx;*.doc"),
                ("Markdown", "*.md"),
                ("HTML", "*.html;*.htm"),
                ("Rich Text", "*.rtf"),
                ("OpenDocument", "*.odt")
            ]
        elif process_type in ["image", "coloring"]:
            filetypes = [
                ("Wszystkie obrazy", "*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp;*.gif;*.svg"),
                ("JPEG", "*.jpg;*.jpeg"),
                ("PNG", "*.png"),
                ("TIFF", "*.tif;*.tiff"),
                ("BMP", "*.bmp"),
                ("GIF", "*.gif"),
                ("SVG", "*.svg")
            ]
        elif process_type == "pdf":
            filetypes = [("PDF", "*.pdf")]
        
        filetypes.append(("Wszystkie pliki", "*.*"))
        
        filename = filedialog.askopenfilename(
            title="Wybierz plik wejściowy",
            filetypes=filetypes
        )
        
        if filename:
            self.input_path.set(filename)
            # Auto-suggest output filename
            if not self.output_path.get():
                input_path = Path(filename)
                process_type = self.type_var.get()
                
                if process_type == "text":
                    output_ext = f".{self.format_var.get()}"
                elif process_type in ["image", "coloring"]:
                    output_ext = input_path.suffix
                else:
                    output_ext = ".pdf"
                
                output_path = input_path.with_suffix(f".kdp{output_ext}")
                self.output_path.set(str(output_path))

    def _browse_output(self):
        """Open file dialog for output file selection."""
        process_type = self.type_var.get()
        
        if process_type == "text":
            filetypes = [
                (f"{self.format_var.get().upper()}", f"*.{self.format_var.get()}")
            ]
        elif process_type in ["image", "coloring"]:
            filetypes = [
                ("JPEG", "*.jpg;*.jpeg"),
                ("PNG", "*.png"),
                ("TIFF", "*.tif;*.tiff")
            ]
        else:
            filetypes = [("PDF", "*.pdf")]
        
        filename = filedialog.asksaveasfilename(
            title="Zapisz jako",
            filetypes=filetypes,
            defaultextension=filetypes[0][1].split('.')[-1]
        )
        
        if filename:
            self.output_path.set(filename)

    def _update_status(self, message, is_error=False):
        """Update status label and optionally show error message."""
        self.status_queue.put((message, is_error))

    def _check_status_queue(self):
        """Check for status updates from the processing thread."""
        try:
            while True:
                message, is_error = self.status_queue.get_nowait()
                self.status_var.set(message)
                if is_error:
                    messagebox.showerror("Błąd", message)
                    self.progress.stop()
                    self.progress.pack_forget()
                    self.process_btn.configure(state='normal')
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._check_status_queue)

    def _start_processing(self):
        """Start the processing thread."""
        if not self.input_path.get():
            messagebox.showwarning("Ostrzeżenie", "Wybierz plik wejściowy!")
            return
        
        if not self.output_path.get():
            messagebox.showwarning("Ostrzeżenie", "Wybierz plik wyjściowy!")
            return

        self.process_btn.configure(state='disabled')
        self.progress.pack(fill=tk.X, padx=5, pady=5)
        self.progress.start()
        
        thread = Thread(target=self._process_file)
        thread.daemon = True
        thread.start()

    def _process_file(self):
        """Process the file in a separate thread."""
        try:
            process_type = self.type_var.get()
            input_path = self.input_path.get()
            output_path = self.output_path.get()

            self._update_status("Rozpoczynam przetwarzanie...")

            if process_type == "text":
                self._update_status("Przetwarzanie tekstu...")
                processor = TextProcessor(input_path, self.format_var.get())
                processor.read_content()
                processor.format_content()
                processor.generate_toc()
                processor.save(output_path)

            elif process_type == "image":
                self._update_status("Przetwarzanie obrazu...")
                processor = ImageProcessor(input_path)
                processor.load_image()
                processor.adjust_resolution(int(self.dpi_var.get()))
                processor.convert_color_profile(self.color_var.get() == "cmyk")
                processor.optimize_size()
                processor.save(output_path)

            elif process_type == "coloring":
                self._update_status("Tworzenie kolorowanki...")
                processor = ImageProcessor(input_path)
                processor.load_image()
                processor.create_coloring_page()
                processor.save(output_path)
                
                if self.mirror_var.get():
                    self._update_status("Tworzenie lustrzanej kopii...")
                    mirror_path = Path(output_path)
                    mirror_path = mirror_path.with_stem(f"{mirror_path.stem}_mirror")
                    processor.create_mirror_copy().save(str(mirror_path))

            elif process_type == "pdf":
                self._update_status("Przetwarzanie PDF...")
                processor = PDFProcessor(input_path)
                # Extract content
                self._update_status("Wydobywanie tekstu...")
                text_content = processor.extract_text()
                
                # Extract images to temporary directory
                self._update_status("Wydobywanie obrazów...")
                temp_dir = Path("temp_images")
                temp_dir.mkdir(exist_ok=True)
                images = [(path, None) for path in processor.extract_images(str(temp_dir))]
                
                # Create print-ready PDF
                self._update_status("Tworzenie PDF...")
                processor.create_print_ready_pdf(
                    "\n".join(text_content),
                    images,
                    output_path,
                    self.page_size_var.get()
                )
                
                # Cleanup
                for image_path, _ in images:
                    Path(image_path).unlink()
                temp_dir.rmdir()

            self._update_status("Przetwarzanie zakończone pomyślnie!")
            messagebox.showinfo("Sukces", "Plik został pomyślnie przetworzony!")

        except Exception as e:
            self._update_status(f"Błąd: {str(e)}", is_error=True)
        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.process_btn.configure(state='normal')

def main():
    """Start the GUI application."""
    root = tk.Tk()
    app = KDPFormatterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()