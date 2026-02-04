import streamlit as st
import requests
import json
import time

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- THE WEBSITE SETTINGS ---
st.set_page_config(page_title="Lisa Repair Mode", page_icon="🚑")
st.title("🚑 Lisa Repair Mode")

# --- THE DOCTOR TOOL ---
def ask_google_what_works(api_key):
    # This asks Google: "Hello? Are you there? What brains can I use?"
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return f"Internet Error: {str(e)}"

# --- THE MAIN SCREEN ---
password_input = st.sidebar.text_input("Enter Password", type="password")

if password_input == ACCESS_PASSWORD:
    st.sidebar.success("✅ Password Accepted")
    
    # Check if the Key is hidden in the safe
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.write("🔑 I found your API Key in the safe.")
    else:
        st.error("❌ I cannot find your API Key! Please check Secrets.")
        st.stop()

    st.divider()
    st.write("### 👇 CLICK THIS BUTTON 👇")
    st.write("This will test your API Key to see if it is working.")
    
    if st.button("TEST MY KEY NOW"):
        with st.spinner("Calling Google..."):
            result = ask_google_what_works(api_key)
            st.write("### 📝 Here is what Google said:")
            st.json(result)

elif password_input:
    st.error("Wrong Password")
