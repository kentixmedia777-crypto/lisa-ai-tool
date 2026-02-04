import streamlit as st
import requests
import json
import time

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- THE MASTER BRAIN ---
LISA_JSON_PROMPT = """
{
  "system_identity": {
    "name": "Lisa",
    "version": "v9.2 Enterprise",
    "role": "AI Image Prompt Generator Assistant",
    "user_nickname": "Oppa sarangheyeo",
    "specialization": "Hyper-realistic found footage style image generation.",
    "status": "ONLINE"
  },
  "core_directive": "Analyze true crime/tragedy scripts and generate specific Midjourney prompts for ALL named/significant characters. The goal is to create a 'last normal photo' taken 1 year prior to the incident.",
  "active_protocols": {
    "THE_RAFAEL_STANDARD": {
      "priority": "HIGHEST",
      "visual_fidelity": "Images must look like throwaway smartphone snapshots.",
      "mandatory_elements": ["visible pores", "natural sebum/oil", "faint acne scars", "razor burn", "harsh direct flash", "red-eye effect", "digital grain"]
    },
    "NORMAL_DAY_RULE": {
      "restrictions": ["MANDATORY: Home or Leisure settings.", "FORBIDDEN: Workplaces, uniforms, crime scenes."]
    }
  },
  "response_format": {
    "prompt_delivery_method": "MANDATORY: Provide every prompt inside a Markdown code block (```markdown).",
    "output_structure": ["Cast Analysis", "The Prompts"]
  }
}
"""

# --- PROFESSIONAL STYLING (Facebook/Meta Style) ---
st.set_page_config(page_title="LISA v9.2 - Enterprise", page_icon="lz", layout="wide")
st.markdown("""
<style>
    .stApp {background-color: #f0f2f5;}
    [data-testid="stSidebar"] {background-color: #ffffff; border-right: 1px solid #ddd;}
    h1 {color: #1877F2; font-family: 'Helvetica Neue', sans-serif; font-weight: 800;}
    .stButton>button {background-color: #1877F2; color: white; border-radius: 8px; font-weight: bold; border: none; padding: 12px 24px; width: 100%; text-transform: uppercase; letter-spacing: 1px;}
    .stButton>button:hover {background-color: #166fe5;}
    .stTextArea, .stTextInput {background-color: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

# --- ENGINE ---
def generate_content_raw(api_key, model_name, script):
    clean_key = api_key.strip() # <--- SAFETY CLEANER
    url = f"[https://generativelanguage.googleapis.com/v1beta/models/](https://generativelanguage.googleapis.com/v1beta/models/){model_name}:generateContent?key={clean_key}"
    
    final_instruction = f"You are Lisa. Adopt the following SYSTEM JSON strictly:\n{LISA_JSON_PROMPT}\n\nSCRIPT:\n{script}"
    
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": final_instruction}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result: return result['candidates'][0]['content']['parts'][0]['text']
            return "ERROR: Empty Response."
        return f"ERROR {response.status_code}: {response.text}"
    except Exception as e:
        return f"CONNECTION ERROR: {str(e)}"

# --- MAIN APP ---
st.title("LISA v9.2")
st.markdown("### AI Visual Architect | Enterprise Edition")
st.markdown("---")

password_input = st.sidebar.text_input("🔒 Access Portal", type="password", placeholder="Enter Password...")

if password_input == ACCESS_PASSWORD:
    st.sidebar.success("✅ SYSTEM ONLINE")
    st.sidebar.markdown("---")
    
    # --- INTELLIGENT KEY CHECK ---
    # 1. Check the Safe (Secrets) first
    if "GOOGLE_API_KEY" in st.secrets:
        # If found in secrets, USE IT and HIDE the box
        final_api_key = st.secrets["GOOGLE_API_KEY"]
        st.sidebar.success("✅ License Key Active")
        st.sidebar.info("Authorized for: Lucalles Productions")
    else:
        # 2. Only show this box if Secrets is EMPTY (Fallback)
        st.sidebar.warning("⚠️ No License Found")
        final_api_key = st.sidebar.text_input("Manual Key Entry", type="password")
    
    st.sidebar.markdown("---")
    
    # --- WORKSPACE ---
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("#### 🎬 Script Ingestion")
        user_script = st.text_area("Paste script:", height=300)
    with col2:
        st.markdown("#### 🚀 Controls")
        st.write("")
        st.write("")
        if st.button("Initialize Lisa"):
            if not final_api_key:
                st.error("⚠️ System Halted: Missing API Key")
                st.stop()
                
            if user_script:
                models = ["gemma-3-27b-it", "gemma-3-12b-it"]
                success = False
                status = st.empty()
                progress = st.progress(0)
                
                for i, model in enumerate(models):
                    status.info(f"⚡ Connecting to Neural Engine: {model}...")
                    progress.progress((i + 1) * 50)
                    result = generate_content_raw(final_api_key, model, user_script)
                    
                    if "ERROR" not in result:
                        st.markdown("---")
                        st.success(f"✅ Generation Complete via {model}")
                        st.markdown(result)
                        success = True
                        status.empty()
                        progress.empty()
                        break
                    else:
                        st.warning(f"⚠️ {model} unresponsive...")
                
                if not success:
                    st.error("❌ System Failure.")
                    st.code(result)
            else:
                st.warning("⚠️ Input Buffer Empty")

elif password_input:
    st.sidebar.error("❌ Access Denied")
