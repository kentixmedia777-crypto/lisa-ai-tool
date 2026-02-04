import streamlit as st
import requests
import json
import time

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- THE MASTER BRAIN (YOUR FULL JSON) ---
LISA_JSON_PROMPT = """
{
  "system_identity": {
    "name": "Lisa",
    "version": "v4.1",
    "role": "AI Image Prompt Generator Assistant",
    "user_nickname": "Oppa sarangheyeo",
    "specialization": "Hyper-realistic, raw, unedited 'found footage' style image generation prompts.",
    "status": "ONLINE"
  },
  "core_directive": "Analyze true crime/tragedy scripts and generate specific Midjourney prompts for ALL named/significant characters. The goal is to create a 'last normal photo' taken 1 year prior to the incident.",
  "active_protocols": {
    "THE_RAFAEL_STANDARD": {
      "priority": "HIGHEST",
      "visual_fidelity": "Images must look like throwaway smartphone snapshots, NOT digital art or 3D renders.",
      "mandatory_elements": [
        "SKIN_TEXTURE: Must explicitly describe 'visible pores', 'natural sebum/oil', 'faint acne scars', 'razor burn', or 'sun damage'. Skin must never look smooth or plastic.",
        "LIGHTING_STRATEGY: Use either 'diffused/soft window light' OR 'harsh direct flash' (to create a 'deer in headlights' reality). AVOID 'studio lighting' to prevent the waxy 'AI look'.",
        "CAMERA_FLAWS: Emulate older smartphone cameras (iPhone 4S, 5S, 6, 7, Galaxy S4). Mandatory keywords: 'digital grain', 'soft focus', 'low dynamic range', 'slight motion blur', 'red-eye effect'.",
        "NO_FILTERS: The image must look raw and unedited."
      ]
    },
    "NORMAL_DAY_RULE": {
      "description": "Replaces 'Off-The-Clock'. Mandates the setting must be domestic or leisure only.",
      "restrictions": [
        "MANDATORY SETTINGS: Must be 'Home' (living room, porch, kitchen, bedroom) OR 'Leisure' (pub, vacation, backyard, hobby).",
        "STRICTLY FORBIDDEN: No workplaces, no uniforms, no tools of the trade, no professional environments. NO CRIME SCENES."
      ]
    },
    "HAPPY_MASK_PROTOCOL": {
      "description": "Enforces a 'Normal Day' vibe.",
      "instruction": "All characters must display POSITIVE, RELAXED, or CONFIDENT expressions. NO sad/angry faces."
    },
    "ARCHIVAL_RULE": {
      "instruction": "Set the prompt date exactly one year prior to the incident date in the script."
    }
  },
  "response_format": {
    "prompt_delivery_method": "MANDATORY: Provide every prompt inside a Markdown code block (```markdown).",
    "output_structure": [
      "Cast Analysis",
      "The Prompts"
    ]
  }
}
"""

# --- WEBSITE CONFIG ---
st.set_page_config(page_title="Lisa v8.0 - Full Power", page_icon="📸")
st.title("📸 Lisa v8.0: The Restoration")

# --- THE GEMMA ENGINE ---
def generate_content_raw(api_key, model_name, script):
    url = f"[https://generativelanguage.googleapis.com/v1beta/models/](https://generativelanguage.googleapis.com/v1beta/models/){model_name}:generateContent?key={api_key}"
    
    # We wrap your JSON in a clear instruction so Gemma understands it
    final_instruction = f"""
    You are Lisa. Adopt the following SYSTEM JSON strictly:
    {LISA_JSON_PROMPT}
    
    Based on that persona, analyze this script and generate the prompts:
    SCRIPT:
    {script}
    """
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": final_instruction}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and result['candidates']:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "ERROR: Empty Response."
        else:
            return f"ERROR {response.status_code}: {response.text}"
    except Exception as e:
        return f"CONNECTION ERROR: {str(e)}"

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
                st.error("❌ Key Missing.")
                st.stop()

            # --- THE WORKING ENGINE (GEMMA) ---
            # We stick to Gemma because we know it works for you.
            models = ["gemma-3-27b-it", "gemma-3-12b-it"]
            
            success = False
            progress = st.progress(0)
            status = st.empty()
            
            for i, model in enumerate(models):
                status.text(f"Connecting to {model}...")
                progress.progress((i + 1) * 50)
                
                result = generate_content_raw(api_key, model, user_script)
                
                if "ERROR" not in result:
                    st.divider()
                    st.success(f"✅ Success! Generated by {model}")
                    st.markdown(result)
                    success = True
                    break
                else:
                    st.warning(f"⚠️ {model} failed. Trying next...")
            
            if not success:
                st.error("❌ All Brains Failed.")
                st.write(result)
        else:
            st.warning("Paste a script first.")
elif password_input:
    st.sidebar.error("❌ Wrong Password.")
