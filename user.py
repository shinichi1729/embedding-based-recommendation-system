import numpy as np
import streamlit as st


class User(object):
    def __init__(self, dim=1536):
        self.stay_history = []       # Userの宿泊履歴
        self.dim = dim
        
    def reserve(self, hotel_id: int):
        self.stay_history.append(hotel_id)
    
    @property
    def embedding(self, weight=0.9):
        if not self.stay_history:
            return np.random.randn(self.dim)
        user_embedding = np.zeros(self.dim)
        for i, hotel_id in enumerate(self.stay_history[:20]):
            hotel_embed = st.session_state.vector_database[hotel_id]["embedding"] 
            user_embedding += hotel_embed * (weight ** i)
        return user_embedding