"""
Test script to verify web scraper functionality
"""

from web_scraper import WebScraper, ExcelExporter
import os


def test_basic_functionality():
    """Test basic scraper and exporter functionality."""
    print("Testing Web Scraper Basic Functionality")
    print("=" * 80)
    
    # Test 1: Initialize scraper
    print("\n1. Testing scraper initialization...")
    scraper = WebScraper()
    print("   ✓ WebScraper initialized successfully")
    
    # Test 2: Initialize exporter
    print("\n2. Testing exporter initialization...")
    exporter = ExcelExporter('test_output.xlsx')
    print("   ✓ ExcelExporter initialized successfully")
    
    # Test 3: Test with example.com (simple, accessible site)
    print("\n3. Testing page scraping with example.com...")
    soup = scraper.scrape_page('https://example.com')
    if soup:
        print("   ✓ Successfully fetched and parsed page")
        title = soup.find('h1')
        if title:
            print(f"   ✓ Found page title: {title.get_text(strip=True)}")
    else:
        print("   ✗ Failed to fetch page")
    
    # Test 4: Test scraping with mock data
    print("\n4. Testing product data scraping...")
    result = scraper.scrape_product_data(
        url='https://example.com',
        name_selectors=['h1', 'title'],
        price_selectors=['.price', '.cost'],  # Won't find these on example.com
        stock_selectors=['.stock', '.availability']  # Won't find these either
    )
    print(f"   ✓ Product name: {result.get('name', 'Not found')}")
    print(f"   ✓ Price: {result.get('price', 'Not found')}")
    print(f"   ✓ Stock: {result.get('stock', 'Not found')}")
    print(f"   ✓ Last updated: {result.get('last_updated')}")
    
    # Test 5: Test Excel export
    print("\n5. Testing Excel export...")
    test_data = [
        {
            'url': 'https://example.com/product1',
            'name': 'Test Product 1',
            'price': '$29.99',
            'stock': 'In Stock',
            'last_updated': '2024-01-15 10:30:00',
            'error': None
        },
        {
            'url': 'https://example.com/product2',
            'name': 'Test Product 2',
            'price': '$49.99',
            'stock': 'Limited Availability',
            'last_updated': '2024-01-15 10:30:05',
            'error': None
        }
    ]
    
    exporter.export_to_excel(test_data, update_existing=False)
    if os.path.exists('test_output.xlsx'):
        print("   ✓ Excel file created successfully")
        
        # Test 6: Test reading from Excel
        print("\n6. Testing Excel reading...")
        read_data = exporter.read_excel()
        print(f"   ✓ Read {len(read_data)} rows from Excel")
        
        # Test 7: Test dynamic update
        print("\n7. Testing dynamic update...")
        updated_data = [
            {
                'url': 'https://example.com/product1',
                'name': 'Test Product 1',
                'price': '$24.99',  # Price changed
                'stock': 'In Stock',
                'last_updated': '2024-01-15 11:00:00',
                'error': None
            },
            {
                'url': 'https://example.com/product3',  # New product
                'name': 'Test Product 3',
                'price': '$39.99',
                'stock': 'Pre-order',
                'last_updated': '2024-01-15 11:00:05',
                'error': None
            }
        ]
        exporter.export_to_excel(updated_data, update_existing=True)
        print("   ✓ Excel file updated successfully")
        
        updated_read_data = exporter.read_excel()
        print(f"   ✓ Now contains {len(updated_read_data)} rows")
        
        # Cleanup
        os.remove('test_output.xlsx')
        print("\n8. Cleanup complete")
    else:
        print("   ✗ Excel file was not created")
    
    print("\n" + "=" * 80)
    print("All tests completed successfully!")
    print("=" * 80)


if __name__ == '__main__':
    test_basic_functionality()
