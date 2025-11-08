# Python Web Scraper

A powerful Python-based web scraper using Beautiful Soup to gather pricing data and product stock/availability information from websites. The scraper can export data to Excel files that dynamically update when prices or stock levels change.

## Features

- **Web Scraping**: Extract product information from websites using Beautiful Soup
- **Flexible Selectors**: Support for multiple CSS selectors to handle different website structures
- **Pricing Data**: Scrape product prices from various e-commerce sites
- **Stock Information**: Extract product availability and stock levels
- **Excel Export**: Export data to formatted Excel files using openpyxl
- **Dynamic Updates**: Update existing Excel files with new data without losing history
- **Multiple Products**: Scrape multiple products in a single run
- **Error Handling**: Robust error handling with detailed error messages

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rlaquea/python-web-scraper.git
cd python-web-scraper
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- beautifulsoup4==4.12.2
- requests==2.31.0
- openpyxl==3.1.2
- lxml==4.9.3

## Quick Start

### Using the Command-Line Script

The easiest way to use the scraper is with the `scrape.py` script:

1. Copy the example configuration:
```bash
cp config.example.json config.json
```

2. Edit `config.json` with your target URLs and CSS selectors

3. Run the scraper:
```bash
python scrape.py
```

Optional arguments:
- `--config FILE`: Specify a different config file
- `--output FILE`: Override the output filename
- `--no-update`: Append data instead of updating existing entries
- `--verbose`: Show detailed output

### Configuration File Format

Create a `config.json` file:

```json
{
  "output_file": "product_data.xlsx",
  "products": [
    {
      "name": "Product Name",
      "url": "https://example.com/product",
      "name_selectors": ["h1.product-title"],
      "price_selectors": [".price"],
      "stock_selectors": [".stock-status"]
    }
  ]
}
```

## Usage

### Basic Usage (Python API)

```python
from web_scraper import WebScraper, ExcelExporter

# Initialize the scraper
scraper = WebScraper()

# Define product configuration
products = [
    {
        'url': 'https://example.com/product1',
        'name_selectors': ['h1.product-title', '.product-name'],
        'price_selectors': ['.price', 'span.product-price'],
        'stock_selectors': ['.availability', '.stock-status']
    }
]

# Scrape products
results = scraper.scrape_multiple_products(products)

# Export to Excel
exporter = ExcelExporter('product_data.xlsx')
exporter.export_to_excel(results, update_existing=True)
```

### Finding CSS Selectors

To scrape a website, you need to identify the CSS selectors for the elements you want to extract:

1. Open the target website in your browser
2. Right-click on the element (price, product name, etc.) and select "Inspect"
3. Find the HTML element in the developer tools
4. Note the class names, IDs, or other attributes
5. Create CSS selectors based on these attributes

Example selectors:
- By class: `.price`, `.product-name`, `.stock-status`
- By ID: `#product-title`, `#price-value`
- By attribute: `[itemprop="price"]`, `[data-price]`
- Nested: `div.product-info h1`, `.pricing span.amount`

### Running the Example

```bash
python example_scraper.py
```

Edit `example_scraper.py` to customize:
- Product URLs
- CSS selectors for your target websites
- Output filename

### Dynamic Updates

The scraper supports dynamic updates to Excel files:

```python
# First run: Creates new Excel file with data
exporter.export_to_excel(results, update_existing=True)

# Subsequent runs: Updates existing entries based on URL
# - If URL exists: Updates the row with new data
# - If URL is new: Adds a new row
exporter.export_to_excel(results, update_existing=True)
```

### Continuous Monitoring

For continuous price/stock monitoring, schedule the script to run periodically:

**Linux/Mac (cron):**
```bash
# Run every hour
0 * * * * cd /path/to/python-web-scraper && python example_scraper.py
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create a new task
3. Set the trigger (e.g., hourly, daily)
4. Set the action to run `python.exe example_scraper.py`

## API Reference

### WebScraper Class

```python
WebScraper(user_agent=None)
```

**Methods:**

- `scrape_page(url, timeout=10)`: Fetch and parse a web page
- `extract_price(soup, price_selectors)`: Extract price using CSS selectors
- `extract_stock(soup, stock_selectors)`: Extract stock info using CSS selectors
- `extract_product_name(soup, name_selectors)`: Extract product name using CSS selectors
- `scrape_product_data(url, name_selectors, price_selectors, stock_selectors)`: Scrape complete product data
- `scrape_multiple_products(products)`: Scrape multiple products

### ExcelExporter Class

```python
ExcelExporter(filename='product_data.xlsx')
```

**Methods:**

- `export_to_excel(data, update_existing=True)`: Export data to Excel
- `read_excel()`: Read existing data from Excel file

## Excel Output Format

The generated Excel file includes:

| Product Name | Price | Stock/Availability | URL | Last Updated | Error |
|-------------|-------|-------------------|-----|--------------|-------|
| Product 1   | $29.99| In Stock          | ... | 2024-01-15... |       |

- **Product Name**: Name of the product
- **Price**: Current price
- **Stock/Availability**: Stock status (In Stock, Out of Stock, Limited, etc.)
- **URL**: Product URL
- **Last Updated**: Timestamp of last scrape
- **Error**: Any errors encountered during scraping

## Best Practices

1. **Respect robots.txt**: Check the website's robots.txt file before scraping
2. **Rate Limiting**: Add delays between requests to avoid overwhelming servers
3. **User Agent**: Use a descriptive user agent string
4. **Terms of Service**: Ensure you have permission to scrape the website
5. **Error Handling**: Always check for errors in the returned data
6. **Selectors**: Provide multiple selector options as websites may change structure

## Troubleshooting

### Common Issues

**Problem**: "Failed to fetch page" error
- **Solution**: Check your internet connection, verify the URL is correct, ensure the website is accessible

**Problem**: Data fields show "N/A"
- **Solution**: The CSS selectors may be incorrect. Inspect the website and update selectors

**Problem**: Excel file is locked
- **Solution**: Close the Excel file before running the scraper

## Legal Disclaimer

This tool is for educational purposes. When using this scraper:

- Ensure you have permission to scrape the target website
- Respect the website's robots.txt file
- Comply with the website's Terms of Service
- Don't overwhelm servers with too many requests
- Be mindful of copyright and data protection laws

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
