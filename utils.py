def nb_vict_aff(data):
    import pandas as pd
    return pd.date_range(data.name.date(), periods=2).isin(data.index.date)

def markdown(text, center=False, size="30px", color=None, sidebar=False):
    import streamlit as st
    text_to_center = ("<div style='text-align:center';>", "</div>") if center else ("", "")
    if sidebar:
        return st.sidebar.markdown(
            f"{text_to_center[0]}<span style='font-size:{size};color:{color};'>{text}</span>{text_to_center[1]}",
            unsafe_allow_html=True
        )
    else:
        return st.markdown(
            f"{text_to_center[0]}<span style='font-size:{size};color:{color};'>{text}</span>{text_to_center[1]}",
            unsafe_allow_html=True
        )

def geocoding(address):
    import requests
    return requests.get(
            f"https://maps.googleapis.com/maps/api/geocode/json?address={address.strip().replace(' ZAC ', ' ').replace(' ', '%20')}&key=AIzaSyDAcFLAXxWWAO42WtuT1l8Hq5az_nuZAV0"
            ).json()["results"][0]["geometry"]["location"]