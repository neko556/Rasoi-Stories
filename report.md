# Project Report: Rasoi Stories 🍲

This report details the design, development, and strategic planning for the Rasoi Stories application, created in alignment with the viswam.ai project guidelines.

## 1.1. Team Information

* **Team Name:** [Team zzz]
* **Team Members:**
    * **Member 1:** [Dhanush]
   
## 1.2. Application Overview

**Rasoi Stories** is a community-driven digital cookbook designed to preserve and share India's vast and diverse culinary heritage. The application addresses the cultural problem of treasured, often undocumented, family recipes being lost over time. It provides users with a simple and beautiful platform to archive their recipes in their native languages, complete with the personal stories and traditions that make them special.

The core mission is to create a living, crowd-sourced museum of authentic Indian flavors, accessible to everyone. For the one-week development sprint, the team focused on a streamlined **Minimum Viable Product (MVP)**. The MVP's scope was deliberately centered on the essential user loop:
1.  **Submit a Recipe:** A simple form allowing users to input recipe details and a photo.
2.  **Browse & Discover:** A gallery view to explore all submitted recipes.
3.  **Engage:** The ability to upvote popular recipes.

This tight focus ensures a robust and functional core application, laying a strong foundation for future features and community growth.

## 1.3. AI Integration Details

The AI integration in Rasoi Stories is designed to be a practical utility that directly enhances the user's cooking experience, rather than a purely experimental feature.

* **AI Feature:** Smart Ingredient Substitute.
* **Problem Solved:** This feature addresses the common real-world scenario where a cook is missing a specific ingredient required by a recipe. It provides relevant, context-aware alternatives.
* **Open-Source Model:** We utilized the `paraphrase-multilingual-MiniLM-L12-v2` model from the open-source `sentence-transformers` library. This model was chosen for its strong performance in understanding semantic similarity across multiple languages while being efficient enough to run on standard cloud infrastructure.
* **Implementation:**
    1.  A curated list of common Indian ingredients is maintained in a file (`ingredients.txt`).
    2.  At application startup, the AI model computes and caches the vector embeddings for this entire list. This pre-computation is a key performance optimization.
    3.  When a user requests a substitute for an ingredient, the model computes the vector for that specific ingredient.
    4.  It then uses **Cosine Similarity** to find the vectors from the cached list that are closest in the semantic space.
    5.  The ingredients corresponding to these closest vectors are presented to the user as recommended substitutes (e.g., suggesting "tamarind paste" or "amchur powder" for "kokum").

## 1.4. Technical Architecture & Development

The application was architected for rapid development, ease of deployment, and performance, in line with the project's accelerated timeline.

* **Frontend Framework:** **Streamlit** was used for the entire user interface. Its Python-native approach allowed our team to build a reactive, interactive web application without needing to write separate HTML, CSS, or JavaScript, drastically speeding up development.
* **Backend & Database:** We chose **SQLite** as our database. As a serverless, file-based database, it eliminated the need for a separate database server, simplifying both development and deployment. The entire database is contained within a single `rasoi.db` file, making the project self-contained. The data schema consists of a single `recipes` table to store all recipe information.
* **Deployment Platform:** The application is deployed on **Hugging Face Spaces**. This platform offers seamless integration with Streamlit and provides the necessary computational resources to run both the web app and the AI models.
* **Key Development Strategy (Offline-First):** A core requirement was offline-first functionality. This was achieved through:
    * **Submission Queuing:** Using Streamlit's `st.session_state`, recipes submitted offline are added to a temporary queue. A user can then "sync" this queue to the main database once connectivity is restored.
    * **Aggressive Caching:** Streamlit's caching decorators (`@st.cache_data` and `@st.cache_resource`) are used extensively to cache database queries and loaded AI models. This ensures that the app feels fast and responsive after the initial load, even on low-bandwidth connections.

## 1.5. User Testing & Feedback (Week 2 Plan)

The objective for Week 2 is to rigorously test the MVP with a target user group to validate its functionality, usability, and performance.

* **Methodology:**
    1.  **Recruitment:** We will recruit a small, diverse group of 5-10 beta testers. This group will include friends and family members with varying levels of technical proficiency, as well as active members from online food and recipe communities to get expert feedback.
    2.  **Task-Based Testing:** Testers will be given a set of specific tasks to perform, designed to cover all core features of the MVP. These tasks include:
        * Submitting a new recipe, including uploading a photo.
        * Searching for a specific recipe.
        * Using the "Smart Ingredient Substitute" feature on at least two different ingredients.
        * Upvoting a recipe.
        * **Crucially, attempting to submit a recipe while their device's internet is disconnected to test the offline queuing feature.**
    3.  **Feedback Collection:** Feedback will be collected via a structured Google Form. The form will contain a mix of quantitative questions (e.g., "On a scale of 1-5, how easy was it to submit a recipe?") and qualitative, open-ended questions (e.g., "What was the most confusing part of the app?", "Did you encounter any bugs or errors?", "What features would you like to see next?"). This structured feedback will be analyzed to create a prioritized list of bugs and improvements for the iteration cycle.