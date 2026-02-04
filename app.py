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
    "version": "v9.1 Pro",
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

# --- WEBSITE CONFIG & CSS STYLING ---
st.set_page_config(page_title="LISA v9.1 - AI Visual Architect", page_icon="lz", layout="wide")

# This is the "CSS Injection" to force the Facebook/Professional look
st.markdown("""
<style>
    /* GLOBAL BACKGROUND */
    .stApp {
        background-color: #f0f2f5;
    }
    
    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #ddd;
    }

    /* HEADERS */
    h1 {
        color: #1877F2;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        padding-bottom: 10px;
        border-bottom: 2px solid #e1e3e8;
    }
    h3 {
        color: #4b4f56;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* CARD STYLE FOR INPUTS */
    .stTextArea, .stTextInput {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* THE 'FACEBOOK BLUE' BUTTON */
    .stButton>button {
        background-color: #1877F2;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        width: 100%;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #166fe5;
        box-shadow: 0 4px 8px rgba(24, 119, 242, 0.3);
    }
    
    /* ALERT BOXES */
    .stAlert {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- THE GEMMA ENGINE ---
def generate_content_raw(api_key, model_name, script):
    clean_key = api_key.strip()
    url = f"[https://generativelanguage.googleapis.com/v1beta/models/](https://generativelanguage.googleapis.com/v1beta/models/){model_name}:generateContent?key={clean_key}"
    
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

# --- MAIN APP LAYOUT ---

# Header Section
st.title("LISA v9.1")
st.markdown("### AI Visual Architect | Professional Edition")
st.markdown("---")

# Login Check
password_input = st.sidebar.text_input("🔒 Access Portal", type="password", placeholder="Enter Password...")

if password_input == ACCESS_PASSWORD:
    st.sidebar.success("✅ SYSTEM ONLINE")
    
    # --- PRO SIDEBAR ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔑 API Configuration")
    st.sidebar.info("Enter your Google API Key below to power the engine.")
    user_api_key = st.sidebar.text_input("API Key", type="password", placeholder="Paste AIzaSy... here")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Engine Status:** Ready")
    st.sidebar.markdown("**Protocol:** Rafael Standard")
    
    # --- MAIN WORKSPACE ---
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### 🎬 Script Ingestion")
        user_script = st.text_area("Paste the script for analysis:", height=300, placeholder="Paste true crime script here...")

    with col2:
        st.markdown("#### 🚀 Controls")
        st.write("") # Spacer
        st.write("") # Spacer
        if st.button("Initialize Lisa"):
            if not user_api_key:
                st.error("⚠️ API Key Required in Sidebar")
                st.stop()
                
            if user_script:
                models = ["gemma-3-27b-it", "gemma-3-12b-it"]
                success = False
                
                status_container = st.empty()
                progress_bar = st.progress(0)
                
                for i, model in enumerate(models):
                    status_container.info(f"⚡ Connecting to Neural Engine: {model}...")
                    progress_bar.progress((i + 1) * 50)
                    
                    result = generate_content_raw(user_api_key, model, user_script)
                    
                    if "ERROR" not in result:
                        st.markdown("---")
                        st.success(f"✅ Generation Complete via {model}")
                        st.markdown("### 📸 Output Manifest:")
                        st.markdown(result)
                        success = True
                        status_container.empty()
                        progress_bar.empty()
                        break
                    else:
                        st.warning(f"⚠️ {model} unresponsive. Rerouting...")
                
                if not success:
                    st.error("❌ System Failure: All engines unresponsive.")
                    st.code(result)
            else:
                st.warning("⚠️ Input Buffer Empty")

elif password_input:
    st.sidebar.error("❌ Access Denied")
