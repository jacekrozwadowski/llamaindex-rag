import os
from pydantic import BaseModel, Field
from typing import List
from llama_index.program.openai import OpenAIPydanticProgram
from llama_index.core.extractors import PydanticProgramExtractor
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.core import StorageContext, VectorStoreIndex
from typing import List

from llama_index.core.node_parser import (
    SemanticDoubleMergingSplitterNodeParser,
    LanguageConfig,
)
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
from llama_index.vector_stores.elasticsearch import ElasticsearchStore


load_dotenv()


def model_setup():
    # Create LLM and Embedding
    llm = OpenAI(model="gpt-4.1-nano")
    Settings.llm = llm

    embed_model = OpenAIEmbedding(
        model=OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL, embed_batch_size=10
    )
    Settings.embed_model = embed_model


def load_data(input_dir):
    class PolishLanguageConfig(LanguageConfig):
        def __init__(
            self,
            language: str = "english",
            spacy_model: str = "en_core_web_md",
            model_validation: bool = True,
        ):
            self.language = language
            self.spacy_model = spacy_model
            self.nlp = None
            self.stopwords: List[str] = []

    documents = SimpleDirectoryReader(input_dir=input_dir).load_data(show_progress=True)

    config = PolishLanguageConfig(language="polish", spacy_model="pl_core_news_md")
    splitter = SemanticDoubleMergingSplitterNodeParser(
        language_config=config,
        initial_threshold=0.4,
        appending_threshold=0.5,
        merging_threshold=0.5,
        max_chunk_size=2048,
    )

    nodes = splitter.get_nodes_from_documents(documents, show_progress=True)
    return nodes


def extract_metadata(nodes):
    class NodeMetadata(BaseModel):
        """Node metadata."""

        entities: List[str] = Field(
            ..., description="Unique entities in this text chunk."
        )
        summary: str = Field(
            ...,
            default_factory=lambda x: "<empty>",
            description="A concise summary of this text chunk. In summary use original language of text.",
        )

    extract_template_str = """\
    Here is the content of the section:
    ----------------
    {context_str}
    ----------------
    Given the contextual information, extract out a {class_name} object. Keep original language of text. \
    """

    # Metadata extraction
    openai_program = OpenAIPydanticProgram.from_defaults(
        output_cls=NodeMetadata,
        prompt_template_str="{input}",
        extract_template_str=extract_template_str,
    )

    metadata_extractor = PydanticProgramExtractor(
        program=openai_program, input_key="input", show_progress=True
    )

    metadata_nodes = metadata_extractor.process_nodes(nodes)

    # add some specific info into metadata
    # for md in metadata_nodes:
    #     metadata = md.metadata
    #     metadata['tags'] = ['t1','t2']

    return metadata_nodes


def load_es(nodes):
    vector_store = ElasticsearchStore(
        index_name=os.environ["ES_INDEX"],
        es_url=os.environ["ES_URL"],
        es_user=os.environ["ES_USERNAME"],
        es_password=os.environ["ES_PASSWORD"],
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(nodes, storage_context=storage_context)
    return index


def main():
    model_setup()
    orig_nodes = load_data(input_dir="./documents")
    metadata_nodes = extract_metadata(orig_nodes)
    # print(metadata_nodes[0].get_content(metadata_mode="all"))
    load_es(metadata_nodes)


if __name__ == "__main__":
    main()
