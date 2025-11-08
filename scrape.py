"""
Advanced Web Scraper Script with Configuration File Support

This script reads product configurations from a JSON file and scrapes
multiple products, exporting the results to Excel.
"""

import json
import sys
import argparse
from web_scraper import WebScraper, ExcelExporter


def load_config(config_file='config.json'):
    """
    Load configuration from JSON file.
    
    Args:
        config_file: Path to the configuration file
        
    Returns:
        Dictionary containing configuration
    """
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        print("Please create a config.json file based on config.example.json")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)


def main():
    """Main function to run the scraper with configuration."""
    parser = argparse.ArgumentParser(
        description='Web scraper for pricing and stock information'
    )
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    parser.add_argument(
        '--output',
        help='Output Excel filename (overrides config file)'
    )
    parser.add_argument(
        '--no-update',
        action='store_true',
        help='Append data instead of updating existing entries'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    if args.verbose:
        print(f"Loading configuration from {args.config}...")
    config = load_config(args.config)
    
    # Get output filename
    output_file = args.output or config.get('output_file', 'product_data.xlsx')
    
    # Initialize scraper
    scraper = WebScraper()
    
    # Prepare products list
    products = config.get('products', [])
    if not products:
        print("Error: No products defined in configuration file.")
        sys.exit(1)
    
    print(f"\nStarting to scrape {len(products)} product(s)...")
    print("=" * 80)
    
    # Scrape products
    results = []
    for idx, product in enumerate(products, 1):
        product_name = product.get('name', f"Product {idx}")
        url = product.get('url')
        
        if not url:
            print(f"[{idx}/{len(products)}] Skipping {product_name}: No URL provided")
            continue
        
        print(f"\n[{idx}/{len(products)}] Scraping: {product_name}")
        print(f"URL: {url}")
        
        result = scraper.scrape_product_data(
            url=url,
            name_selectors=product.get('name_selectors', []),
            price_selectors=product.get('price_selectors', []),
            stock_selectors=product.get('stock_selectors', [])
        )
        
        if args.verbose:
            print(f"  Product Name: {result.get('name', 'N/A')}")
            print(f"  Price: {result.get('price', 'N/A')}")
            print(f"  Stock: {result.get('stock', 'N/A')}")
            if result.get('error'):
                print(f"  Error: {result.get('error')}")
        else:
            status = "✓" if not result.get('error') else "✗"
            print(f"  {status} Scraped successfully" if not result.get('error') else f"  {status} Error: {result.get('error')}")
        
        results.append(result)
    
    print("\n" + "=" * 80)
    print(f"\nExporting data to {output_file}...")
    
    # Export to Excel
    exporter = ExcelExporter(output_file)
    exporter.export_to_excel(results, update_existing=not args.no_update)
    
    print(f"\n✓ Successfully exported {len(results)} product(s) to {output_file}")
    
    # Summary
    successful = sum(1 for r in results if not r.get('error'))
    failed = len(results) - successful
    
    print("\nSummary:")
    print(f"  Total products: {len(results)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    
    if failed > 0:
        print("\nFailed products:")
        for result in results:
            if result.get('error'):
                print(f"  - {result.get('url')}: {result.get('error')}")


if __name__ == '__main__':
    main()
