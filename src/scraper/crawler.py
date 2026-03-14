import requests
from bs4 import BeautifulSoup
from .utils import resolve_url

class Crawler:
    BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

    def __init__(self, session=None):
        self.session = session or requests.Session()

    def get_categories(self):
        """Discover top-level categories."""
        response = self.session.get(self.BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        categories = []
        # Categories are usually in the sidebar under 'Home'
        sidebar_links = soup.select('#side-menu > li > a')
        for link in sidebar_links:
            name = link.get_text().strip()
            if name == "Home":
                continue
            categories.append({
                'name': name,
                'url': resolve_url(self.BASE_URL, link['href'])
            })
        return categories

    def get_subcategories(self, category_url):
        """Discover subcategories for a given category."""
        response = self.session.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        subcategories = []
        # Subcategories are usually nested in the sidebar when on a category page
        # Or they appear as links in the main content area
        sub_links = soup.select('#side-menu > li.active > ul > li > a')
        for link in sub_links:
            subcategories.append({
                'name': link.get_text().strip(),
                'url': resolve_url(self.BASE_URL, link['href'])
            })
        return subcategories

    def get_pages(self, subcategory_url):
        """Discover all paginated URLs for a subcategory."""
        response = self.session.get(subcategory_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        pages = [subcategory_url]
        pagination_links = soup.select('.pagination li a')
        
        for link in pagination_links:
            href = link.get('href')
            if href and 'page=' in href:
                full_url = resolve_url(self.BASE_URL, href)
                if full_url not in pages:
                    pages.append(full_url)
        
        # Sort pages to process sequentially if possible
        return sorted(list(set(pages)))
