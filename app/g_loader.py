import re
from dotenv import load_dotenv
import nest_asyncio

nest_asyncio.apply()

from typing import Any
from llama_index.core import PropertyGraphIndex
from app.g_common import get_logger, GraphRAGExtractor, GraphRAGStore
from app.loader import model_setup, load_data

load_dotenv()

log = get_logger("GraphRag Loader")


def main():

    llm, embed_model = model_setup()

    kg_triplet_extract_tmpl = """
    -Goal-
    Given a text document, identify all entities and their entity types from the text and all relationships among the identified entities.
    Given the text, extract up to {max_knowledge_triplets} entity-relation triplets.
    
    -Steps-
    1. Identify all entities. For each identified entity, extract the following information:
    - entity_name: Name of the entity, capitalized
    - entity_type: Type of the entity
    - entity_description: Comprehensive description of the entity's attributes and activities
    Format each entity as ("entity"$$$$<entity_name>$$$$<entity_type>$$$$<entity_description>)
    
    2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
    For each pair of related entities, extract the following information:
    - source_entity: name of the source entity, as identified in step 1
    - target_entity: name of the target entity, as identified in step 1
    - relation: relationship between source_entity and target_entity
    - relationship_description: explanation as to why you think the source entity and the target entity are related to each other
    
    Format each relationship as ("relationship"$$$$<source_entity>$$$$<target_entity>$$$$<relation>$$$$<relationship_description>)
    
    3. When finished, output only the extracted entities and relationships without including the steps.
    
    -Real Data-
    ######################
    text: {text}
    ######################
    output:"""

    entity_pattern = r'\("entity"\$\$\$\$(.+?)\$\$\$\$(.+?)\$\$\$\$(.+?)\)'
    relationship_pattern = (
        r'\("relationship"\$\$\$\$(.+?)\$\$\$\$(.+?)\$\$\$\$(.+?)\$\$\$\$(.+?)\)'
    )

    def parse_fn(response_str: str) -> Any:
        entities = re.findall(entity_pattern, response_str)
        relationships = re.findall(relationship_pattern, response_str)
        return entities, relationships

    #
    kg_extractor = GraphRAGExtractor(
        llm=llm,
        extract_prompt=kg_triplet_extract_tmpl,
        max_paths_per_chunk=2,
        parse_fn=parse_fn,
    )

    log.info("GraphRAGStore start")
    graph_store = GraphRAGStore(
        username="neo4j", password="password", url="bolt://localhost:7687"
    )
    graph_store.set_llm_client(llm)
    graph_store.verify_version()
    log.info("GraphRAGStore end")

    # load documents
    nodes = load_data("./documents")
    log.info(f"No of nodes {len(nodes)}")

    log.info("Create new PropertyGraphIndex")
    # clean neo4j
    # kg_triplet_extract_tmpl
    index = PropertyGraphIndex(
        llm=llm,
        embed_model=embed_model,
        nodes=nodes,
        kg_extractors=[kg_extractor],
        property_graph_store=graph_store,
        show_progress=True,
        use_async=True,
    )


if __name__ == "__main__":
    main()
