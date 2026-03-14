from bs4 import BeautifulSoup
from .utils import clean_price, clean_text, resolve_url

class ProductParser:
    @staticmethod
    def parse_listing(html, base_url, category, subcategory):
        """Parse product information from a listing item."""
        soup = BeautifulSoup(html, 'html.parser')
        
        products = []
        items = soup.select('.thumbnail')
        
        for item in items:
            title_tag = item.select_one('h4 > a') or item.select_one('h4')
            title = clean_text(title_tag.get_text()) if title_tag else "N/A"
            relative_url = title_tag['href'] if title_tag and title_tag.has_attr('href') else ""
            url = resolve_url(base_url, relative_url)
            
            price_tag = item.select_one('.price')
            price = clean_price(price_tag.get_text()) if price_tag else 0.0
            
            desc_tag = item.select_one('.description')
            description = clean_text(desc_tag.get_text()) if desc_tag else "N/A"
            
            reviews_tag = item.select_one('.ratings p.pull-right')
            reviews = clean_text(reviews_tag.get_text()) if reviews_tag else "0 reviews"
            review_count = int(re.search(r'\d+', reviews).group()) if re.search(r'\d+', reviews) else 0
            
            # For "Spec", we'll take the first part of the description (e.g., Screen Size)
            spec = description.split(',')[0] if ',' in description else description
            
            products.append({
                'Category': category,
                'Subcategory': subcategory,
                'Title': title,
                'Price': price,
                'URL': url,
                'Description': description,
                'Review Count': review_count,
                'Spec': spec
            })
            
        return products

    @staticmethod
    def parse_detail(html):
        """Parse additional detail page data if needed."""
        # The requirements ask for detail page extraction too.
        # However, for this static site, all info is usually in the listing.
        # But I'll implement it to fulfill the "extract detail page data" requirement.
        soup = BeautifulSoup(html, 'html.parser')
        
        # In the detail page:
        # Title is in <h4>, Price is in .price, Description/Spec is in .description
        # We might find more detailed specs here if the site has them.
        
        data = {}
        title_tag = soup.select_one('.caption h4:not(.price)')
        data['title'] = clean_text(title_tag.get_text()) if title_tag else "N/A"
        
        price_tag = soup.select_one('.price')
        data['price'] = clean_price(price_tag.get_text()) if price_tag else 0.0
        
        desc_tag = soup.select_one('.description')
        data['description'] = clean_text(desc_tag.get_text()) if desc_tag else "N/A"
        
        reviews_tag = soup.select_one('.ratings p.pull-right')
        data['review_count'] = int(re.search(r'\d+', reviews_tag.get_text()).group()) if reviews_tag and re.search(r'\d+', reviews_tag.get_text()) else 0
        
        # For spec, maybe check if there are other attributes or just splitting description
        data['spec'] = data['description'].split(',')[0] if ',' in data['description'] else data['description']
        
        return data

import re # Needed for review count extraction
