import streamlit as st
import requests
import math
from typing import List, Tuple
import pandas as pd

import sys
sys.path.append("./venv/lib/python3.11/site-packages/bs4")

# def page_reservation(hotel_id: int):
#     """ 予約ボタンなどの表示 """
#     st.markdown(str(hotel_id) + 'Reserve This Hotel?')
#     if st.button(str(hotel_id) + ". Yes"):
#         st.session_state.user.reserve(hotel_id)
#         st.write(st.session_state.user.stay_history)
#     elif st.button(str(hotel_id) + ". No"):
#         pass
        
# def get_ido_keido_from_spot(spot: str) -> tuple[float, float]:
#     """ 場所情報から緯度経度を獲得する """
#     url = 'https://www.geocoding.jp/api/'
#     payload = {"v": 1.1, "q": spot}
#     r = requests.get(url, params=payload)
#     ret = BeautifulSoup(r.content, "lxml")
#     if ret.find("error"):
#         return -1, -1
#     else:
#         ido = float(ret.find("lat").string)
#         keido = float(ret.find("lng").string)
#         return ido, keido

def get_ido_keido_from_spot(place: str):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place,
        "format": "json"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if not data:
        return 1, 1

    lat = data[0]["lat"]
    lon = data[0]["lon"]
    return float(lat), float(lon)


def simple_distance(lat1, lon1, lat2, lon2):
    """ 検索クエリからのホテルの距離を測るのに使用 """
    # 緯度1度あたりの距離 (約111km)
    km_per_latitude = 111.0
    # 経度1度あたりの距離。緯度に依存するため、平均的な緯度を使用する。
    km_per_longitude = 111.0 * abs(math.cos(math.radians((lat1 + lat2) / 2)))
    
    # 緯度と経度の差に応じた距離を計算
    x = (lat2 - lat1) * km_per_latitude
    y = (lon2 - lon1) * km_per_longitude
    
    # ピタゴラスの定理で直線距離を計算
    distance = math.sqrt(x**2 + y**2)
    
    return distance


def show_recommend_hotel(related_hotels_and_sim: List[Tuple[float, str]]) -> None:
    if not related_hotels_and_sim:
        return 
    for sim, hotel_id in related_hotels_and_sim:
        name, url, title = (st.session_state.vector_database[hotel_id][key] for key in ["name", "url", "title"])
        col1, col2 = st.columns([2, 8])

        with col1:
            if col1.button("Reserve", key=hotel_id):
                st.session_state.user.reserve(hotel_id)
        with col2:
            col2.markdown(f'**[{name}]({url})**  <br>.. <sub>{title}</sub>', unsafe_allow_html=True)
        st.markdown("---")
    
    df = pd.DataFrame(
        [[st.session_state.vector_database[hotel_id][key] for key in ["ido", "keido"]] for sim, hotel_id in related_hotels_and_sim],
        columns = ["lat", "lon"]
        )
    st.map(df)
        
    return


# if __name__ == "__main__":
#     print(get_ido_keido_from_spot("北海道"))