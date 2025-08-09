import streamlit as st
from PIL import Image
import os

# Import your custom modules
import database
import ai_utils

# --- App Configuration ---
st.set_page_config(page_title="Rasoi Stories", page_icon="🍲", layout="wide")

# --- Initialize Database & AI Model ---
database.setup_database()
model, ingredient_list, ingredient_embeddings = ai_utils.load_model_and_data()

# --- Initialize Session State for Offline Queue ---
if 'submission_queue' not in st.session_state:
    st.session_state.submission_queue = []

# --- Helper Function to Save Uploaded File ---
def save_uploaded_file(uploaded_file):
    # Ensure 'uploads' directory exists
    os.makedirs("uploads", exist_ok=True)
    # Save the file
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# --- Sidebar for Navigation ---
st.sidebar.title("🍲 Rasoi Stories")
app_mode = st.sidebar.selectbox("Choose a Page", ["Home", "Add a Recipe", "Recommend","Offline Submissions"])

# --- OFFLINE SUBMISSIONS PAGE ---
if app_mode == "Offline Submissions":
    st.header("Pending Submissions")
    if not st.session_state.submission_queue:
        st.info("Your offline submission queue is empty.")
    else:
        st.warning(f"You have {len(st.session_state.submission_queue)} recipe(s) waiting to be synced.")
        if st.button("Sync Now"):
            with st.spinner("Syncing..."):
                for recipe_data in st.session_state.submission_queue:
                    database.add_recipe(**recipe_data)
                st.session_state.submission_queue = [] # Clear the queue
                st.success("All pending recipes have been synced!")
                st.rerun()

# --- ADD A RECIPE PAGE ---
elif app_mode == "Add a Recipe":
    st.header("Share Your Family Recipe")
    
    with st.form("recipe_form", clear_on_submit=True):
        name = st.text_input("Recipe Name *")
        region = st.text_input("Region / State (e.g., Punjab, Kerala)")
        story = st.text_area("Story behind the dish (optional)")
        ingredients = st.text_area("Ingredients (one per line) *")
        instructions = st.text_area("Instructions *")
        photo = st.file_uploader("Upload a photo of your dish", type=["jpg", "png", "jpeg"])
        
        submitted = st.form_submit_button("Submit Recipe")
        
        if submitted:
            if not name or not ingredients or not instructions:
                st.error("Please fill in all required fields (*).")
            else:
                photo_filename = None
                if photo:
                    # Compress and save the image
                    image = Image.open(photo)
                    image.thumbnail((800, 800)) # Resize image
                    photo_filename = save_uploaded_file(photo)

                # Add to offline queue instead of directly to DB
                recipe_data = {
                    "name": name, "region": region, "story": story,
                    "ingredients": ingredients, "instructions": instructions,
                    "photo_filename": photo_filename
                }
                st.session_state.submission_queue.append(recipe_data)
                st.success(f"Recipe '{name}' added to your offline queue! Go to 'Offline Submissions' to sync.")



else:
    st.title("The People's Cookbook of India")
    
    # --- Search Bar ---
    search_query = st.text_input("Search for a recipe")
    
    recipes_df = database.get_all_recipes()
    
    # Filter based on search query
    if search_query:
        recipes_df = recipes_df[recipes_df['name'].str.contains(search_query, case=False)]

    if recipes_df.empty:
        st.info("No recipes found. Be the first to add one!")
    else:
        for index, row in recipes_df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if row['photo_filename'] and os.path.exists(row['photo_filename']):
                        st.image(row['photo_filename'], use_column_width=True)
                
                with col2:
                    st.subheader(row['name'])
                    st.caption(f"From {row['region']}")
                    
                    # Upvote button
                    if st.button(f"🍲 Upvote ({row['upvotes']})", key=f"upvote_{row['id']}"):
                        database.upvote_recipe(row['id'])
                        st.success(f"You upvoted {row['name']}!")
                        st.rerun()

                    with st.expander("Read Full Recipe"):
                        st.markdown(f"**Story:**\n\n_{row['story']}_")
                        st.markdown("**Ingredients:**")
                        st.code(row['ingredients'])
                        st.markdown("**Instructions:**")
                        st.text(row['instructions'])
                        
                        st.markdown("**Find Ingredient Substitutes (AI-Powered):**")
                        # Allow user to select an ingredient from this recipe to find a substitute
                        recipe_ingredients = [ing.strip() for ing in row['ingredients'].split('\n') if ing.strip()]
                        selected_ingredient = st.selectbox("Select an ingredient:", options=recipe_ingredients, key=f"select_{row['id']}")
                        
                        if st.button("Find Substitute", key=f"sub_{row['id']}"):
                            with st.spinner("AI is thinking..."):
                                substitutes = ai_utils.get_substitutes(selected_ingredient, model, ingredient_list, ingredient_embeddings)
                                st.success(f"Substitutes for **{selected_ingredient}**: {', '.join(substitutes)}")