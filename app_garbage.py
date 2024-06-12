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

def insert_input(datum,moment,t_1,t_2,locatie,kant,temp,wind,weersomstandigheden,rapport):

  return db.put({"Datum":str(datum),"Moment":moment,"Starttijd":str(t_1),"Eindtijd":str(t_2),"Locatie":locatie,"kant":kant,"Laagste temperatuur":temp,"Windsnelheid":wind,"Weersomstandigheden":weersomstandigheden,"rapport":rapport})

        
# --- APP ---
datum = st.date_input("Datum", datetime.datetime.today())
operator = st.selectbox('Operator',OPERATOR,key='OPERATOR',placeholder="chose an operator...",index=None)
location = st.selectbox('Location',LOCATION,key='LOCATION',placeholder="chose an location...",index=None)

for type in TYPE:
  with st.expander(type):
    for class in dict_classes[type]:
      
      option = st.selectbox('Class',dict_classes[type],key=type,placeholder="chose an type...",index=None)


# submitted = st.button("Gegevens invoegen")

# if submitted:

#     if locatie==None or moment==None or t_1==None or t_2==None or temp==None or kant==None:
#         st.warning("Vul het formulier in, alstublieft")
#         st.stop()

#     insert_input(datum,moment,t_1,t_2,locatie,kant,temp,wind,weersomstandigheden,rapport)
#     st.write(f"Done!")
