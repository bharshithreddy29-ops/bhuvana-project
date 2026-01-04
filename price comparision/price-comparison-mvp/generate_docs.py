import os
import json
import pandas as pd

def generate_datasets_document():
    datasets_dir = 'datasets'
    output_file = 'ALL_DATASETS_DOCUMENTATION.txt'
    
    with open(output_file, 'w', encoding='utf-8') as docs:
        docs.write("="*80 + "\n")
        docs.write("PRICE COMPARISON PLATFORM - DATASET DOCUMENTATION\n")
        docs.write("="*80 + "\n\n")
        docs.write(f"This document contains all product data from the '{datasets_dir}' directory.\n")
        docs.write("Data is presented in table format for each platform/category source.\n\n")
        
        # Get all JSON files
        files = [f for f in os.listdir(datasets_dir) if f.endswith('.json')]
        files.sort()
        
        total_products = 0
        
        for filename in files:
            filepath = os.path.join(datasets_dir, filename)
            platform_name = filename.replace('_products.json', '').replace('.json', '').replace('_', ' ').title()
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if not data:
                    continue
                    
                total_products += len(data)
                
                # Header for this file
                docs.write("\n" + "#"*80 + "\n")
                docs.write(f"DATASET: {platform_name} ({filename})\n")
                docs.write(f"Total Items: {len(data)}\n")
                docs.write("#"*80 + "\n\n")
                
                # Convert to DataFrame for easy table formatting
                df = pd.DataFrame(data)
                
                # Select common columns to display (handle potentially missing columns)
                cols_order = ['product_name', 'price', 'brand', 'category']
                cols_to_show = [c for c in cols_order if c in df.columns]
                
                # Add any other useful columns that might exist
                extra_cols = [c for c in df.columns if c not in cols_order and c != 'image_url']
                cols_to_show.extend(extra_cols)
                
                if not cols_to_show:
                    docs.write("No displayable data found.\n")
                    continue
                
                # Rename columns for better readability
                df_display = df[cols_to_show].copy()
                df_display.columns = [c.replace('_', ' ').title() for c in df_display.columns]
                
                # Format price column if it exists
                if 'Price' in df_display.columns:
                    df_display['Price'] = df_display['Price'].apply(lambda x: f"₹{float(x):.2f}" if pd.notnull(x) else "N/A")
                
                # Convert to string table
                table_str = df_display.to_string(index=True)
                docs.write(table_str)
                docs.write("\n\n" + "-"*80 + "\n\n")
                
            except Exception as e:
                docs.write(f"\nERROR reading {filename}: {str(e)}\n\n")
        
        # Summary
        docs.write("\n" + "="*80 + "\n")
        docs.write("SUMMARY\n")
        docs.write("="*80 + "\n")
        docs.write(f"Total Files Processed: {len(files)}\n")
        docs.write(f"Total Products Documented: {total_products}\n")
        docs.write("="*80 + "\n")

    print(f"Documentation generated at: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    generate_datasets_document()
