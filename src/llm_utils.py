import os
import sys
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from langchain_core.language_models.llms import LLM
from langchain_community.embeddings import HuggingFaceEmbeddings

# Add the parent directory to sys.path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv()

class HuggingFaceInferenceLLM(LLM):
    """Custom LLM that uses the Hugging Face Inference API directly."""
    
    def __init__(self, api_key, model_name="mistralai/Mistral-7B-Instruct-v0.2"):
        """Initialize with API key and model name."""
        super().__init__()
        self.api_key = api_key
        self.model_name = model_name
        self.client = InferenceClient(token=api_key)
    
    def _call(self, prompt, **kwargs):
        """Call the Hugging Face Inference API."""
        try:
            # Use the text-generation endpoint directly
            response = self.client.text_generation(
                prompt,
                model=self.model_name,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True
            )
            return response
        except Exception as e:
            print(f"Error calling Hugging Face API: {str(e)}")
            return f"Error: {str(e)}"

class LLMManager:
    """Manages LLM model initialization and usage."""
    
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.2", embedding_model="sentence-transformers/all-mpnet-base-v2"):
        """Initialize LLM and embedding models.
        
        Args:
            model_name: Name of the model to use with HuggingFace Inference API
            embedding_model: HuggingFace model name for embeddings
        """
        self.model_name = model_name
        self.embedding_model_name = embedding_model
        self.llm = None
        self.embeddings = None
        
        # Initialize models
        self._initialize_llm()
        self._initialize_embeddings()
    
    def _initialize_llm(self):
        """Initialize the model through HuggingFace Inference API."""
        try:
            # Get API token from environment variable
            huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
            if not huggingface_api_key:
                raise ValueError("HUGGINGFACE_API_KEY environment variable not set")
                
            self.llm = HuggingFaceInferenceLLM(
                api_key=huggingface_api_key,
                model_name=self.model_name
            )
        except Exception as e:
            print(f"Error initializing HuggingFace LLM: {str(e)}")
            
    def _initialize_embeddings(self):
        """Initialize the embedding model."""
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
        except Exception as e:
            print(f"Error initializing embeddings: {str(e)}")
            
    def generate_text(self, prompt, max_tokens=1000):
        """Generate text with the LLM."""
        if not self.llm:
            raise ValueError("LLM not initialized")
        
        return self.llm.invoke(prompt)
    
    def get_embeddings(self, texts):
        """Get embeddings for the given texts."""
        if not self.embeddings:
            raise ValueError("Embeddings model not initialized")
        
        return self.embeddings.embed_documents(texts)