from llama_index.vector_stores.types import(
    VectorStore,
    VectorStoreQuery,
    VectorStoreQueryResult,
)
from typing import List, Any, Optional, Dict
from llama_index.schema import TextNode, BaseNode

class BaseVectorStore(VectorStore):

    stores_text: bool = True

    def get(self, id: str) -> List[float]:
        """ Get embeddings."""
        pass

    def add(self, nodes: List[BaseNode]) -> List[str]:
        """ Add node to index."""
        pass

