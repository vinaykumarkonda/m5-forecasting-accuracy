from support.helper import SupportMethods
import streamlit as st
import pandas as pd
from time import gmtime, strftime

sm = SupportMethods()

def app():
    st.title('Forecast Sales')
    st.markdown(unsafe_allow_html=True, body="""<pre>By selecting Store_Id and Item_Id, will forecast the sales.</pre>""")
    sm.sales_forecasting()