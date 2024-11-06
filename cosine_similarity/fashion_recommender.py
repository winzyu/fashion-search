from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import json
import numpy as np

class FashionRecommender:
    def __init__(self, df):
        self.df = df
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.prepare_features()
        
    def prepare_features(self):
        """Prepare text features for similarity comparison"""
        # Combine relevant text fields
        self.df['combined_features'] = self.df.apply(self._combine_features, axis=1)
        
        # Create TF-IDF matrix
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['combined_features'].fillna(''))
        print(f"Created TF-IDF matrix with shape: {self.tfidf_matrix.shape}")
        
    def _combine_features(self, row):
        """Combine relevant features into a single text string"""
        features = []
        
        # Add product name
        if pd.notna(row['name']):
            features.append(str(row['name']))
            
        # Add color
        if pd.notna(row['colour']):
            features.append(f"color {str(row['colour'])}")
            
        # Add brand
        if pd.notna(row['brand']):
            features.append(f"brand {str(row['brand'])}")
            
        # Add description
        if pd.notna(row['description']):
            features.append(str(row['description']))
            
        # Add attributes
        if pd.notna(row['p_attributes']):
            try:
                attrs = json.loads(str(row['p_attributes']).replace("'", '"'))
                for key, value in attrs.items():
                    if value and value != 'NA':
                        features.append(f"{key} {value}")
            except:
                pass
                
        return ' '.join(features)
    
    def search_similar_items(self, search_query, n_results=5):
        """Search for items similar to the search query"""
        try:
            # Transform search query using same TF-IDF vectorizer
            query_vector = self.tfidf.transform([search_query])
            
            # Calculate cosine similarity between query and all items
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get indices of top N similar items
            top_indices = similarities.argsort()[-n_results:][::-1]
            
            # Prepare results
            results = []
            for idx in top_indices:
                # Skip items with very low similarity
                if similarities[idx] < 0.01:
                    continue
                    
                results.append({
                    'name': str(self.df.iloc[idx]['name']),
                    'brand': str(self.df.iloc[idx]['brand']),
                    'price': float(self.df.iloc[idx]['price']),
                    'image_url': str(self.df.iloc[idx]['img']),
                    'similarity_score': float(similarities[idx]),
                    'description': str(self.df.iloc[idx]['description'])
                })
            
            print(f"Found {len(results)} results for query: {search_query}")
            return results
            
        except Exception as e:
            print(f"Error in search_similar_items: {e}")
            raise e

def main():
    """Test function"""
    # Load the dataset
    df = pd.read_csv('../dataset/Fashion Dataset.csv')
    
    # Initialize recommender
    recommender = FashionRecommender(df)
    
    # Test search
    test_query = "black dress with floral print"
    results = recommender.search_similar_items(test_query)
    
    # Print results
    print(f"\nSearch Query: {test_query}\n")
    for i, result in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"Product: {result['name']}")
        print(f"Brand: {result['brand']}")
        print(f"Price: ₹{result['price']:,.2f}")
        print(f"Similarity Score: {result['similarity_score']:.3f}")
        print("-" * 80)

if __name__ == "__main__":
    main()
