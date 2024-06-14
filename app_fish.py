import streamlit as st

import pandas as pd
import datetime

from deta import Deta

# --- CONFIGURATION ---
st.set_page_config(
    page_title="fish",
    page_icon="🐟",
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
db = deta.Base("df_fish")

# --- COSTANTS ---

OPERATOR = ["Maddie","Brooke", "Ashlyn","Alexis","Other"]
LOCATION = ["Small bay","Big bay"]
TRANSECT_SB = ["SB1","SB2","SB3","SB4",'SB5','SB6','SB7','SB8']
TRANSECT_BB = ['BB1','BB2','BB3']
REPETITION = ['1','2','3','4','5','6','7','8','9','10']
GENUS = ["Lipophrys","Microlipophrys","Aidablennius","Parablennius","Tripterygium"]
SPECIES =  ['Lipophrys trigloides','Microlipophrys canevae','Microlipophrys nigriceps','Aidablennius sphynx',
                    'Parablennius gattorugine','Parablennius incognitus','Parablennius pilicornis','Parablennius rouxi',
                    'Parablennius sanguinolentus','Parablennius zvonimiri','Tripterygium delaisi','Tripterygion melanurum','Tripterygion tripteronotum']

SPECES_dict ={"Lipophrys":['Lipophrys trigloides'],
              "Microlipophrys":['Microlipophrys canevae','Microlipophrys nigriceps'],
              "Aidablennius":['Aidablennius sphynx'],
              "Parablennius":['Parablennius gattorugine','Parablennius incognitus','Parablennius pilicornis','Parablennius rouxi','Parablennius sanguinolentus','Parablennius zvonimiri'],
              "Tripterygium":['Tripterygium delaisi','Tripterygion melanurum','Tripterygion tripteronotum']}


# --- FUNCTIONS ---
def load_dataset():
  return db.fetch().items

def insert_input(dict_values,datum,operator,location,trial,repetition,comment):

  return db.put({"dict_values":dict_values,"transect":transect,"comment":comment,"datum":str(datum),
                "operator":operator,"location":location,"trial":trial})


# --- APP ---
datum = st.date_input("Date", datetime.datetime.today())
operator = st.selectbox('Operator',OPERATOR,key='OPERATOR',placeholder="chose an operator...",index=None)
location = st.selectbox('Location',LOCATION,key='LOCATION',placeholder="chose a location...",index=None)

try:
    if location=="Small bay":
      transect_2 = TRANSECT_SB
    elif location=="Big bay":
      transect_2 = TRANSECT_BB
    transect = st.selectbox('Transect',transect_2,key='TRANSECT',placeholder="chose a transect...",index=None)
except:
    st.warning("Please chose a location!!")
    st.stop()
repetition = st.selectbox('Repetition',REPETITION,key='REPETITION',placeholder="chose a trial...",index=None)

dict_values = {}
for genus in GENUS:
    with st.expander(f"{genus}"):
        idict = {}
        for species in SPECES_dict[genus]: 
            input = st.number_input(species,  step=1,  key=species, label_visibility="visible")
            idict[species] = input
        dict_values[genus] = idict

comment = st.text_input("Comment")

submitted = st.button("Insert data")

if submitted:

    if operator==None or location==None:
        st.warning("Please complete all fields")
        st.stop()
    
    insert_input(dict_values,datum,operator,location,transect,trial,comment)
    st.write(f"Done!")

    
