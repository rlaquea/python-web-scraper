"""
Example Web Scraper Usage

This script demonstrates how to use the web scraper to collect pricing and
stock information from websites and export it to Excel.
"""

from web_scraper import WebScraper, ExcelExporter


def example_scrape():
    """
    Example function demonstrating web scraper usage.
    
    This is a template showing how to configure and use the scraper.
    You'll need to customize the selectors for your specific target websites.
    """
    
    # Initialize the scraper
    scraper = WebScraper()
    
    # Define products to scrape
    # Note: These are example configurations. You need to inspect the target
    # websites and provide the correct CSS selectors for your use case.
    products = [
        {
            'url': 'https://example.com/product1',
            'name_selectors': [
                'h1.product-title',
                '.product-name',
                'h1[itemprop="name"]'
            ],
            'price_selectors': [
                '.price',
                'span.product-price',
                '[itemprop="price"]',
                '.sale-price'
            ],
            'stock_selectors': [
                '.availability',
                '.stock-status',
                '[itemprop="availability"]',
                '.inventory-status'
            ]
        },
        {
            'url': 'https://example.com/product2',
            'name_selectors': [
                'h1.product-title',
                '.product-name'
            ],
            'price_selectors': [
                '.price',
                'span.product-price'
            ],
            'stock_selectors': [
                '.availability',
                '.stock-status'
            ]
        }
    ]
    
    # Scrape the products
    print("Starting to scrape products...")
    results = scraper.scrape_multiple_products(products)
    
    # Display results
    print("\n" + "="*80)
    print("SCRAPING RESULTS")
    print("="*80)
    for result in results:
        print(f"\nProduct: {result.get('name', 'N/A')}")
        print(f"Price: {result.get('price', 'N/A')}")
        print(f"Stock: {result.get('stock', 'N/A')}")
        print(f"URL: {result.get('url', 'N/A')}")
        print(f"Last Updated: {result.get('last_updated', 'N/A')}")
        if result.get('error'):
            print(f"Error: {result.get('error')}")
        print("-" * 80)
    
    # Export to Excel
    exporter = ExcelExporter('product_data.xlsx')
    exporter.export_to_excel(results, update_existing=True)
    
    print("\nData has been exported to product_data.xlsx")
    print("Run this script again to update the existing data dynamically!")


def example_with_custom_site():
    """
    Example showing how to scrape a specific website structure.
    
    To use this with a real website:
    1. Inspect the website's HTML structure using browser dev tools
    2. Identify the CSS selectors for product name, price, and stock
    3. Update the selectors in the product configuration
    4. Run the scraper
    """
    scraper = WebScraper()
    
    # Example: Scraping a hypothetical e-commerce site
    product_config = {
        'url': 'https://www.example-store.com/products/widget-123',
        'name_selectors': [
            'h1#product-title',          # Try ID selector first
            'h1.product-name',            # Then class selector
            'div.product-info h1'         # Then nested selector
        ],
        'price_selectors': [
            'span.price-current',         # Current/sale price
            'div.pricing .amount',        # Alternative pricing container
            'meta[itemprop="price"]'      # Schema.org metadata
        ],
        'stock_selectors': [
            'div.stock-info span',        # Stock status container
            'p.availability',             # Availability paragraph
            'span.inventory-msg'          # Inventory message
        ]
    }
    
    # Scrape single product
    result = scraper.scrape_product_data(
        url=product_config['url'],
        name_selectors=product_config['name_selectors'],
        price_selectors=product_config['price_selectors'],
        stock_selectors=product_config['stock_selectors']
    )
    
    # Export to Excel
    exporter = ExcelExporter('my_products.xlsx')
    exporter.export_to_excel([result])
    
    return result


def continuous_monitoring_example():
    """
    Example showing how to set up continuous monitoring.
    
    In a real scenario, you might want to:
    - Run this script on a schedule (e.g., using cron or Task Scheduler)
    - Add email notifications when prices change
    - Track price history over time
    """
    import time
    
    scraper = WebScraper()
    exporter = ExcelExporter('monitored_products.xlsx')
    
    products = [
        # Add your products here
    ]
    
    print("Starting continuous monitoring...")
    print("This example will run once. For continuous monitoring,")
    print("schedule this script using cron (Linux/Mac) or Task Scheduler (Windows)")
    
    # Scrape and export
    results = scraper.scrape_multiple_products(products)
    exporter.export_to_excel(results, update_existing=True)
    
    print("Monitoring complete. Excel file has been updated.")


if __name__ == '__main__':
    print("Web Scraper Example")
    print("=" * 80)
    print("\nThis script demonstrates how to use the web scraper.")
    print("Please customize the product URLs and CSS selectors for your needs.")
    print("\nIMPORTANT:")
    print("- Ensure you have permission to scrape the target websites")
    print("- Respect robots.txt and terms of service")
    print("- Add delays between requests to avoid overwhelming servers")
    print("- Some websites may require additional headers or authentication")
    print("\n" + "=" * 80)
    
    # Uncomment the example you want to run:
    # example_scrape()
    # example_with_custom_site()
    # continuous_monitoring_example()
    
    print("\nTo use this scraper:")
    print("1. Uncomment one of the example functions above")
    print("2. Customize the product URLs and CSS selectors")
    print("3. Run the script: python example_scraper.py")
