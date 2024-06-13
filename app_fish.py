import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import datetime

from deta import Deta

# --- CONFIGURATION ---
st.set_page_config(
    page_title="fish",
    page_icon="🐟",
    layout="wide",
    
)

# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_fish")

# --- COSTANTS ---

OPERATOR = ["Michael","Noah", "Other"]
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

def insert_input(dict_values,datum,operator,location,transect,repetition,comment):

  return db.put({"dict_values":dict_values,"transect":transect,"comment":comment,"datum":str(datum),
                "operator":operator,"location":location,"repetition":repetition})

selected = option_menu(None, ['✍️','📊'], 
                       icons=None,
                       default_index=0,
                       orientation="horizontal",
                       )
# --- APP ---
if selected == '✍️':
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
    repetition = st.selectbox('Repetition',REPETITION,key='REPETITION',placeholder="chose a repetition...",index=None)
  
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
        
        insert_input(dict_values,datum,operator,location,transect,repetition,comment)
        st.write(f"Done!")

    
if selected == '📊':

    col_1,col_2 = st.columns([4,3])
    db_content = load_dataset()
    df = pd.DataFrame(db_content)
    if len(df)==0:
        st.warning("No data yet")
        st.stop()
        
    df_2 = df[["datum","location","operator","transect","repetition","comment"]]
    option = col_1.dataframe(data=df_2, width=None, height=None, use_container_width=True,
                 hide_index=True, column_order=None, column_config=None, key=None, on_select="rerun", selection_mode="single-row")

    try:
        a = df.loc[option["selection"]["rows"][0]]["dict_values"]
        id = df.loc[option["selection"]["rows"][0]]["key"]
        df_3 = pd.DataFrame.from_dict(a, orient='index').stack().to_frame().rename(columns={0:"Ammount"})
        col_2.dataframe(df_3,use_container_width=True)
    except:
        col_2.warning("Select a row")
        st.stop()
        
    # placeholder = col_2.empty()
    submitted = col_1.button("Delete observation",key="submitted_1")
    if submitted:
        # placeholder.empty()
        st.write(id)
        db.delete(id)
        col_1.warning("Are you sure you want to delete this observation?!")
        submitted_2 = col_1.button("Yes I am sure!",key="submitted_2")
        if submitted_2:
            db.delete(id)
            # st.rerun()
