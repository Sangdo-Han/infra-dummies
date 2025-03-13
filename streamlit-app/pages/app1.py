import os

import dotenv
import requests
import streamlit as st

dotenv.load_dotenv("./app1.env")

TARGET_API_SERVER = os.getenv("TARGET_API_SERVER")
APP_NAME = "APP -> " + TARGET_API_SERVER

if st.button("interact"):
    try:
        response = requests.get(f"{TARGET_API_SERVER}/interact")
        if 200 == response.status_code:
            data = response.json()
            st.success(data.get("message", "No message received"))
        else:
            st.error("Failed to get response")
    except Exception as e:
        st.error(f"Error: {e}")

