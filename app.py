import streamlit as st
import requests
import json
import base64

# --- DARK MODE CONFIG ---
st.set_page_config(page_title="LISA - Neural Scanner", page_icon="lz", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #18191a; }
    h1, h2, h3 { color: #2D88FF !important; font-family: sans-serif; }
    .stMarkdown, p, label { color: #e4e6eb !important; }
    .stTextInput input { background-color: #3a3b3c; color: white; border: 1px solid #3e4042; }
    .stButton>button { background-color: #2D88FF; color: white; border: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("LISA: Neural Network Scanner")
st.markdown("### 🔍 Diagnostic Mode")
st.info("Paste your NEW API Key below to identify the fastest available model.")

# --- INPUT NEW KEY ---
new_api_key = st.text_input("New API Key", type="password")

if st.button("Start Scan"):
    if not new_api_key:
        st.error("Please enter a key.")
        st.stop()
        
    clean_key = new_api_key.strip()
    
    # SAFE URL BUILDER
    secret_domain = "aHR0cHM6Ly9nZW5lcmF0aXZlbGFuZ3VhZ2UuZ29vZ2xlYXBpcy5jb20="
    base_url = base64.b64decode(secret_domain).decode('utf-8')
    url = f"{base_url}/v1beta/models?key={clean_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "error" in data:
            st.error(f"❌ API Error: {data['error']['message']}")
        else:
            st.success("✅ Access Granted. Available Brains:")
            
            # Filter and display only generating models
            found_models = []
            for m in data.get('models', []):
                if "generateContent" in m['supportedGenerationMethods']:
                    name = m['name'].replace("models/", "")
                    found_models.append(name)
            
            # Display results nicely
            st.write("---")
            for model in found_models:
                # Highlight the best ones
                if "flash" in model:
                    st.markdown(f"**🚀 {model} (FAST - RECOMMENDED)**")
                else:
                    st.code(model)
                    
            st.write("---")
            st.markdown("### 📋 Instructions for Solomon:")
            st.write("Copy the name of the **🚀 FAST** model above and send it to me.")
            
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
