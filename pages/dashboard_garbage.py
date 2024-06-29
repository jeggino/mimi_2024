import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import datetime

import plotly.express as px

from deta import Deta

# --- CONFIGURATION ---
st.set_page_config(
    page_title="dashboard",
    page_icon="🌊",
    layout="wide",
    
)


choose = option_menu(menu_title=None, options = ["Observations", "Sunburst chart"],
                     icons=['book','kanban'],
                     orientation = "horizontal"
                     )
    


st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)

st.sidebar.page_link("dashboard.py", label="", icon="🏠")
st.sidebar.page_link("pages/fish_dashboard.py", label="", icon="🐟")
st.sidebar.page_link("pages/dashboard_garbage.py", label="", icon="🗑️")

# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_garbage")

# --- COSTANTS ---


# --- FUNCTIONS ---
def load_dataset():
  return db.fetch().items

# --- DATASET ---
db_content = load_dataset()
df = pd.DataFrame(db_content)

df_concat = pd.DataFrame()

for i in range(len(df)):
    df_temp = pd.DataFrame.from_dict(df.dict_values[i], orient='index')\
    .stack().to_frame().rename(columns={0:i})
    
    df_concat= pd.concat([df_concat,df_temp],axis=1)

a = df_concat.stack().to_frame().reset_index()\
.rename(columns={0:"value","level_2":"row"})

a["datum"] = a["row"].apply(lambda x: df.loc[x,"datum"])
a["location"] = a["row"].apply(lambda x: df.loc[x,"location"])
a["day_storm"] = a["row"].apply(lambda x: df.loc[x,"day_storm"])

df_2 = df[["datum","location","day_storm","operator","total","comment"]]

# --- APP ---
if choose == "Observations":
    col_1,col_2 = st.columns([4,3])
    
    if len(df)==0:
        st.warning("No data yet")
        st.stop()
        
    option = col_1.dataframe(data=df_2, use_container_width=True,hide_index=True, on_select="rerun", selection_mode="single-row")
    # st.download_button(label="Download data as CSV",data=a,file_name="df.csv",mime="text/csv")
    
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



elif choose == "Sunburst chart":
    a_sunplot = a.groupby(['location',"level_0","level_1"],as_index=False)["value"].sum()
    a_sunplot_2 = a.groupby(["level_0","level_1"],as_index=False)["value"].sum()
    
    fig = px.sunburst(a_sunplot, path=['location',"level_0","level_1"], values='value')
    fig_2 = px.sunburst(a_sunplot_2, path=["level_0","level_1"], values='value')

    
    st.plotly_chart(fig, use_container_width=True)
    "---"
    st.plotly_chart(fig_2, use_container_width=True)
    "---
    df_bar_chart = df_2.groupby('location')['total'].sum().sort_values(by='total',ascending=False)
    st.bar_chart(df_bar_chart,horizontal=True)
    # st.dataframe(data=df_2.groupby('location',as_index=False)['total'].sum(), use_container_width=True,hide_index=True)
    

    
   
