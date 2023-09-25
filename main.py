import streamlit as st
import pandas as pd
import numpy as np

import pickle

from page import page_all_hotel_info, page_accommodation_history, page_recommend_hotel
from user import User
            
            
def initialize_page():
    st.set_page_config(
        page_title = "Hotel Recommend Tools",
    )


def main():
    initialize_page()
    
    page_selection = st.sidebar.radio("Go to", ["main", "All Hotels info", "Your Accommodation history"])
    if page_selection == "All Hotels info":
        page_all_hotel_info()
    elif page_selection == "Your Accommodation history":
        page_accommodation_history()
    else:
        page_recommend_hotel()
    
    
if __name__ == "__main__":
    # describe_map(None, None)
    if "user" not in st.session_state:
        print("create user")
        st.session_state["user"] = User()
    if "vector_database" not in st.session_state:
        with open('./data/vector_database.pkl', 'rb') as f:
            st.session_state["vector_database"] = pickle.load(f)
        print("created vector database")
    main()
