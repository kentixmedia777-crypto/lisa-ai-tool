import streamlit as st
import requests
import json
import time

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- SYSTEM PROMPT ---
LISA_SYSTEM_PROMPT = """
You are Lisa, an AI Image Prompt Generator Assistant.
Your User Nickname is "Oppa sarangheyeo".

**STRICT SYSTEM INSTRUCTIONS (JSON FORMAT):**
{
  "system_identity": {
    "name": "Lisa",
    "version": "v6.0 (Survival Mode)",
    "status": "ONLINE"
  },
  "core_directive": "Analyze true crime/tragedy scripts and generate specific Midjourney prompts.",
  "active_protocols": {
    "THE_RAFAEL_STANDARD": {
      "mandatory_elements": ["visible pores", "natural sebum/oil", "faint acne scars", "razor burn", "harsh direct flash", "red-eye effect", "digital grain"]
    }
  },
  "response_format": {
    "prompt_delivery_method": "Provide every prompt inside a Markdown code block."
  }
}
"""

# --- WEBSITE CONFIG ---
st.set_page_config(page_title="Lisa v6.0 - Survival", page_icon="📸")
st.title("📸 Lisa v6.0: Survival Mode")

# --- THE ENGINE ---
def generate_content_raw(api_key, model_name, script):
    # Toggle between v1beta and v1 based on the model to find a working door
    version = "v1beta" 
    
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
            # Handle different response structures for Gemma vs Gemini
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
    
    if st.button("Activate Lisa"):
        if user_script:
            
            if "GOOGLE_API_KEY" in st.secrets:
                api_key = st.secrets["GOOGLE_API_KEY"]
            else:
                st.error("❌ API Key Missing in Secrets")
                st.stop()

            # --- THE SURVIVAL LIST ---
            # 1. gemini-flash-latest: The generic pointer (Might work)
            # 2. gemini-2.0-flash-001: The specific stable version (Might work)
            # 3. gemma-3-27b-it: The Open Model (Backup)
            models = [
                "gemini-flash-latest",
                "gemini-2.0-flash-001",
                "gemma-3-27b-it"
            ]
            
            success = False
            progress = st.progress(0)
            status = st.empty()
            error_log = []
            
            for i, model in enumerate(models):
                status.text(f"Attempting connection to Brain: {model}...")
                progress.progress((i + 1) * 30)
                
                result = generate_content_raw(api_key, model, user_script)
                
                if "ERROR" not in result:
                    st.divider()
                    st.success(f"✅ Success! Connected to Brain: {model}")
                    st.markdown(result)
                    success = True
                    break
                else:
                    # Capture the SPECIFIC error to show you
                    clean_error = result.replace('"', '')[:200] + "..." # Shorten it
                    error_msg = f"⚠️ {model} Failed: {clean_error}"
                    error_log.append(error_msg)
                    st.warning(error_msg)
                    time.sleep(1)
            
            if not success:
                st.error("❌ All Brains Failed.")
                with st.expander("🔍 READ THIS ERROR LOG TO SOLOMON"):
                    for err in error_log:
                        st.write(err)
                
        else:
            st.warning("Paste a script first.")

elif password_input:
    st.sidebar.error("❌ Wrong Password.")
