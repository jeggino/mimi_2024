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

# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_garbage")

# --- COSTANTS ---

OPERATOR = ["Michael","Noah", "Other"]
LOCATION = ["Small beach","Platform","Floor of the small bay","Floor of the big bay","Big beach","Sea surface"]
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

def insert_input(dict_values):

  return db.put({"observation":dict_values})

        
# --- APP ---
datum = st.date_input("Date", datetime.datetime.today())
operator = st.selectbox('Operator',OPERATOR,key='OPERATOR',placeholder="chose an operator...",index=None)
location = st.selectbox('Location',LOCATION,key='LOCATION',placeholder="chose an location...",index=None)


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

dict_values["Total"] = total
dict_values["comment"] = comment
dict_values["datum"] = str(datum)
dict_values["operator"] = operator
dict_values["location"] = location

dict_values

submitted = st.button("Insert data")

if submitted:
    
    insert_input(dict_values)
    st.write(f"Done!")

db_content = load_dataset()
df = pd.DataFrame(db_content).stack().to_frame().reset_index()
df
