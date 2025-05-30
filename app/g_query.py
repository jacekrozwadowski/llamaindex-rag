from dotenv import load_dotenv
import nest_asyncio

nest_asyncio.apply()
from llama_index.core import PropertyGraphIndex
from app.g_common import (
    get_logger,
    GraphRAGStore,
    GraphRAGQueryEngine,
)
from app.loader import model_setup

load_dotenv()

log = get_logger("GraphRag Query")


def main():

    llm, embed_model = model_setup()

    log.info("GraphRAGStore start")
    graph_store = GraphRAGStore(
        username="neo4j", password="password", url="bolt://localhost:7687"
    )
    graph_store.set_llm_client(llm)
    graph_store.verify_version()
    log.info("GraphRAGStore end")

    log.info("Create index from existing graph")
    index = PropertyGraphIndex.from_existing(
        property_graph_store=graph_store, use_async=True
    )

    log.info("Build communities")
    index.property_graph_store.build_communities()

    log.info("Build GraphRAGQueryEngine")
    query_engine = GraphRAGQueryEngine(
        graph_store=index.property_graph_store,
        llm=llm,
        index=index,
        similarity_top_k=10,
    )

    query_list = [
        "Czym różni się Agile od Scrum'a?",
        "Co to jest Agile?",
        "Co to jest Sprint?",
        "Jak duży powinien być zespół w Scrum?",
        "Jak duży powinien być zespół w Agile?",
        "Jakie jest zadanie Scrum Master'a?",
        "Jakie jest zadanie Product Owner'a?",
    ]

    for query in query_list:
        log.info(f"Query: \n {query}")
        response = query_engine.query(query)
        log.info(f"Answer: \n {response}")


if __name__ == "__main__":
    main()
