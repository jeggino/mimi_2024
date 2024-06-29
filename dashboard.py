import streamlit as st
from streamlit_player import st_player


# --- CONFIGURATION ---
st.set_page_config(
    page_title="dashboard",
    page_icon="🌊",
    layout="wide",
    
)

st.logo("https://i.pinimg.com/originals/01/ca/da/01cada77a0a7d326d85b7969fe26a728.jpg", link="https://streamlit.io/gallery", icon_image="https://cdn3.iconfinder.com/data/icons/nature-animals/512/Bird-1024.png")


st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)


st.sidebar.page_link("dashboard.py", label="", icon="🏠")
st.sidebar.page_link("pages/fish_dashboard.py", label="", icon="🐟")
st.sidebar.page_link("pages/dashboard_garbage.py", label="", icon="🗑️")

# Embed a youtube video
st_player("https://www.youtube.com/watch?v=CHa8c-xUHlI")
