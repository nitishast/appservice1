import streamlit as st
import base64
from PIL import Image
import requests
from io import BytesIO

# Function to load an image from a URL
def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

# Function to encode the image to base64
def img_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Set page config
st.set_page_config(page_title="Multi-App Platform", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
    }
    .sidebar .sidebar-content {
        background-color: #FFFFFF;
    }
    .st-emotion-cache-1wbqy5l {
        padding-top: 1rem;
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 100%;
    }
    .app-card {
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.title("Multi-App Platform")

# Define apps
apps = [
    {"name": "Home", "description": "Landing page", "image_url": "https://cdn.usegalileo.ai/sdxl10/2012b728-996f-456c-9ee9-868a5b670a71.png"},
    {"name": "SQL", "description": "SQL LLM Agents - SQL DB query", "image_url": "https://cdn.usegalileo.ai/sdxl10/2012b728-996f-456c-9ee9-868a5b670a71.png"},
    {"name": "CSV", "description": "LLM + VectorDB - Embedding + Vector search", "image_url": "https://cdn.usegalileo.ai/sdxl10/251683a2-6145-4875-bbca-763ca0c848de.png"},
    {"name": "Word Document", "description": "LLM - Chunking + Knowledge Graph+ Cypher query", "image_url": "https://cdn.usegalileo.ai/sdxl10/f9cfac55-4535-4c07-a7d9-a75836a91fff.png"},
    {"name": "RAG-GPT", "description": "RAG - Embedding + Vector search", "image_url": "https://cdn.usegalileo.ai/sdxl10/c7eb655b-4061-4a13-ac0f-37f9a2dbf1d5.png"},
    {"name": "LLM Knowledge Graph", "description": "Knowledge graph + LLM - Cypher query", "image_url": "https://cdn.usegalileo.ai/sdxl10/1e898bb2-f13c-42d3-a803-5f9c78ba55b0.png"},
    {"name": "Knowledge Graph + LLM", "description": "LLM Agents - Chunking + Knowledge Graph + GraphDB", "image_url": "https://cdn.usegalileo.ai/sdxl10/e4218b76-22e6-4b62-9d65-1fd884c8e3af.png"},
    {"name": "Neo4j", "description": "Knowledge Graph + LLM - Cypher query + GraphDB", "image_url": "https://cdn.usegalileo.ai/sdxl10/6195c24f-180d-4f52-aaf2-a3abdcfb91d8.png"},
    {"name": "Chroma", "description": "SQLite", "image_url": "https://cdn.usegalileo.ai/sdxl10/b822c129-5e96-4903-879d-98d8435a14e5.png"},
]

# Navigation
st.sidebar.title("Navigation")
nav_options = [app["name"] for app in apps]
selected_nav = st.sidebar.radio("", nav_options)

# Function to display app content
def display_app_content(app_name):
    st.header(f"Welcome to {app_name}")
    st.write(f"This is the {app_name} application page.")
    # Add more content specific to each app here

# Main content
if selected_nav == "Home":
    st.header("Welcome to Our Multi-App Platform")
    st.write("This is the landing page for our versatile application suite. Here's what you can do:")

    # App cards
    col1, col2, col3, col4 = st.columns(4)

    for i, app in enumerate(apps[1:]):  # Skip the Home app
        with [col1, col2, col3, col4][(i) % 4]:
            st.image(app["image_url"], use_column_width=True)
            st.subheader(app["name"])
            st.write(app["description"])
            if st.button(f"Open {app['name']}", key=f"btn_{app['name']}"):
                st.session_state.selected_nav = app['name']
                st.experimental_rerun()

else:
    display_app_content(selected_nav)

# Handle navigation from image clicks
if 'selected_nav' in st.session_state:
    selected_nav = st.session_state.selected_nav
    del st.session_state.selected_nav
    display_app_content(selected_nav)

# Expand button (for demonstration, doesn't have functionality in this example)
st.button("Expand")