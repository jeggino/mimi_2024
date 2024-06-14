import streamlit as st

st.sidebar.page_link("dashboard.py", label="Home")
st.page_link("pages/fish_dashboard.py", label="Fish")

st.write("Ciao peperone")
