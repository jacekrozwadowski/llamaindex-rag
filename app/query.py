import os
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers.fusion_retriever import FUSION_MODES
from pydantic import BaseModel, Field
from typing import List
from llama_index.program.openai import OpenAIPydanticProgram
from llama_index.core.extractors import PydanticProgramExtractor
from llama_index.core import (
    SimpleDirectoryReader,
    QueryBundle,
    get_response_synthesizer,
)
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.vector_stores.elasticsearch import (
    AsyncDenseVectorStrategy,
    AsyncBM25Strategy,
    AsyncRetrievalStrategy,
)
from app.loader import model_setup

from dotenv import load_dotenv

load_dotenv()


def custom_query(query, query_str):
    print("custom query", query)
    return query


def create_rrf_query_engine():
    vector_store_bm25 = ElasticsearchStore(
        index_name=os.environ["ES_INDEX"],
        es_url=os.environ["ES_URL"],
        es_user=os.environ["ES_USERNAME"],
        es_password=os.environ["ES_PASSWORD"],
        retrieval_strategy=AsyncBM25Strategy(),
    )

    vector_store = ElasticsearchStore(
        index_name=os.environ["ES_INDEX"],
        es_url=os.environ["ES_URL"],
        es_user=os.environ["ES_USERNAME"],
        es_password=os.environ["ES_PASSWORD"],
    )

    index_bm25 = VectorStoreIndex.from_vector_store(vector_store=vector_store_bm25)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    retriever = QueryFusionRetriever(
        [index_bm25.as_retriever(), index.as_retriever()],
        mode=FUSION_MODES.RECIPROCAL_RANK,
        similarity_top_k=5,
        num_queries=3,  # set this to 1 to disable query generation
        use_async=True,
        verbose=False,
        # query_gen_prompt="...",  # we could override the query generation prompt here
    )
    query_engine = RetrieverQueryEngine.from_args(retriever)
    return query_engine


def create_simple_query_engine():

    vector_store = ElasticsearchStore(
        index_name=os.environ["ES_INDEX"],
        es_url=os.environ["ES_URL"],
        es_user=os.environ["ES_USERNAME"],
        es_password=os.environ["ES_PASSWORD"],
    )

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    # build retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=5,
        vector_store_query_mode="default",
        alpha=None,
        doc_ids=None,
        vector_store_kwargs={
            # "es_filter": [{"match": {"content": "matrix"}}],
            "custom_query": custom_query,  # use this to see ES query
        },
    )

    query_engine = RetrieverQueryEngine(
        retriever=retriever, response_synthesizer=get_response_synthesizer()
    )
    return query_engine


def main():
    model_setup()
    query_engine = create_rrf_query_engine()
    # query_engine = create_simple_query_engine()

    while True:
        query = input("Enter a query (or 'done' to finish): ")
        if query == "done":
            break
        elif not query or query == "":
            print("No query!")
            continue

        response = query_engine.query(query)
        print(response)


if __name__ == "__main__":
    main()
