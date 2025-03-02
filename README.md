# KDP Formatter

Narzędzie do automatycznego formatowania książek zgodnie ze standardami Amazon Kindle Direct Publishing (KDP).

## Szczegółowa instrukcja instalacji i użytkowania

### 1. Wymagania wstępne

Przed rozpoczęciem upewnij się, że masz zainstalowane:

1. Python 3.8 lub nowszy
   - Sprawdź czy masz Python: Otwórz terminal i wpisz `python --version`
   - Jeśli nie masz, pobierz z [python.org](https://www.python.org/downloads/)

2. Pandoc
   - Windows: [Pobierz instalator](https://github.com/jgm/pandoc/releases/latest)
   - Linux: `sudo apt-get install pandoc`
   - macOS: `brew install pandoc`

3. ImageMagick
   - Windows: [Pobierz instalator](https://imagemagick.org/script/download.php#windows)
   - Linux: `sudo apt-get install imagemagick`
   - macOS: `brew install imagemagick`

### 2. Instalacja programu

1. Pobierz program:
   - Kliknij zielony przycisk "Code" na [stronie projektu](https://github.com/bimberus/kdp-formatter)
   - Wybierz "Download ZIP"
   - Rozpakuj pobrany plik

2. Otwórz terminal/wiersz poleceń:
   - Windows: Wyszukaj "cmd" lub "PowerShell"
   - macOS/Linux: Otwórz Terminal

3. Przejdź do katalogu z programem:
   ```bash
   cd ścieżka/do/kdp-formatter
   ```

4. Stwórz wirtualne środowisko Python (opcjonalnie, ale zalecane):
   ```bash
   python -m venv kdp-venv
   ```

   Aktywuj środowisko:
   - Windows:
     ```bash
     kdp-venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source kdp-venv/bin/activate
     ```

5. Zainstaluj wymagane biblioteki:

   **WAŻNE**: W przypadku problemów z połączeniem internetowym podczas instalacji:

   a) Najpierw zaktualizuj pip:
   ```bash
   python -m pip install --upgrade pip
   ```

   b) Ustaw zaufane hosty dla pip:
   ```bash
   pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"
   ```

   c) Następnie zainstaluj wymagania:
   ```bash
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
   pip install -e .
   ```

### 3. Jak używać - przykłady

#### A. Formatowanie dokumentu tekstowego do e-booka

1. Przygotuj dokument (np. w Wordzie) i zapisz go
2. Otwórz terminal
3. Wpisz komendę:
   ```bash
   kdp-format "C:\Users\TwojaNazwa\Documents\mojaksiezka.docx" --type text --format epub --output "C:\Users\TwojaNazwa\Documents\gotowa_ksiazka.epub"
   ```

#### B. Tworzenie kolorowanki

1. Przygotuj obrazek
2. Wykonaj konwersję:
   ```bash
   kdp-format "C:\Users\TwojaNazwa\Pictures\rysunek.png" --type coloring --mirror-pages --output "C:\Users\TwojaNazwa\Pictures\kolorowanka.png"
   ```

#### C. Przygotowanie okładki książki

1. Przygotuj grafikę okładki
2. Dostosuj do wymagań KDP:
   ```bash
   kdp-format "C:\Users\TwojaNazwa\Pictures\okladka.jpg" --type image --dpi 300 --color-space cmyk --output "C:\Users\TwojaNazwa\Pictures\okladka_kdp.jpg"
   ```

#### D. Przygotowanie PDF do druku

1. Mając gotowy PDF:
   ```bash
   kdp-format "C:\Users\TwojaNazwa\Documents\ksiazka.pdf" --type pdf --page-size letter --output "C:\Users\TwojaNazwa\Documents\ksiazka_do_druku.pdf"
   ```

### 4. Najważniejsze opcje

- `--type`: Rodzaj przetwarzania
  - `text` - dla dokumentów tekstowych
  - `image` - dla obrazów
  - `pdf` - dla plików PDF
  - `coloring` - do tworzenia kolorowanek

- `--format`: Format wyjściowy dla dokumentów tekstowych
  - `epub` - dla e-booków
  - `pdf` - dla wydań drukowanych
  - `mobi` - dla Kindle

- `--dpi`: Rozdzielczość obrazów (minimum 300 dla KDP)

- `--color-space`: Przestrzeń kolorów
  - `rgb` - dla e-booków
  - `cmyk` - dla druku

- `--page-size`: Rozmiar strony
  - `letter` - format amerykański
  - `a4` - format europejski

### 5. Rozwiązywanie problemów

1. Problemy z instalacją pakietów (pip):
   - Sprawdź połączenie internetowe
   - Wykonaj kroki instalacji z punktu 2.5 (trusted-host)
   - Spróbuj użyć innego połączenia internetowego
   - Jeśli używasz proxy, ustaw zmienne środowiskowe:
     ```bash
     export HTTP_PROXY="http://proxy:port"
     export HTTPS_PROXY="https://proxy:port"
     ```

2. Jeśli pojawia się błąd "command not found":
   - Windows: Upewnij się, że Python jest w PATH
   - Sprawdź czy środowisko wirtualne jest aktywowane
   - Spróbuj użyć `python -m kdp_formatter` zamiast `kdp-format`

3. Problemy z konwersją obrazów:
   - Sprawdź czy ImageMagick jest zainstalowany
   - Upewnij się, że masz prawa do zapisu w katalogu docelowym
   - Dla Windows: Dodaj ImageMagick do PATH

4. Problem z formatowaniem tekstu:
   - Sprawdź czy Pandoc jest zainstalowany
   - Upewnij się, że dokument źródłowy nie jest uszkodzony
   - Sprawdź czy masz wystarczająco miejsca na dysku

### 6. Wsparcie

Jeśli napotkasz problemy:
1. Sprawdź sekcję "Issues" na GitHubie
2. Utwórz nowe zgłoszenie, opisując dokładnie problem
3. Dołącz informacje o:
   - Systemie operacyjnym
   - Użytych komendach
   - Pełnej treści błędu
   - Krokach, które doprowadziły do błędu

### 7. Przykładowy workflow

1. Przygotowanie książki:
   ```bash
   # Konwersja tekstu do formatu KDP
   kdp-format "ksiazka.docx" --type text --format epub

   # Przygotowanie okładki
   kdp-format "okladka.png" --type image --dpi 300 --color-space cmyk

   # Generowanie wersji do druku
   kdp-format "ksiazka.pdf" --type pdf --page-size letter
   ```

2. Przygotowanie kolorowanki:
   ```bash
   # Konwersja obrazów na kolorowanki
   kdp-format "obrazek1.png" --type coloring --mirror-pages
   kdp-format "obrazek2.png" --type coloring --mirror-pages

   # Łączenie w PDF
   kdp-format "kolorowanki/*.png" --type pdf --page-size letter --output "kolorowanka_final.pdf"