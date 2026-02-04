import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- THE SYSTEM PROMPT (FULL JSON MODE) ---
LISA_SYSTEM_PROMPT = """
You are Lisa, an AI Image Prompt Generator Assistant.
Your User Nickname is "Oppa sarangheyeo".

**STRICT SYSTEM INSTRUCTIONS (JSON FORMAT):**
{
  "system_identity": {
    "name": "Lisa",
    "version": "v4.2",
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
        "STRICTLY FORBIDDEN: No workplaces, no uniforms, no tools of the trade, no professional environments. NO CRIME SCENES."
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
      "instruction": "Do NOT generate prompts for: Police, Paramedics, Doctors, Rangers, BOATS, OBJECTS, or unnamed crowds. Focus ONLY on the specific victims or named perpetrators."
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
  }
}
"""

# --- THE WEBSITE INTERFACE ---
st.set_page_config(page_title="Lisa v4.2 - AI Generator", page_icon="📸")

# --- SOLOMON'S INVISIBILITY CLOAK ---
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("📸 Lisa v4.2: Image Prompt Generator")
st.markdown("*System Status: ONLINE*")

# 1. Password Protection
password_input = st.sidebar.text_input("Enter Access Password", type="password")

if password_input == ACCESS_PASSWORD:
    st.sidebar.success("✅ Access Granted")
    
    # 2. Input Area
    st.write("### Paste the Script Below:")
    user_script = st.text_area("Script Input", height=300, placeholder="Paste the true crime script here...")
    
    if st.button("Activate Lisa"):
        if user_script:
            
            # --- THE HYDRA STRATEGY (UPDATED) ---
            # We removed the broken "1.5-pro" model and added safer backups.
            model_list = [
                "gemini-1.5-flash",           # Priority 1: High Quota, Very Stable
                "gemini-1.5-flash-latest",    # Priority 2: The latest version of Flash
                "gemini-pro"                  # Priority 3: The "Legacy" 1.0 model (The Safety Net)
            ]
            
            success = False
            error_log = []

            # Connect to the Safe
            try:
                if "GOOGLE_API_KEY" in st.secrets:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                else:
                    st.error("❌ Key Error: Secret 'GOOGLE_API_KEY' not found.")
                    st.stop()
            except Exception as e:
                st.error(f"Configuration Error: {e}")
                st.stop()

            # Start the Search for a Brain
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, model_name in enumerate(model_list):
                status_text.text(f"Lisa is looking for a working brain... (Trying: {model_name})")
                progress_bar.progress((i + 1) * 33)
                
                try:
                    # Initialize the specific model
                    model = genai.GenerativeModel(model_name)
                    full_prompt = f"{LISA_SYSTEM_PROMPT}\n\nHere is the Script to analyze:\n{user_script}"
                    
                    # Generate
                    response = model.generate_content(full_prompt)
                    
                    # IF WE REACH HERE, IT WORKED!
                    st.divider()
                    st.success(f"✅ Success! Connected to Brain: {model_name}")
                    st.write("### 📸 Lisa's Output:")
                    st.markdown(response.text)
                    success = True
                    progress_bar.progress(100)
                    status_text.text("Done.")
                    break # Stop looping, we found a winner.
                    
                except Exception as e:
                    # If this brain fails, record error and try the next
                    error_log.append(f"{model_name} failed: {str(e)}")
                    time.sleep(1) # Brief pause
                    continue
            
            if not success:
                st.error("❌ All Brains Failed.")
                # Show all errors so we know exactly what happened
                with st.expander("See Error Details"):
                    for err in error_log:
                        st.write(err)
                st.info("The servers might be overloaded. Please wait 1 minute and try again.")

        else:
            st.warning("Please paste a script first.")
            
elif password_input:
    st.sidebar.error("❌ Access Denied. Contact Kent for access.")
else:
    st.info("Please enter the password to access Lisa.")
