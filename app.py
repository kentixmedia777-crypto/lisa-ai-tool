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
    "version": "v5.1 (Stable Edition)",
    "status": "ONLINE"
  },
  "core_directive": "Analyze true crime/tragedy scripts and generate specific Midjourney prompts.",
  "active_protocols": {
    "THE_RAFAEL_STANDARD": {
      "mandatory_elements": ["visible pores", "natural sebum/oil", "faint acne scars", "razor burn", "harsh direct flash", "red-eye effect", "digital grain"]
    },
    "NORMAL_DAY_RULE": {
      "restrictions": ["MANDATORY: Home or Leisure settings.", "FORBIDDEN: Workplaces, uniforms, crime scenes."]
    }
  },
  "response_format": {
    "prompt_delivery_method": "Provide every prompt inside a Markdown code block."
  }
}
"""

# --- WEBSITE CONFIG ---
st.set_page_config(page_title="Lisa v5.1 - Stable", page_icon="📸")
st.title("📸 Lisa v5.1: Stable Edition")

# --- THE ENGINE ---
def generate_content_raw(api_key, model_name, script):
    # We use the "Stable Aliases" found in your list (Item #16 and #18)
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
            return result['candidates'][0]['content']['parts'][0]['text']
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

            # --- THE STABLE LIST ---
            # These are aliases that point to the working versions
            models = [
                "gemini-flash-latest",    # Priority 1: High Speed, High Quota
                "gemini-pro-latest",      # Priority 2: High Intelligence
                "gemini-1.5-flash"        # Priority 3: Old Reliable
            ]
            
            success = False
            progress = st.progress(0)
            status = st.empty()
            
            for i, model in enumerate(models):
                status.text(f"Lisa is connecting to {model}...")
                progress.progress((i + 1) * 30)
                
                result = generate_content_raw(api_key, model, user_script)
                
                if "ERROR" not in result:
                    st.divider()
                    st.success(f"✅ Success! Connected to Brain: {model}")
                    st.markdown(result)
                    success = True
                    break
                else:
                    # If it fails, we wait 2 seconds before trying the next one
                    # to avoid hitting the speed limit again.
                    st.warning(f"⚠️ {model} failed or is busy. Switching...")
                    time.sleep(2)
            
            if not success:
                st.error("❌ All Brains Failed.")
                st.write(result) 
                
        else:
            st.warning("Paste a script first.")

elif password_input:
    st.sidebar.error("❌ Wrong Password.")
