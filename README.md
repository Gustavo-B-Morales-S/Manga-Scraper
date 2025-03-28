# Manga-Scraper

**Manga-Scraper** is a web scraping project designed to extract detailed information from the largest manga database in Brazil. The goal is to collect data such as price in different marketplaces, release dates in Brazil and Japan, volumes, chapters, publishers (Brazilian and Japanese), translators, authors, genres, and other relevant information.

## Project Overview

- **Data Collection**: Scrapes manga information using HTTPX and BeautifulSoup/Selectolax.
- **Local Storage**: Data is stored in local files for efficiency and easy access.
- **Analysis and Transformation**: Extracted data can be processed and analyzed for future use.
- **Dependency Management**: Uses Poetry to organize and manage Python libraries.

## Project Structure

```plaintext
.
├── LICENSE.txt
├── poetry.lock
├── pyproject.toml
├── README.md
├── contents/
│   └── example.html           # All HTML content containing manga information
├── data/
│   └── analysis.ipynb         # Notebook for data analysis
├── src/
│   ├── core/
│   │   ├── agents.py          # User-agent handling
│   │   ├── requester.py       # HTTP request management
│   │   ├── settings.py        # Project settings
│   │   └── utils.py           # Utility functions
│   ├── entrypoint.py          # Scraper entry point
│   ├── extraction/
│   │   ├── __init__.py
│   │   ├── spider.py          # Main scraping module
│   │   ├── static.py          # Static values used in scraping
│   │   └── utils.py           # Utility functions for data extraction
│   └── __init__.py
├── template.env               # Environment variables template
└── tests/
    └── test_todo.py           # Placeholder for tests
```

## Requirements

- **Python 3.12.4+**
- **Poetry**

## Installation and Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Manga-Scraper
```

### 2. Install dependencies with Poetry

```bash
poetry install && poetry shell
```

### 3. Environment Configuration

Create a `.env` file based on `template.env` and fill in the necessary configurations.

## Usage

### Running the Scraper

To start data collection, run:

```bash
poetry run python3 src/extraction/spider.py
```

This will initiate the scraping process and store the extracted data locally.

## Data Analysis

Collected data can be analyzed using the `analysis.ipynb` notebook located in `src/extraction/data/`.

## License

This project is licensed under the MIT License. See `LICENSE.txt` for more details.
