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
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -e .
   ```

### 3. Uruchamianie programu

#### Interfejs graficzny (GUI)

Program posiada przyjazny interfejs graficzny, który jest domyślnym sposobem uruchamiania:

1. Uruchom program przez:
   ```bash
   kdp-gui
   ```
   lub
   ```bash
   python -m kdp_formatter
   ```

2. W interfejsie graficznym:
   - Wybierz plik wejściowy używając przycisku "Przeglądaj..."
   - Wybierz typ przetwarzania (tekst, obraz, PDF, kolorowanka)
   - Ustaw opcje dla wybranego typu przetwarzania
   - Wybierz lokalizację pliku wyjściowego
   - Kliknij "Rozpocznij przetwarzanie"

3. Postęp przetwarzania będzie widoczny w oknie programu

#### Wiersz poleceń (CLI)

Alternatywnie, program można uruchomić z wiersza poleceń:

```bash
kdp-format --help  # Pokaż dostępne opcje
```

### 4. Przykłady użycia GUI

#### A. Formatowanie dokumentu tekstowego do e-booka

1. Uruchom `kdp-gui`
2. Kliknij "Przeglądaj..." i wybierz plik Word/PDF/TXT
3. Wybierz typ przetwarzania "Tekst"
4. Wybierz format wyjściowy (np. "epub")
5. Wybierz lokalizację pliku wyjściowego
6. Kliknij "Rozpocznij przetwarzanie"

#### B. Tworzenie kolorowanki

1. Uruchom `kdp-gui`
2. Wybierz obrazek źródłowy
3. Wybierz typ przetwarzania "Kolorowanka"
4. Zaznacz opcję "Strony lustrzane" jeśli potrzebne
5. Wybierz lokalizację pliku wyjściowego
6. Kliknij "Rozpocznij przetwarzanie"

#### C. Przygotowanie okładki książki

1. Uruchom `kdp-gui`
2. Wybierz plik graficzny okładki
3. Wybierz typ przetwarzania "Obraz"
4. Ustaw DPI na 300
5. Wybierz przestrzeń kolorów (CMYK dla druku)
6. Kliknij "Rozpocznij przetwarzanie"

### 5. Rozwiązywanie problemów

1. Program się nie uruchamia:
   - Sprawdź czy środowisko wirtualne jest aktywowane
   - Spróbuj `python -m kdp_formatter`
   - Sprawdź logi błędów w terminalu

2. Problemy z instalacją pakietów (pip):
   - Użyj opcji `--trusted-host` jak opisano w sekcji instalacji
   - Sprawdź połączenie internetowe
   - Spróbuj użyć innego połączenia internetowego

3. Problemy z przetwarzaniem:
   - Sprawdź czy plik wejściowy jest poprawny
   - Upewnij się, że masz wystarczająco miejsca na dysku
   - Sprawdź prawa dostępu do katalogów

### 6. Wsparcie

Jeśli napotkasz problemy:
1. Sprawdź sekcję "Issues" na GitHubie
2. Utwórz nowe zgłoszenie, dołączając:
   - Zrzut ekranu błędu
   - Kroki prowadzące do błędu
   - Logi z terminala
   - Informacje o systemie operacyjnym