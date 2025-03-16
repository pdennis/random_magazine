# Random Magazine Browser

A command-line tool that discovers and opens random magazines from the Internet Archive collection, helping you explore historical publications across different eras.

## Features

- Browse random magazines from the Internet Archive
- Filter by collection, year range, or specific decade
- Continuous browsing mode with customizable delay
- View information about each magazine (title, year, creator, collections, subjects)
- Get a list of popular magazine collections

## Requirements

- Python 3.6 or higher
- Required packages: `requests`, `argparse` (included in standard library)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Create a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install required packages
   ```bash
   pip install requests
   ```

## Making the script executable

Add a shebang line to the beginning of the script:
```python
#!/home/pdennis/projects/magazine/venv/bin/python
```

Make the script executable:
```bash
chmod +x mag.py
```

## Adding to PATH

For convenience, you can add the script to your PATH to run it from anywhere:

```bash
# Create a bin directory in your home if it doesn't exist
mkdir -p ~/bin

# Create a symlink to your script
ln -s /home/pdennis/projects/magazine/mag.py ~/bin/random_magazine

# Add ~/bin to your PATH if it's not already there
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Basic Usage

```bash
random_magazine
```

This will fetch and open a random magazine in your default web browser.

### Filter by Collection

```bash
random_magazine --collection magazine_rack
```

### Filter by Year Range

```bash
random_magazine --min-year 1950 --max-year 1959
```

### Filter by Decade

```bash
random_magazine --decade 1980
```

### Continuous Browsing

```bash
random_magazine --continuous --delay 60
```
This will open a new random magazine every 60 seconds. Press Ctrl+C to exit.

### List Popular Collections

```bash
random_magazine --list-collections
```

### Advanced Options

```bash
random_magazine --collection scientific_american --min-year 2000 --max 200
```
This will fetch from the scientific_american collection, from year 2000 onwards, and search through up to 200 results.

## Popular Collections

- magazine_rack
- scientific_american
- national_geographic_magazine
- lifemagazine
- time_magazine_archives
- popular_mechanics
- computers_and_techmagazines
- pulpmagazinearchive
- vintage_computer_magazines
- vogue
- new_yorker
- wired

## Tips

- If you're getting similar results, try increasing the `--max` parameter to search through more magazines
- Use `--continuous` mode for a relaxing digital magazine browsing experience
- Different collections have different date ranges available

## Troubleshooting

- If you get a "No magazines found" error, try broadening your search criteria
- If the script doesn't open your browser, check your default browser settings
- If you encounter network errors, verify your internet connection

---

Explore the vast archives of magazines spanning decades of history, culture, technology, and more with this simple tool. Happy browsing!
