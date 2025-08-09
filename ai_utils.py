import streamlit as st
from sentence_transformers import SentenceTransformer, util
import torch

MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
# Add these imports at the top of ai_utils.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

# --- LLM Recommendation Model ---
#
LLM_MODEL_NAME = "google/gemma-2b-it"



@st.cache_resource
def load_model_and_data():
    """Loads the AI model and ingredient data. Cached for performance."""
    print("Loading AI model and data for the first time...")
    model = SentenceTransformer(MODEL_NAME)
    with open('ingredients.txt', 'r', encoding='utf-8') as f:
        ingredient_list = [line.strip() for line in f if line.strip()]
    
    # Pre-compute embeddings for the entire ingredient list - this is a key optimization
    ingredient_embeddings = model.encode(ingredient_list, convert_to_tensor=True)
    print("Model and data loaded successfully.")
    return model, ingredient_list, ingredient_embeddings

def get_substitutes(ingredient_name, model, ingredient_list, ingredient_embeddings):
    """Finds and returns the top 3 substitutes for a given ingredient."""
    if ingredient_name.lower() not in ingredient_list:
        return [f"Sorry, '{ingredient_name}' is not in our ingredients database yet."]

    # Encode the user's ingredient
    ingredient_to_find_embedding = model.encode(ingredient_name, convert_to_tensor=True)
    
    # Compute cosine similarity
    cosine_scores = util.cos_sim(ingredient_to_find_embedding, ingredient_embeddings)
    
    # Get the top 4 scores (top 1 will be the ingredient itself)
    top_results = torch.topk(cosine_scores, k=4)
    
    substitutes = []
    for i in range(1, 4): # Start from 1 to skip the ingredient itself
        idx = top_results.indices[0][i].item()
        substitutes.append(ingredient_list[idx])
        
    return substitutes