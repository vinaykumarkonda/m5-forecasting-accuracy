import streamlit as st
from support.helper import SupportMethods
from multiapp import MultiApp
# import your app modules here
from apps import sales_forecast
from PIL import Image

sm = SupportMethods()

favicon = Image.open('favicon.jpg')
st.set_page_config(
    page_title="WallmartSF",
    page_icon=favicon,
    layout="wide",
)

app = MultiApp()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

sm.set_page_title("WallmartSF")
st.sidebar.title("WallmartSF")
st.sidebar.markdown("*Version 1.1*")

# Add all your application here
app.add_app("Wallmart's Sales Forecast", sales_forecast.app)


# The main app
app.run()
