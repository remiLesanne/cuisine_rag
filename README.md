# cuisine_rag
construction d'un rag pour aider dans la préparation culinaire

## How to use

1.  **Start the services**:
    ```bash
    docker-compose up -d --build
    ```

2.  **Clean and Ingest Data** (if not already done):
    You can run these scripts locally or inside the `rag_engine` container.
    ```bash
    # Locally (requires python env)
    python rag_engine/clean.py
    python rag_engine/ingest_qdrant.py
    ```

3.  **Access the Application**:
    Open your browser and go to:
    [http://localhost:8000](http://localhost:8000)

4.  **API Documentation**:
    You can access the automatic API documentation at:
    [http://localhost:8000/docs](http://localhost:8000/docs)

## Architecture

*   **`rag_engine/`**: Contains the core logic for data processing and searching.
    *   `clean.py`: Prepares data and generates embeddings.
    *   `ingest_qdrant.py`: Loads data into Qdrant.
    *   `search_qdrant.py`: Defines the `RagEngine` class for searching.
*   **`api/`**: FastAPI application serving the RAG engine and frontend.
    *   `main.py`: API endpoints.
    *   `static/index.html`: Simple web interface.
*   **`data/`**: Stores raw recipes and processed pickle files.
*   **`qdrant_storage/`**: Persisted data for the Vector DB.
