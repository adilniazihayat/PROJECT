import pandas as pd
import os

class Exporter:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def export_products(self, products_list):
        """Export raw product data to CSV."""
        df = pd.DataFrame(products_list)
        file_path = os.path.join(self.data_dir, 'products.csv')
        df.to_csv(file_path, index=False)
        return file_path

    def export_summary(self, products_list):
        """Export category/subcategory summary statistics."""
        df = pd.DataFrame(products_list)
        
        # Calculate duplicates (based on Title and URL)
        # In a real scrape, duplicates might happen if we hit the same page twice or if items overlap categories
        duplicates = df.duplicated(subset=['Title', 'URL']).sum()
        
        # Group by Category and Subcategory
        summary = df.groupby(['Category', 'Subcategory']).agg(
            Product_Count=('Title', 'count'),
            Avg_Price=('Price', 'mean'),
            Min_Price=('Price', 'min'),
            Max_Price=('Price', 'max')
        ).reset_index()
        
        # Add duplicate count as a global stat or per category?
        # The requirement says "duplicate counts", plural, maybe per subcategory.
        dup_summary = df[df.duplicated(subset=['Title', 'URL'], keep=False)].groupby(['Category', 'Subcategory']).size().reset_index(name='Duplicate_Count')
        
        # Merge summary with duplicate counts
        final_summary = pd.merge(summary, dup_summary, on=['Category', 'Subcategory'], how='left').fillna(0)
        final_summary['Duplicate_Count'] = final_summary['Duplicate_Count'].astype(int)
        
        file_path = os.path.join(self.data_dir, 'category_summary.csv')
        final_summary.to_csv(file_path, index=False)
        return file_path
