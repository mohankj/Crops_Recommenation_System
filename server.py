import streamlit as st
import numpy as np
import pandas as pd
import pickle
import time
import base64

# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()


# def set_background(png_file):
#     bin_str = get_base64(png_file)
#     page_bg_img = '''
#     <style>
#     .stApp {
#     background-image: url("data:image/png;base64,%s");
#     background-size: 2000px 900px;
#     }
#     </style>
#     ''' % bin_str
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# set_background('img\crp.gif')


st.set_page_config(layout="wide")

video_html = """
		<style>

		#myVideo {
		  position: fixed;
		  right: 0;
		  bottom: 0;
		  min-width: 100%;
		  min-height: 100%;
		}

		.content {
		  position: fixed;
		  bottom: 0;
		  background: rgba(0, 0, 0, 0.5);
		  color: #f1f1f1;
		  width: 100%;
		  padding: 20px;
		}

		</style>
		<video autoplay muted loop id="myVideo">
		#   <source src="https://v1.pinimg.com/videos/mc/720p/ad/f5/0c/adf50c302e314fcab737ed8dc813e246.mp4")>
		  Your browser does not support HTML5 video.
		</video>
        """

st.markdown(video_html, unsafe_allow_html=True)
st.title('Crops Production')

# https://v1.pinimg.com/videos/mc/720p/8b/0d/ef/8b0def62d7fa9da5f1734c1e4e23294e.mp4
st.subheader('Predict the Production of Crops at any Particular Season')

with open('Crops_Model/mapping_dict.pkl', 'rb') as f:
    mapping_dict = pickle.load(f)

with open('Crops_Model/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('Crops_Model/original_data.pkl', 'rb') as f:
   # data = pickle.load(f)
    data = pd.read_pickle(f)


def predict(State, District, Season, Area):
    # Predicting the Production Of Crops.
    state = mapping_dict['State'][State]
    district = mapping_dict['District'][District]
    season = mapping_dict['Season'][Season]

    prediction = model.predict(pd.DataFrame(np.array([state, district, season, Area]).reshape(
        1, 4), columns=['State', 'District', 'Season', 'Area']))
    crop = list(filter(
        lambda x: mapping_dict['Crop'][x] == prediction, mapping_dict['Crop']))[0]
    return crop


# Input
state_list = data['State'].unique()
selected_state = st.selectbox(
    "Type or select a State from the dropdown",
    options=state_list
)

district_list = data['District'].unique()
selected_district = st.selectbox(
    "Type or select a District from the dropdown",
    district_list
)

season_list = data['Season'].unique()
selected_season = st.selectbox(
    "Type or select a Season from the dropdown",
    season_list
)

area = st.number_input('Areas of Plot in (Hectares):',
                       min_value=0.00001, max_value=100000000.0, value=1.0)


if st.button('Predict Production'):
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
        if percent_complete == 98:
            my_bar.progress(percent_complete+1, text="Sucessfully Completed")


st.subheader('We will Recommend you to Cultivate')
st.subheader( predict(selected_state, selected_district, selected_season, area))