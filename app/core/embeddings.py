from sentence_transformers import SentenceTransformer
import logging
from config import MODEL_NAME

logger = logging.getLogger(__name__)

# Initialize the model
model = SentenceTransformer(MODEL_NAME)

def generate_embedding(text: str):
    """Generate embedding vector for the given text."""
    try:
        return model.encode(text)
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        raise