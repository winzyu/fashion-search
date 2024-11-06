import pandas as pd
import os
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

def display_data_structure(df):
    """
    Display dataset structure similar to R's str() function
    """
    print("\n=== Data Structure (similar to R's str()) ===")
    print(f"DataFrame with {df.shape[0]:,} observations and {df.shape[1]} variables:\n")
    
    for col in df.columns:
        n_unique = df[col].nunique()
        sample_vals = df[col].dropna().sample(min(3, len(df))).values
        print(f"$ {col}: {df[col].dtype}")
        print(f"  {n_unique:,} unique values")
        print(f"  Sample values: {', '.join(str(x) for x in sample_vals)}\n")

def analyze_fashion_dataset(dataset_path):
    """
    Analyze the Myntra fashion product dataset and print summary statistics.
    
    Args:
        dataset_path (str): Path to the dataset directory
    """
    # Load the data
    try:
        df = pd.read_csv(Path(dataset_path) / 'Fashion Dataset.csv')
    except FileNotFoundError:
        print(f"Could not find 'Fashion Dataset.csv' in {dataset_path}")
        print("Available files in directory:")
        print("\n".join(os.listdir(dataset_path)))
        return
    
    # Display first few rows (like R's head())
    print("\n=== First 5 Rows (similar to R's head()) ===")
    print(df.head().to_string())
    
    # Display data structure
    display_data_structure(df)
        
    print("\n=== Dataset Overview ===")
    print(f"Total number of products: {len(df):,}")
    print(f"Number of columns: {len(df.columns)}")
    print("\nColumns in dataset:")
    for col in df.columns:
        print(f"- {col} ({df[col].dtype})")
    
    print("\n=== Missing Values Analysis ===")
    missing_data = df.isnull().sum()
    print(missing_data[missing_data > 0].to_string())
    
    # Check for the actual category column name in the dataset
    category_col = next((col for col in df.columns if 'category' in col.lower()), None)
    if category_col:
        print(f"\n=== Category Distribution ({category_col}) ===")
        category_counts = df[category_col].value_counts()
        print(f"Number of unique categories: {len(category_counts)}")
        print("\nTop 10 categories:")
        print(category_counts.head(10).to_string())
    
    # Check for price column
    price_col = next((col for col in df.columns if 'price' in col.lower()), None)
    if price_col:
        print(f"\n=== Price Analysis ({price_col}) ===")
        print(f"Price range: ₹{df[price_col].min():,.2f} - ₹{df[price_col].max():,.2f}")
        print(f"Average price: ₹{df[price_col].mean():,.2f}")
        print(f"Median price: ₹{df[price_col].median():,.2f}")
        
        # Add quartile information
        print("\nPrice quartiles:")
        print(df[price_col].describe().to_string())
    
    # Check for brand column
    brand_col = next((col for col in df.columns if 'brand' in col.lower()), None)
    if brand_col:
        print(f"\n=== Brand Analysis ({brand_col}) ===")
        brand_counts = df[brand_col].value_counts()
        print(f"Number of unique brands: {len(brand_counts)}")
        print("\nTop 10 brands:")
        print(brand_counts.head(10).to_string())
    
    # Create visualizations directory if it doesn't exist
    viz_dir = Path(dataset_path) / 'analysis_output'
    viz_dir.mkdir(exist_ok=True)
    
    # Price distribution plot
    if price_col:
        plt.figure(figsize=(12, 6))
        sns.histplot(data=df, x=price_col, bins=50)
        plt.title('Price Distribution')
        plt.xlabel('Price (₹)')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(viz_dir / 'price_distribution.png')
        plt.close()
    
    # Image directory analysis
    images_dir = Path(dataset_path) / 'Images'
    if images_dir.exists():
        print("\n=== Image Files Analysis ===")
        image_files = list(images_dir.glob('*'))
        print(f"Number of image files: {len(image_files):,}")
        print(f"Sample image filenames: {', '.join(str(f.name) for f in image_files[:5])}")
    
    # Save summary to file
    summary = {
        'total_products': len(df),
        'columns': list(df.columns),
        'missing_values': missing_data.to_dict(),
        'unique_categories': len(category_counts) if category_col else None,
        'unique_brands': len(brand_counts) if brand_col else None,
    }
    
    if price_col:
        summary['price_stats'] = {
            'min': float(df[price_col].min()),
            'max': float(df[price_col].max()),
            'mean': float(df[price_col].mean()),
            'median': float(df[price_col].median())
        }
    
    with open(viz_dir / 'dataset_summary.json', 'w') as f:
        json.dump(summary, f, indent=4)
    
    print(f"\nAnalysis complete! Visualizations and summary saved to {viz_dir}")

if __name__ == "__main__":
    # Use the path from your download
    dataset_path = "../dataset/"
    analyze_fashion_dataset(dataset_path)
