from langchain_openai import AzureOpenAIEmbeddings, \
   AzureChatOpenAI  # Import classes for Azure OpenAI embeddings and chat
import os  # Import the os module to interact with the operating system
import numpy as np  # Import numpy for numerical operations


# Set the OpenAI API key as an environment variable
os.environ['OPENAI_API_KEY'] = 'e05202e4665242a9aa5f75ff4e1ca082'

# Define a function to calculate cosine similarity between two vectors
def cosine_similarity(vec1, vec2):
   # Cosine similarity measures the cosine of the angle between two vectors
   # It is a measure of similarity between two non-zero vectors
   return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# Define the main function that will run the program
def main():
   # Retrieve the OpenAI API key from the environment variables
   openai_api_key = os.environ.get('OPENAI_API_KEY')


   # Check if the API key is not set
   if not openai_api_key:
       # Raise an error if the API key is not found
       raise ValueError("Please set the OPENAI_API_KEY environment variable.")


   # Initialize the Azure OpenAI Embedding model with the API key and other parameters
   embedding_function = AzureOpenAIEmbeddings(
       openai_api_key=openai_api_key,  # API key for authentication
       api_version="2024-03-01-preview",  # API version
       base_url="https://flexapimanager.flex.com/openai/v2",  # Base URL for the API
       default_headers={"Ocp-Apim-Subscription-Key": openai_api_key},  # Headers for the API request
       model="embedding"  # Model type
   )


   # List of words for which we want to get embeddings
   words = ["apple", "train", "travel"]


   # Get embeddings for each word and store them in a dictionary
   embeddings = {word: embedding_function.embed_query(word) for word in words}


   # Print the embeddings for each word
   for word, vector in embeddings.items():
       # Print the first 5 elements of the embedding vector for each word
       print(f"Vector for '{word}': {vector[:5]}...")


   # Compare the embeddings of each pair of words
   for i, word1 in enumerate(words):
       for word2 in words[i + 1:]:
           # Calculate the cosine similarity between the embeddings of the two words
           similarity = cosine_similarity(embeddings[word1], embeddings[word2])
           # Print the similarity score
           print(f"Similarity between '{word1}' and '{word2}': {similarity}")




# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
   # Call the main function to run the program
   main()
