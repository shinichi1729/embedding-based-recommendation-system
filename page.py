import streamlit as st
import numpy as np

from common import simple_distance, get_ido_keido_from_spot, show_recommend_hotel

def page_all_hotel_info():
    st.header("Hotel Database")

    for key, values in st.session_state.vector_database.items():
        # 行をボタンとして表示し、クリックされたらセッションステートにインデックス番号を保存
        col1, col2 = st.columns([2, 8])
        with col1:
            if col1.button("Reserve", key=key):
                st.session_state.user.reserve(key)
                
        with col2:
            col2.markdown(f'**[{values["name"]}](https://travel.yahoo.co.jp/{key}/)**  <br>.. <sub>{values["title"]}</sub>', unsafe_allow_html=True)
        st.markdown("---")    
    
    return


def page_accommodation_history():
    st.header("Your Accommodation History")
    # TODO 
    col1, col2 = st.columns([2, 8])
    
    with col1:
        col1.markdown("**Hotel ID**")
    with col2:
        col2.markdown("**Hotel Information**")
    st.markdown("---")
    for hotel_id in st.session_state["user"].stay_history:
        name, url, title = (st.session_state.vector_database[hotel_id][key] for key in ["name", "url", "title"])
        col1, col2 = st.columns([2, 8])
        with col1:
            col1.markdown(f"{hotel_id} <br><br>", unsafe_allow_html=True)
        with col2:
            col2.markdown(f'**[{name}]({url})**  <br>.. <sub>{title}</sub>', unsafe_allow_html=True)
        st.markdown("---")
    return


def page_recommend_hotel():
    """ ホテル検索のメインページ """
    st.header("User-Centric Hotel Recommendation System")
    
    query_input = st.text_input("**Where would you like to stay? Enter a spot**👇", placeholder="例：新宿駅、東京タワー周辺")
    
    init_search_radius = st.session_state.search_radius if "search_radius" in st.session_state else 1.5
    search_radius = st.slider('**Allowed distance** (km)',  0.3, 5.0, step=0.1, value=init_search_radius)
    st.session_state.search_radius = search_radius
    
    topk = st.select_slider("**Number of recommendations**", options=[1, 3, 5, 10], value=5)
    pressed = st.button("Search Hotels")
    
    if pressed:
        st.session_state.recommend_hotels = []
        
    if "recommend_hotels" in st.session_state:
        show_recommend_hotel(st.session_state.recommend_hotels)
    
    if pressed:
        st.session_state.recommend_hotels = []
        user_embedding = st.session_state.user.embedding
        
        with st.spinner("Processing..."):
            target_ido, target_keido = get_ido_keido_from_spot(query_input)
            related_hotels_and_sim = []
            for key, values in st.session_state.vector_database.items():
                ido, keido, hotel_embedding = values["ido"], values["keido"], values["embedding"]
                distance = simple_distance(target_ido, target_keido, ido, keido)
                if distance > search_radius:
                    # 探索空間より遠いので無視 
                    continue
                embedding_dot_product = np.dot(user_embedding, hotel_embedding)
                related_hotels_and_sim.append((embedding_dot_product, key))
        related_hotels_and_sim.sort(reverse=True)
        related_hotels_and_sim = related_hotels_and_sim[:topk]
        st.session_state.recommend_hotels = related_hotels_and_sim
        show_recommend_hotel(st.session_state.recommend_hotels)