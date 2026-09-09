from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_file(filepath):
    """Read a single text file and return its stripped content as one string."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()

def load_lines(filepath):
    """Read a text file and return a list of non-empty stripped lines."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return [line for line in lines if line]

def main():
    # Step 1: Load the 5 documents from separate files
    doc_filenames = ["Doc1.txt", "Doc2.txt", "Doc3.txt", "Doc4.txt", "Doc5.txt"]
    documents = [load_file(fname) for fname in doc_filenames]

    # Step 2: Load queries from queries.txt
    queries = load_lines("queries.txt")

    # Step 3: Load the embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Step 4: Encode all documents into embeddings (done once)
    document_embeddings = model.encode(documents)

    results_output = []

    # Step 5: For each query, encode it and find the most relevant document
    for query in queries:
        query_embedding = model.encode([query])  # wrapped in a list -> 2D shape

        # Step 6: Compute cosine similarity between query and all documents
        similarities = cosine_similarity(query_embedding, document_embeddings)[0]

        # Step 7: Find index of the highest similarity score
        best_index = np.argmax(similarities)
        best_document_name = doc_filenames[best_index]
        best_document_text = documents[best_index]

        # Print to console
        print(f"Query: {query}")
        print(f"Retrieved Document: {best_document_name}")
        print(f"Content: {best_document_text}\n")

        # Store for results.txt
        results_output.append(
            f"Query: {query}\n\n"
            f"Retrieved Document: {best_document_name}\n"
            f"{best_document_text}\n\n---\n"
        )

    # Step 8: Save results to results.txt
    with open("results.txt", "w", encoding="utf-8") as f:
        f.writelines(results_output)

if __name__ == "__main__":
    main()