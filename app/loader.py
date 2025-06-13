import os

import httpx
from pydantic import BaseModel, Field
from llama_index.program.openai import OpenAIPydanticProgram
from llama_index.core.extractors import PydanticProgramExtractor
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.core import StorageContext, VectorStoreIndex
from typing import List
from pathlib import Path

from llama_index.core.node_parser import (
    SemanticDoubleMergingSplitterNodeParser,
    LanguageConfig,
)
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
from llama_index.vector_stores.elasticsearch import ElasticsearchStore


load_dotenv()


# def onprem_model_setup():
#     from llama_index.llms.openai_like import OpenAILike
#     from llama_index.embeddings.openai_like import OpenAILikeEmbedding
#
#     llm = OpenAILike(
#         model="<model>",
#         api_base="http://...../../v1",
#         api_key="fake",
#         is_chat_model=True,
#         is_function_calling_model=True,
#         http_client=httpx.Client(verify=False),
#         async_http_client=httpx.AsyncClient(verify=False),
#     )
#
#     embed_model=OpenAILikeEmbedding(
#         model="<model>",
#         api_base="http://.....",
#         api_key="fake",
#         embed_batch_size=10,
#         http_client=httpx.Client(verify=False),
#         async_http_client=httpx.AsyncClient(verify=False),
#     )
#
#     Settings.llm = llm
#     Settings.embed_model = embed_model
#     return llm, embed_model


def model_setup():
    # Create LLM and Embedding
    llm = OpenAI(model="gpt-4.1-nano")
    Settings.llm = llm

    embed_model = OpenAIEmbedding(
        model=OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL, embed_batch_size=10
    )
    Settings.embed_model = embed_model

    return llm, embed_model


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

    documents = SimpleDirectoryReader(input_dir=input_dir, recursive=True).load_data(
        show_progress=True
    )

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


def extract_metadata(nodes, input_dir=None):
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
    if input_dir:
        for md in metadata_nodes:
            metadata = md.metadata
            file_path = metadata.get("file_path", None)
            if file_path:
                _, file_uri = file_path.split(input_dir)
                file_path_parts = list(Path(file_uri).parts[1:-1])
                file_path_parts = [p.lower() for p in file_path_parts]
                if file_path_parts and len(file_path_parts) > 0:
                    metadata["tags"] = file_path_parts

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
    doc_path = "documents"
    orig_nodes = load_data(input_dir=doc_path)
    metadata_nodes = extract_metadata(orig_nodes, input_dir=doc_path)
    # print(metadata_nodes[0].get_content(metadata_mode="all"))
    load_es(metadata_nodes)


if __name__ == "__main__":
    main()
