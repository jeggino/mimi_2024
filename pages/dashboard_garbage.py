import streamlit as st

import pandas as pd
import datetime

from deta import Deta

# --- CONFIGURATION ---


st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)

# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_garbage")

# --- COSTANTS ---


# --- FUNCTIONS ---
def load_dataset():
  return db.fetch().items


# --- APP ---
col_1,col_2 = st.columns([4,3])
db_content = load_dataset()
df = pd.DataFrame(db_content)
if len(df)==0:
    st.warning("No data yet")
    st.stop()
    
df_2 = df[["datum","location","operator","total","comment"]]
option = col_1.dataframe(data=df_2, width=None, height=None, use_container_width=True,
             hide_index=True, column_order=None, column_config=None, key=None, on_select="rerun", selection_mode="single-row")

try:
    a = df.loc[option["selection"]["rows"][0]]["dict_values"]
    df_3 = pd.DataFrame.from_dict(a, orient='index').stack().to_frame().rename(columns={0:"Ammount"})
    col_2.dataframe(df_3,use_container_width=True)
except:
    col_1.warning("Select a row")
    st.stop()

submitted = col_1.toggle("Delete observation",key="submitted_1",value=False)
if not submitted:
    st.stop()
    
col_1.warning("Are you sure you want to delete this observation?!")
submitted_2 = col_1.button("Yes I am sure!",key="submitted_2")
if submitted_2:
    id = df.loc[option["selection"]["rows"][0]]["key"]
    db.delete(id)
    st.rerun()
    
   
