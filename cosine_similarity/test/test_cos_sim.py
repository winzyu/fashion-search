import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import ast

# Setup data (same as before)
data = {
    'name': [
        "Khushal K Women Black Ethnic Motifs Printed Kurta with Palazzos & With Dupatta",
        "InWeave Women Orange Solid Kurta with Palazzos & Floral Print Dupatta",
        "Anubhutee Women Navy Blue Ethnic Motifs Embroidered Thread Work Kurta with Trousers & With Dupatta",
        "Nayo Women Red Floral Printed Kurta With Trouser & Dupatta",
        "AHIKA Women Black & Green Printed Straight Kurta"
    ],
    'description': [
        "Black printed Kurta with Palazzos with dupatta Kurta design: Ethnic motifs printed Anarkali shape Regular style Mandarin collar, three-quarter regular sleeves",
        "Orange solid Kurta with Palazzos with dupatta Kurta design: Solid A-line shape Regular style Square neck, sleeveless shoulder straps",
        "Navy blue embroidered Kurta with Trousers with dupatta Kurta design: Ethnic motifs embroidered A-line shape Regular style Round neck",
        "Red printed kurta with trouser and dupatta Kurta design: Printed kurta Anarkali design Round neck Three-quarter sleeves",
        "Black and green printed straight kurta, has a nitched round neck, three-quarter sleeves, straight hem, side slits"
    ],
    'colour': ['Black', 'Orange', 'Navy Blue', 'Red', 'Black'],
    'p_attributes': [
        "{'Occasion': 'Festive', 'Print or Pattern Type': 'Ethnic Motifs', 'Top Shape': 'Anarkali'}",
        "{'Occasion': 'Fusion', 'Print or Pattern Type': 'Solid', 'Top Shape': 'A-Line'}",
        "{'Occasion': 'Daily', 'Print or Pattern Type': 'Ethnic Motifs', 'Top Shape': 'A-Line'}",
        "{'Occasion': 'Daily', 'Print or Pattern Type': 'Ethnic Motifs', 'Top Shape': 'Anarkali'}",
        "{'Occasion': 'Daily', 'Print or Pattern Type': 'Ethnic Motifs', 'Shape': 'Straight'}"
    ]
}

df = pd.DataFrame(data)

# Process attributes and combine features
def extract_attributes(attr_str):
    try:
        attr_dict = ast.literal_eval(attr_str)
        return f"{attr_dict.get('Occasion', '')} {attr_dict.get('Print or Pattern Type', '')} {attr_dict.get('Top Shape', '')}"
    except:
        return ''

df['combined_features'] = df.apply(lambda x: f"{x['description']} {x['colour']} {extract_attributes(x['p_attributes'])}", axis=1)

# Create TF-IDF vectors
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Sample queries
queries = [
    "black ethnic festive wear",
    "casual orange straight kurta",
    "daily wear solid color",
    "formal anarkali with embroidery"
]

# Function to show non-zero terms in vector
def show_vector_terms(vector, vocabulary):
    non_zero_indices = vector.nonzero()[1]
    terms = []
    for idx in non_zero_indices:
        term = [word for word, i in vocabulary.items() if i == idx][0]
        weight = vector[0, idx]
        terms.append(f"{term}: {weight:.4f}")
    return terms

# Print vocabulary
print("Vocabulary (term -> index mapping):")
sorted_vocab = sorted(tfidf.vocabulary_.items(), key=lambda x: x[1])
for term, idx in sorted_vocab:
    print(f"{idx}: {term}")

print("\nProduct TF-IDF Vectors (non-zero terms only):")
for i, row in enumerate(df['combined_features']):
    print(f"\nProduct {i+1}:")
    vector = tfidf_matrix[i]
    terms = []
    for idx in vector.nonzero()[1]:
        term = [word for word, i in tfidf.vocabulary_.items() if i == idx][0]
        weight = vector[0, idx]
        terms.append(f"{term}: {weight:.4f}")
    print("\n".join(terms))

print("\nQuery TF-IDF Vectors:")
for query in queries:
    print(f"\nQuery: '{query}'")
    query_vector = tfidf.transform([query])
    terms = show_vector_terms(query_vector, tfidf.vocabulary_)
    print("\n".join(terms))
