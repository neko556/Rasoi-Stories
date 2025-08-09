# Rasoi Stories 🍲

**A community-driven digital cookbook designed to preserve and share India's vast and diverse culinary heritage, one family recipe at a time.**

[Image of the Rasoi Stories Streamlit app user interface]

Rasoi Stories provides a simple platform for users to archive their treasured family recipes in their native language. It's more than just a recipe app; it's a living museum of flavors, techniques, and the cultural memories embedded in our food.

---

## ✨ Key Features

* **Recipe Submission:** An easy-to-use form to submit recipes with names, stories, ingredients, instructions, and photos.
* **Community Gallery:** Browse and discover authentic, hyper-regional dishes from across India.
* **Upvote System:** Engage with the community by upvoting your favorite recipes.
* **AI Ingredient Substitute:** Missing an ingredient? Our AI-powered assistant suggests relevant, practical alternatives.
* **Offline First:** Submit recipes even with a spotty internet connection. Your submissions are queued and synced automatically when you're back online.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Backend & Database:** Python & [SQLite](https://www.sqlite.org/index.html)
* **AI Model:** `paraphrase-multilingual-MiniLM-L12-v2` from [Sentence-Transformers](https://www.sbert.net/)
* **Deployment:** [Hugging Face Spaces](https://huggingface.co/spaces)

---

## 🚀 Getting Started

Follow these steps to run Rasoi Stories on your local machine.

### Prerequisites

* Python 3.9+
* An active internet connection (for the initial setup)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [your-repository-url]
    cd rasoi-stories
    ```

2.  **Create and activate a virtual environment:**
    * On Windows:
        ```powershell
        python -m venv .venv
        .\.venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        python -m venv .venv
        source .venv/bin/activate
        ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

Your web browser should automatically open with the application running!