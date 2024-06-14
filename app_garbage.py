import streamlit as st

import pandas as pd
import datetime

from deta import Deta

# --- CONFIGURATION ---
st.set_page_config(
    page_title="garbage",
    page_icon="🗑️",
    layout="wide",
    
)

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

OPERATOR = ["Michael","Noah", "Other"]
LOCATION = ["Small beach","Platform","Floor of the small bay","Floor of the big bay","Big beach","Sea surface"]
DAY_STORM = ["1-2","3-4","5+"]
TYPE = ["Wood", "Paper", "Plastic", "Metal", "Glass", "Other"]
PLASTIC = ["bottle", "cup", "piece S", "piece M", "piece L", "bottle S", "bottle M", "bottle L", "bag S", "bag M", "bag L", "pen cup"]
OTHER = ["cigarette butt" ,"styrofoam S", "styrofoam M", "styrofoam L", "Clothe", "clothe tag", "tissue", "boat fragment S", "boat fragment M",
         "boat fragment L", "rope string"]
WOOD = ["piece S", "piece M", "piece L"]
METAL = ["piece S", "piece M", "piece L"]
PAPER = ["piece S", "piece M", "piece L"]
GLASS = ["piece S", "piece M", "piece L"]

dict_classes = {"Wood":WOOD, "Paper":PAPER, "Plastic":PLASTIC, "Metal":METAL, "Glass":GLASS, "Other":OTHER}

# --- FUNCTIONS ---
def load_dataset():
  return db.fetch().items

def insert_input(dict_values,total,comment,datum,operator,location,day_storm):

  return db.put({"dict_values":dict_values,"total":total,"comment":comment,"datum":str(datum),
                "operator":operator,"location":location,"day_storm":day_storm})


# --- APP ---
datum = st.date_input("Date", datetime.datetime.today())
operator = st.selectbox('Operator',OPERATOR,key='OPERATOR',placeholder="chose an operator...",index=None)
location = st.selectbox('Location',LOCATION,key='LOCATION',placeholder="chose a location...",index=None)
day_storm = st.selectbox('Number of days since the last storm',DAY_STORM,key='DAY_STORM',placeholder="make a choice...",index=None)

.Number of days from  last storm:


dict_values = {}
for type_1 in TYPE:
    with st.expander(type_1):
        idict = {}
        for type_2 in dict_classes[type_1]: 
            input = st.number_input(type_2,  step=1,  key=type_1 + type_2, label_visibility="visible")
            idict[type_2] = input
        dict_values[type_1] = idict


total = st.number_input("Total weight",  step=1,  key="TOTAL WEIGHT", help=None, on_change=None, placeholder=None, disabled=False, label_visibility="visible")
comment = st.text_input("Comment",)
submitted = st.button("Insert data")

if submitted:

    if operator==None or location==None or total==0 or comment==None:
        st.warning("Please complete all fields")
        st.stop()
    
    insert_input(dict_values,total,comment,datum,operator,location,day_storm)
    st.write(f"Done!")
