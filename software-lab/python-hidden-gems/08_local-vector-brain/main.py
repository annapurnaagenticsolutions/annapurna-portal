"""
Project 08: Local Vector Brain

Hidden Gem: `chromadb` — embedded vector database that runs in-process.
No server, no API, no setup. Just `pip install chromadb` and go.

What it does: Stores text documents as vector embeddings and performs
semantic similarity search — all locally, no API keys needed.
"""
import chromadb
from chromadb.utils import embedding_functions


SAMPLE_DOCUMENTS = [
    "Python is a high-level programming language known for its readability and simplicity.",
    "Machine learning models can be trained to recognize patterns in large datasets.",
    "The Django framework is popular for building web applications in Python.",
    "Neural networks are inspired by the structure of the human brain.",
    "FastAPI is a modern Python framework for building APIs with automatic documentation.",
    "Vector databases store embeddings for semantic similarity search.",
    "Data structures like hash maps and trees are fundamental to computer science.",
    "Natural language processing enables computers to understand human language.",
    "Docker containers package applications with their dependencies for consistent deployment.",
    "The asyncio library enables concurrent programming in Python using coroutines.",
]


def main():
    print("--- Local Vector Brain ---")
    print("Setting up in-memory ChromaDB with default embeddings...\n")

    # Create an in-memory client (no persistence)
    client = chromadb.Client()

    # Use default sentence-transformer embeddings (downloads on first run)
    try:
        embed_fn = embedding_functions.DefaultEmbeddingFunction()
        collection = client.create_collection(
            name="knowledge",
            embedding_function=embed_fn,
        )
    except Exception as e:
        print(f"Could not initialize embeddings: {e}")
        print("ChromaDB requires the `sentence-transformers` package.")
        print("Install with: pip install chromadb")
        return

    # Add documents
    print(f"Adding {len(SAMPLE_DOCUMENTS)} documents...")
    collection.add(
        ids=[f"doc_{i}" for i in range(len(SAMPLE_DOCUMENTS))],
        documents=SAMPLE_DOCUMENTS,
        metadatas=[{"index": i} for i in range(len(SAMPLE_DOCUMENTS))],
    )
    print("✓ Documents indexed\n")

    # Query
    queries = [
        "What is Python good for?",
        "How do neural networks work?",
        "How to deploy applications?",
    ]

    for query in queries:
        print(f"Query: \"{query}\"")
        results = collection.query(query_texts=[query], n_results=3)

        for i, (doc, dist) in enumerate(zip(
            results['documents'][0],
            results['distances'][0]
        )):
            similarity = 1 - dist
            print(f"  {i+1}. [sim={similarity:.3f}] {doc[:80]}...")
        print()


if __name__ == "__main__":
    main()
