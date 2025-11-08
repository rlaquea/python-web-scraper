# Quick Start Guide

This guide will help you get started with the Python Web Scraper quickly.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rlaquea/python-web-scraper.git
   cd python-web-scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup Your First Scrape

### Step 1: Create Configuration

Copy the example configuration:
```bash
cp config.example.json config.json
```

### Step 2: Find Your CSS Selectors

To scrape a website, you need to identify the CSS selectors:

1. Open your target website in a web browser
2. Right-click on the element you want to scrape (e.g., price)
3. Select "Inspect" or "Inspect Element"
4. In the developer tools, you'll see the HTML structure
5. Look for unique identifiers like:
   - Class names: `class="price"` → use `.price`
   - IDs: `id="product-price"` → use `#product-price`
   - Attributes: `itemprop="price"` → use `[itemprop="price"]`

### Step 3: Edit Configuration

Edit `config.json` with your product information:

```json
{
  "output_file": "my_products.xlsx",
  "products": [
    {
      "name": "iPhone 15",
      "url": "https://www.apple.com/shop/buy-iphone/iphone-15",
      "name_selectors": [
        "h1.rf-hcard-headline",
        ".product-name"
      ],
      "price_selectors": [
        ".price",
        ".current-price",
        "[data-autom='purchaseGroupOptionFullPrice']"
      ],
      "stock_selectors": [
        ".availability",
        ".delivery-msg"
      ]
    }
  ]
}
```

**Tips for CSS Selectors**:
- Provide multiple selectors as fallbacks
- Start with the most specific selector
- Use browser dev tools to test selectors in the console:
  ```javascript
  document.querySelector('.price')
  ```

### Step 4: Run the Scraper

```bash
python scrape.py
```

With options:
```bash
# Use verbose mode to see detailed output
python scrape.py --verbose

# Use a different config file
python scrape.py --config my_config.json

# Override the output filename
python scrape.py --output my_data.xlsx

# Append instead of updating
python scrape.py --no-update
```

### Step 5: View Results

Open the generated Excel file (`product_data.xlsx` by default) to see:
- Product names
- Current prices
- Stock availability
- Last update timestamp

## Updating Prices

Run the script again to update the Excel file with current data:

```bash
python scrape.py
```

The scraper will:
- Update existing products (matched by URL)
- Add new products
- Keep the timestamp of the last update

## Scheduling Automatic Updates

### On Linux/Mac (cron)

Edit your crontab:
```bash
crontab -e
```

Add a line to run every hour:
```
0 * * * * cd /path/to/python-web-scraper && /usr/bin/python3 scrape.py
```

### On Windows (Task Scheduler)

1. Open Task Scheduler
2. Create New Task
3. Set Trigger: Daily or Hourly
4. Set Action: Start a program
   - Program: `python.exe`
   - Arguments: `scrape.py`
   - Start in: `C:\path\to\python-web-scraper`

## Common Issues

### Problem: "Failed to fetch page"
**Solutions**:
- Check your internet connection
- Verify the URL is correct and accessible
- Some websites block automated requests - try adding delays
- Check if the website requires authentication

### Problem: "N/A" in data fields
**Solutions**:
- Your CSS selectors are incorrect
- Inspect the website again and update selectors
- The website structure may have changed
- Some content may be loaded dynamically with JavaScript

### Problem: Empty or incorrect data
**Solutions**:
- Test your CSS selectors in browser console
- Try different selector variations
- Check if content is inside an iframe
- Website may use JavaScript to load content dynamically

## Best Practices

1. **Respect robots.txt**: Check `https://example.com/robots.txt`
2. **Add delays**: Don't overwhelm servers with requests
3. **Use proper User-Agent**: Identify yourself clearly
4. **Check Terms of Service**: Ensure you're allowed to scrape
5. **Monitor changes**: Websites update their structure
6. **Handle errors**: Always check for errors in results

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review [example_scraper.py](example_scraper.py) for code examples
- Run tests: `python test_scraper.py`
- Open an issue on GitHub for bugs or questions

## Example Websites to Practice

For learning purposes, you can practice on:
- Your own website
- Sites that explicitly allow scraping
- Public APIs with HTML endpoints

**Remember**: Always respect website owners and their terms of service!
