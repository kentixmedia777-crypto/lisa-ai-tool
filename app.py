import streamlit as st
import requests
import json
import time

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- SYSTEM PROMPT ---
# Gemma is a bit more literal, so we simplify the instructions slightly.
LISA_SYSTEM_PROMPT = """
You are Lisa, an AI Assistant.
ROLE: Generate "found footage" style image prompts based on the user's script.
STYLE: Realistic, 2015 Smartphone Quality, Flash Photography.
OUTPUT FORMAT: Provide the prompt inside a Markdown code block.
"""

# --- WEBSITE CONFIG ---
st.set_page_config(page_title="Lisa v7.0 - Gemma Edition", page_icon="💎")
st.title("💎 Lisa v7.0: Gemma Edition")

# --- THE ENGINE ---
def generate_content_raw(api_key, model_name, script):
    # This URL targets the Gemma models
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": f"{LISA_SYSTEM_PROMPT}\n\nSCRIPT:\n{script}"}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            # Gemma's response structure is standard
            if 'candidates' in result and result['candidates']:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"ERROR: Empty Response. {result}"
        else:
            return f"ERROR {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"CRITICAL CONNECTION ERROR: {str(e)}"

# --- MAIN APP ---
password_input = st.sidebar.text_input("Enter Access Password", type="password")

if password_input == ACCESS_PASSWORD:
    st.sidebar.success("✅ Access Granted")
    
    st.write("### Paste the Script Below:")
    user_script = st.text_area("Script Input", height=300)
    
    if st.button("Activate Lisa (Gemma)"):
        if user_script:
            
            if "GOOGLE_API_KEY" in st.secrets:
                api_key = st.secrets["GOOGLE_API_KEY"]
            else:
                st.error("❌ API Key Missing in Secrets")
                st.stop()

            # --- THE GEMMA LIST ---
            # We use the models found in your scan (Items 13, 12, 11)
            models = [
                "gemma-3-27b-it",  # The Big Brain
                "gemma-3-12b-it",  # The Medium Brain
                "gemma-3-4b-it"    # The Fast Brain
            ]
            
            success = False
            progress = st.progress(0)
            status = st.empty()
            
            for i, model in enumerate(models):
                status.text(f"Connecting to Backup Brain: {model}...")
                progress.progress((i + 1) * 30)
                
                result = generate_content_raw(api_key, model, user_script)
                
                if "ERROR" not in result:
                    st.divider()
                    st.success(f"✅ Success! Connected to {model}")
                    st.markdown(result)
                    success = True
                    break
                else:
                    st.warning(f"⚠️ {model} is locked. Trying smaller brain...")
                    time.sleep(1)
            
            if not success:
                st.error("❌ All Brains (Gemini AND Gemma) are exhausted.")
                st.info("💡 You have hit the 'Global Limit' for this free Google account.")
                st.write("Solution: You must wait 1-2 hours for the quota to reset, or use a different Google Account's API Key.")
                st.code(result)
                
        else:
            st.warning("Paste a script first.")

elif password_input:
    st.sidebar.error("❌ Wrong Password.")
