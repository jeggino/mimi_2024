import streamlit as st

st.sidebar.switch_page("dashboard.py", label="Home", icon="🏠")
st.sidebar.switch_page("pages/fish_dashboard.py", label="Fish")

st.write("Ciao peperone")
