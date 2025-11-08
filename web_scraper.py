"""
Web Scraper Module

This module provides functionality to scrape pricing data and product stock/availability
information from websites using Beautiful Soup and export the data to Excel files.
"""

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
import os
from datetime import datetime
from typing import List, Dict, Optional


class WebScraper:
    """
    A web scraper class for extracting pricing and product availability data from websites.
    """
    
    def __init__(self, user_agent: Optional[str] = None):
        """
        Initialize the web scraper.
        
        Args:
            user_agent: Optional custom user agent string for HTTP requests
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_page(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: The URL to scrape
            timeout: Request timeout in seconds
            
        Returns:
            BeautifulSoup object if successful, None otherwise
        """
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_price(self, soup: BeautifulSoup, price_selectors: List[str]) -> Optional[str]:
        """
        Extract price from a page using CSS selectors.
        
        Args:
            soup: BeautifulSoup object of the page
            price_selectors: List of CSS selectors to try for finding the price
            
        Returns:
            Price string if found, None otherwise
        """
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                return price_text
        return None
    
    def extract_stock(self, soup: BeautifulSoup, stock_selectors: List[str]) -> Optional[str]:
        """
        Extract stock/availability information from a page using CSS selectors.
        
        Args:
            soup: BeautifulSoup object of the page
            stock_selectors: List of CSS selectors to try for finding stock info
            
        Returns:
            Stock/availability string if found, None otherwise
        """
        for selector in stock_selectors:
            element = soup.select_one(selector)
            if element:
                stock_text = element.get_text(strip=True)
                return stock_text
        return None
    
    def extract_product_name(self, soup: BeautifulSoup, name_selectors: List[str]) -> Optional[str]:
        """
        Extract product name from a page using CSS selectors.
        
        Args:
            soup: BeautifulSoup object of the page
            name_selectors: List of CSS selectors to try for finding the product name
            
        Returns:
            Product name if found, None otherwise
        """
        for selector in name_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None
    
    def scrape_product_data(
        self,
        url: str,
        name_selectors: List[str],
        price_selectors: List[str],
        stock_selectors: List[str]
    ) -> Dict[str, Optional[str]]:
        """
        Scrape product data from a URL.
        
        Args:
            url: URL of the product page
            name_selectors: CSS selectors for product name
            price_selectors: CSS selectors for price
            stock_selectors: CSS selectors for stock/availability
            
        Returns:
            Dictionary containing product data
        """
        soup = self.scrape_page(url)
        
        if not soup:
            return {
                'url': url,
                'name': None,
                'price': None,
                'stock': None,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': 'Failed to fetch page'
            }
        
        return {
            'url': url,
            'name': self.extract_product_name(soup, name_selectors),
            'price': self.extract_price(soup, price_selectors),
            'stock': self.extract_stock(soup, stock_selectors),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': None
        }
    
    def scrape_multiple_products(
        self,
        products: List[Dict[str, any]]
    ) -> List[Dict[str, Optional[str]]]:
        """
        Scrape data for multiple products.
        
        Args:
            products: List of product configurations, each containing:
                - url: Product URL
                - name_selectors: CSS selectors for product name
                - price_selectors: CSS selectors for price
                - stock_selectors: CSS selectors for stock
        
        Returns:
            List of dictionaries containing scraped data for each product
        """
        results = []
        for product in products:
            print(f"Scraping: {product.get('url', 'Unknown URL')}")
            data = self.scrape_product_data(
                url=product['url'],
                name_selectors=product.get('name_selectors', []),
                price_selectors=product.get('price_selectors', []),
                stock_selectors=product.get('stock_selectors', [])
            )
            results.append(data)
        return results


class ExcelExporter:
    """
    Export scraped data to Excel files with dynamic updates.
    """
    
    def __init__(self, filename: str = 'product_data.xlsx'):
        """
        Initialize the Excel exporter.
        
        Args:
            filename: Name of the Excel file to create/update
        """
        self.filename = filename
    
    def _create_header(self, worksheet):
        """Create formatted header row."""
        headers = ['Product Name', 'Price', 'Stock/Availability', 'URL', 'Last Updated', 'Error']
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF')
        
        for col, header in enumerate(headers, start=1):
            cell = worksheet.cell(row=1, column=col)
            cell.value = header
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
    
    def _find_product_row(self, worksheet, url: str) -> Optional[int]:
        """Find the row number for a product by URL."""
        for row in range(2, worksheet.max_row + 1):
            if worksheet.cell(row=row, column=4).value == url:
                return row
        return None
    
    def export_to_excel(self, data: List[Dict[str, Optional[str]]], update_existing: bool = True):
        """
        Export data to Excel file.
        
        Args:
            data: List of product data dictionaries
            update_existing: If True, update existing entries; if False, append all
        """
        # Load existing workbook or create new one
        if os.path.exists(self.filename) and update_existing:
            workbook = load_workbook(self.filename)
            worksheet = workbook.active
        else:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "Product Data"
            self._create_header(worksheet)
        
        # Process each product
        for product_data in data:
            if update_existing:
                row = self._find_product_row(worksheet, product_data['url'])
                if row is None:
                    # New product, append to end
                    row = worksheet.max_row + 1
            else:
                # Always append
                row = worksheet.max_row + 1
            
            # Write data
            worksheet.cell(row=row, column=1).value = product_data.get('name', 'N/A')
            worksheet.cell(row=row, column=2).value = product_data.get('price', 'N/A')
            worksheet.cell(row=row, column=3).value = product_data.get('stock', 'N/A')
            worksheet.cell(row=row, column=4).value = product_data.get('url', 'N/A')
            worksheet.cell(row=row, column=5).value = product_data.get('last_updated', 'N/A')
            worksheet.cell(row=row, column=6).value = product_data.get('error', '')
        
        # Adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except Exception:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
        
        # Save workbook
        workbook.save(self.filename)
        print(f"Data exported to {self.filename}")
    
    def read_excel(self) -> List[Dict[str, str]]:
        """
        Read existing data from Excel file.
        
        Returns:
            List of product data dictionaries
        """
        if not os.path.exists(self.filename):
            return []
        
        workbook = load_workbook(self.filename)
        worksheet = workbook.active
        
        data = []
        for row in range(2, worksheet.max_row + 1):
            data.append({
                'name': worksheet.cell(row=row, column=1).value,
                'price': worksheet.cell(row=row, column=2).value,
                'stock': worksheet.cell(row=row, column=3).value,
                'url': worksheet.cell(row=row, column=4).value,
                'last_updated': worksheet.cell(row=row, column=5).value,
                'error': worksheet.cell(row=row, column=6).value
            })
        
        return data
