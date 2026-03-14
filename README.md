# E-Commerce Web Scraper

A modular web scraper for the [WebScraper.io Test Site](https://webscraper.io/test-sites/e-commerce/static), built with `uv`, `BeautifulSoup4`, and `pandas`.

## Features
- **Modular Architecture**: Separate logic for crawling, parsing, and exporting.
- **Dynamic Discovery**: Automatically finds categories and subcategories.
- **Pagination Support**: Handles multi-page listings.
- **Data Cleaning**: Normalizes prices and handles missing descriptions.
- **Deduplication**: Identifies and counts duplicate records in the summary.

## Project Structure
```
src/
├── main.py              # Entry point
└── scraper/
    ├── crawler.py       # Category/Subcategory discovery and pagination
    ├── parsers.py       # Data extraction logic
    ├── exporters.py     # CSV generation
    ├── utils.py         # Text cleaning and URL resolution
    └── __init__.py
data/
├── products.csv         # Detailed product information
└── category_summary.csv # Aggregated statistics and duplicate counts
```

## Setup Instructions

### Prerequisites
- [uv](https://github.com/astral-sh/uv) installed on your system.
- Git installed on your system.

### Installation
1. Clone the repository (once provided).
2. Sync the environment using `uv`:
   ```bash
   uv sync
   ```

### Running the Scraper
Execute the scraper via the `uv` tool:
```bash
uv run src/main.py
```

## Git Workflow
This project follows a strict branching and merging sequence:
1. **Initial**: Start on `main`, create `dev`.
2. **Features**:
   - `feature/catalog-navigation`: Logic for categories, subcategories, and pagination.
   - `feature/product-details`: Logic for scraping individual product pages.
   - Merge both into `dev`.
3. **Fixes**:
   - `fix/url-resolution`: Absolute link handling.
   - `fix/deduplication`: Removing overlap.
   - Merge both into `dev`.
4. **Final**: Merge `dev` into `main` after validation.

## Data Output
- **products.csv**: Fields include Category, Subcategory, Title, Price, URL, Description, Review Count, and Spec.
- **category_summary.csv**: Aggregated stats (Count, Avg Price) and duplicate metrics.
