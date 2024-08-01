# extract.py
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Azure OpenAI configurations
os.environ['OPENAI_API_KEY'] = 'e05202e4665242a9aa5f75ff4e1ca082'
AZURE_ENDPOINT = "https://flexapimanager.flex.com/openai/v2"
API_VERSION = "2024-03-01-preview"
EMBEDDING_DEPLOYMENT = "embedding"
CHAT_DEPLOYMENT = "chat"

# Define constants for paths and settings
CHROMA_PATH = "chroma"
CORPORATE_ASS_TXT = "corporate_assessment.txt"

# Default prompt template for the chat model
DEFAULT_PROMPT_TEMPLATE = """
Answer the question based only on the following context: {context}
---
Answer the question based on the above context:
{question}
"""

def query_data(query_text, prompt_template):
    # Initialize the Azure Embedding model
    embedding_function = AzureOpenAIEmbeddings(
        openai_api_key="e05202e4665242a9aa5f75ff4e1ca082",
        api_version="2024-03-01-preview",
        base_url="https://flexapimanager.flex.com/openai/v2",
        default_headers={"Ocp-Apim-Subscription-Key": "e05202e4665242a9aa5f75ff4e1ca082"},
        model="embedding"
    )

    # Initialize the Chroma database with the embedding function
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Perform a similarity search in the Chroma database
    results = db.similarity_search_with_relevance_scores(query_text, k=12)
    if len(results) == 0 or results[0][1] < 0.45:
        return "Unable to find matching results.", ""

    # Concatenate the content of the top results to form the context text
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Return the context text for the first output box
    vector_search_output = context_text

    # Format the prompt using the provided template and context text
    prompt_template = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Initialize the Azure Chat model
    model = AzureChatOpenAI(
        streaming=True,
        model_name="gpt-4o",
        openai_api_key="e05202e4665242a9aa5f75ff4e1ca082",
        api_version="2024-03-01-preview",
        base_url="https://flexapimanager.flex.com/openai/v2",
        default_headers={"Ocp-Apim-Subscription-Key": "e05202e4665242a9aa5f75ff4e1ca082"}
    )

    # Get the response from the chat model
    response_text = model.predict(prompt)

    # Extract the sources from the metadata of the results
    sources = [doc.metadata.get("source", None) for doc, _score in results]

    # Format the response with the sources
    formatted_response = f"Response: {response_text}\nSources: {sources}"

    # Return both the vector search output and the formatted response
    return vector_search_output, formatted_response