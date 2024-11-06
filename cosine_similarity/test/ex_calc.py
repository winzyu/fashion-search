import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Let's do this step by step
print("Step-by-Step Cosine Similarity Calculation")
print("-----------------------------------------")

# 1. Create simplified example with just our query and first product
texts = [
    # Our first product's combined features
    "Black printed Kurta with Palazzos with dupatta Kurta design: Ethnic motifs printed Anarkali shape Regular style Mandarin collar Black Festive Ethnic Motifs Anarkali",
    # Our query
    "black ethnic anarkali"
]

# 2. Create and fit TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
vectors = tfidf.fit_transform(texts)

# 3. Show the vocabulary and vectors
vocabulary = tfidf.vocabulary_
print("\n1. Vocabulary (word -> index mapping):")
print(vocabulary)

# Get vectors as arrays
product_vector = vectors[0].toarray()[0]
query_vector = vectors[1].toarray()[0]

# 4. Show non-zero terms and their weights
def show_vector_weights(vector, vocabulary):
    word_weights = []
    for word, idx in vocabulary.items():
        if vector[idx] != 0:
            word_weights.append((word, vector[idx]))
    return sorted(word_weights, key=lambda x: x[1], reverse=True)

print("\n2. Product vector non-zero weights:")
for word, weight in show_vector_weights(product_vector, vocabulary):
    print(f"{word}: {weight:.4f}")

print("\n3. Query vector non-zero weights:")
for word, weight in show_vector_weights(query_vector, vocabulary):
    print(f"{word}: {weight:.4f}")

# 5. Calculate cosine similarity manually
def cosine_sim_manual(v1, v2):
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    return dot_product / (norm1 * norm2)

similarity = cosine_sim_manual(product_vector, query_vector)

print(f"\n4. Cosine Similarity Calculation:")
print(f"Dot product: {np.dot(product_vector, query_vector):.4f}")
print(f"Product vector norm: {np.linalg.norm(product_vector):.4f}")
print(f"Query vector norm: {np.linalg.norm(query_vector):.4f}")
print(f"Final similarity: {similarity:.4f}")
