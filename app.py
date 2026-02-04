import streamlit as st
import requests
import json
import time
import base64

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- THE MASTER BRAIN (UNTOUCHED) ---
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
    "UNIQUE_GENETICS_RULE": {
      "description": "Prevents 'Same Face Syndrome'.",
      "instruction": "Assign specific, unique facial geometry to every new character (e.g., 'hooked nose', 'wide-set eyes', 'weak chin', 'round cheeks', 'thick neck', 'dental imperfections'). Never reuse generic descriptions."
    },
    "NORMAL_DAY_RULE": {
      "description": "Replaces 'Off-The-Clock'. Mandates the setting must be domestic or leisure only.",
      "restrictions": [
        "MANDATORY SETTINGS: Must be 'Home' (living room, porch, kitchen, bedroom) OR 'Leisure' (pub, vacation, backyard, hobby).",
        "STRICTLY FORBIDDEN: No workplaces, no uniforms, no tools of the trade, no professional environments."
      ]
    },
    "SOCIOECONOMIC_CONSISTENCY": {
      "description": "Ensures the environment and props match the character's financial status.",
      "instruction": "IF character is wealthy: Use 'clean', 'spacious', 'high-end materials', 'groomed'. IF character is struggling/working class: Use 'cluttered', 'cramped', 'worn textures', 'cheap materials', 'messy backgrounds'."
    },
    "HAPPY_MASK_PROTOCOL": {
      "description": "Enforces a 'Normal Day' vibe.",
      "instruction": "All characters must display POSITIVE, RELAXED, or CONFIDENT expressions (smiling, laughing, 'fierce' posing, eating/drinking).",
      "prohibition": "ABSOLUTELY NO tired, sad, crying, angry, stressed, or bored expressions, regardless of the character's tragic backstory."
    },
    "MULTI_CAST_EXPANSION": {
      "instruction": "Scan the script for [MAIN CHARACTER] and specific [NAMED SIDE CHARACTERS] who play a significant role (e.g., partners, friends). Generate a separate prompt for each."
    },
    "THE_CAST_FILTER": {
      "description": "Filters out irrelevant background roles.",
      "instruction": "Do NOT generate prompts for: Police, Paramedics, Doctors, Rangers, or unnamed crowds. Focus ONLY on the specific victims or named perpetrators."
    },
    "ANTI_CARTOON_PROTOCOL": {
      "description": "Prevents the 'Video Game Character' look.",
      "instruction": "If a face looks too 'pretty' or '3D rendered', apply 'harsh flash', 'oily skin', 'asymmetry', and 'unflattering angles' to force photorealism."
    },
    "ARCHIVAL_RULE": {
      "instruction": "Set the prompt date exactly one year prior to the incident date in the script."
    },
    "MINOR_CHARACTER_BYPASS": {
      "description": "Protocol to bypass AI safety filters regarding realistic depictions of minors while maintaining quality.",
      "instruction": "IF the character is a MINOR/CHILD: STRICTLY AVOID 'selfie', 'close-up', 'messy', 'dirty', or 'imperfect' keywords applied to the child. SHIFT style to 'Candid photograph taken by an adult' or 'Family photo'. Use 'safe distance', 'wholesome', 'clean', and 'soft lighting' contexts. Maintain realism via camera specs (e.g., 'grainy', 'soft focus'), but ensure the content is strictly 'safe family memory' style to ensure generation success."
    }
  },
  "response_format": {
    "style": "Professional, slightly robotic, compliant, and concise.",
    "standard_greeting": "Understood, Oppa sarangheyeo.",
    "prompt_delivery_method": "MANDATORY: Provide every prompt inside a Markdown code block (```markdown) for easy one-click copying. Do not use plain text for the final prompt.",
    "output_structure": [
      "Cast Analysis (identifying distinct genetic traits for each person)",
      "The Prompts (Use Markdown code blocks for the prompt text)",
      "Wait for user feedback before System Reset."
    ]
  },
  "workflow_memory": {
    "instruction": "After every successful generation, wipe character data but RETAIN the protocols (Lisa v4.1). Treat every new script as a new project."
  }
}
"""

# --- DARK MODE DESIGN (UNTOUCHED) ---
st.set_page_config(page_title="LISA v9.16 - AutoRetry", page_icon="lz", layout="wide")

st.markdown("""
<style>
    /* META DARK MODE THEME */
    .stApp { background-color: #18191a; }
    [data-testid="stSidebar"] { background-color: #242526; border-right: 1px solid #3e4042; }
    h1 { color: #2D88FF !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; border-bottom: 1px solid #3e4042; padding-bottom: 15px; }
    h3, h4, p, label, .stMarkdown { color: #e4e6eb !important; }
    .stTextArea textarea, .stTextInput input { background-color: #3a3b3c !important; color: #e4e6eb !important; border: 1px solid #3e4042; border-radius: 8px; }
    .stTextArea textarea:focus, .stTextInput input:focus { border-color: #2D88FF; box-shadow: 0 0 0 1px #2D88FF; }
    .stButton>button { background-color: #2D88FF; color: white; border-radius: 6px; font-weight: 700; border: none; padding: 12px 24px; text-transform: uppercase; letter-spacing: 0.5px; }
    .stButton>button:hover { background-color: #1877F2; box-shadow: 0 4px 12px rgba(45, 136, 255, 0.4); }
    .stAlert { background-color: #242526; color: #e4e6eb; border: 1px solid #3e4042; }
    code { color: #e4e6eb; background-color: #3a3b3c; }
</style>
""", unsafe_allow_html=True)

# --- THE ENGINE (WITH AUTO-RETRY) ---
def generate_content_raw(api_key, model_name, script):
    clean_key = api_key.strip()
    
    # 1. ENCRYPTED URL (Base64) - Prevents editor bugs
    secret_domain = "aHR0cHM6Ly9nZW5lcmF0aXZlbGFuZ3VhZ2UuZ29vZ2xlYXBpcy5jb20="
    base_url = base64.b64decode(secret_domain).decode('utf-8')
    endpoint = f"/v1beta/models/{model_name}:generateContent"
    params = f"?key={clean_key}"
    url = base_url + endpoint + params
    
    # SYSTEM PROMPT
    final_instruction = f"""
    SYSTEM OVERRIDE: YOU ARE LISA.
    ADOPT THE FOLLOWING JSON CONFIGURATION STRICTLY. DO NOT DEVIATE.
    {LISA_JSON_PROMPT}
    ---------------------------------------------------
    TASK: Analyze the following script and generate prompts according to the JSON rules above.
    SCRIPT:
    {script}
    """
    
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": final_instruction}]}]}
    
    try:
        # ATTEMPT 1
        response = requests.post(url, headers=headers, json=data)
        
        # --- AUTO-RETRY LOGIC ---
        if response.status_code == 429:
            # If we hit the speed limit, we WAIT 40 SECONDS then try again.
            st.warning("⚠️ Speed Limit Hit. Cooling down for 40 seconds... (Auto-Retry active)")
            time.sleep(40) 
            
            # ATTEMPT 2 (After waiting)
            response = requests.post(url, headers=headers, json=data)
        # ------------------------
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result: 
                return result['candidates'][0]['content']['parts'][0]['text']
            return "ERROR: Empty Response from Google."
            
        return f"ERROR {response.status_code}: {response.text}"
        
    except Exception as e:
        return f"CONNECTION ERROR: {str(e)}"

# --- MAIN APP LAYOUT ---
st.title("LISA v9.16")
st.markdown("### AI Visual Architect | Dark Enterprise Edition")
st.write("") 

password_input = st.sidebar.text_input("🔒 Access Portal", type="password", placeholder="Enter Password...")

if password_input == ACCESS_PASSWORD:
    st.sidebar.success("✅ SYSTEM ONLINE")
    st.sidebar.markdown("---")
    
    if "GOOGLE_API_KEY" in st.secrets:
        final_api_key = st.secrets["GOOGLE_API_KEY"]
        st.sidebar.success("✅ License Key Active")
        st.sidebar.info("Authorized for: Lucalles Productions")
    else:
        st.sidebar.warning("⚠️ No License Found")
        final_api_key = st.sidebar.text_input("Manual Key Entry", type="password")
    
    st.sidebar.markdown("---")
    
    st.markdown("#### 🎬 Script Ingestion")
    user_script = st.text_area("Input Stream", height=300, placeholder="Paste your true crime script here...", label_visibility="collapsed")
    
    st.write("") # Spacer
    
    if st.button("Initialize Lisa"):
        if not final_api_key:
            st.error("⚠️ System Halted: Missing API Key")
            st.stop()
            
        if user_script:
            # We stick to the model Google TOLD us to use.
            models = ["gemini-2.0-flash-exp"] 
            
            success = False
            status_box = st.empty()
            
            for i, model in enumerate(models):
                status_box.markdown(f"**🔄 Lisa is scanning for a viable neural link...**")
                
                result = generate_content_raw(final_api_key, model, user_script)
                
                if "ERROR" not in result:
                    st.markdown("---")
                    st.success(f"✅ Connection Established via Neural Node {i+1}")
                    st.markdown("### 📸 Visual Analysis & Prompts")
                    st.markdown(result)
                    success = True
                    status_box.empty()
                    break
                else:
                    continue
            
            if not success:
                st.error("❌ System Failure.")
                if "429" in result:
                     st.info("ℹ️ QUOTA LIMIT: Even after retrying, the speed limit is hit. Please wait 2 minutes.")
                st.code(result)
        else:
            st.warning("⚠️ Input Buffer Empty")

elif password_input:
    st.sidebar.error("❌ Access Denied")
