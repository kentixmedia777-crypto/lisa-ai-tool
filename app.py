import streamlit as st
import subprocess
import sys

# --- FORCE UPGRADE (THE NUCLEAR FIX) ---
# This forces the server to download the new Brain Software immediately.
try:
    import google.generativeai as genai
    # Check if the version is old. If it is, force upgrade.
    version = genai.__version__
    if version < "0.7.0":
        st.warning(f"⚠️ Old Brain Software detected (v{version}). Upgrading now... please wait 10 seconds...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "google-generativeai"])
        st.success("✅ Upgrade Complete! Please refresh the page.")
        st.stop()
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    st.experimental_rerun()

# --- NOW IMPORT THE FRESH LIBRARY ---
import google.generativeai as genai
import time

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- THE SYSTEM PROMPT ---
LISA_SYSTEM_PROMPT = """
You are Lisa, an AI Image Prompt Generator Assistant.
Your User Nickname is "Oppa sarangheyeo".

**STRICT SYSTEM INSTRUCTIONS (JSON FORMAT):**
{
  "system_identity": {
    "name": "Lisa",
    "version": "v4.3",
    "status": "ONLINE"
  },
  "core_directive": "Analyze true crime/tragedy scripts and generate specific Midjourney prompts. Goal: 'last normal photo' taken 1 year prior to incident.",
  "active_protocols": {
    "THE_RAFAEL_STANDARD": {
      "visual_fidelity": "Throwaway smartphone snapshots. NO digital art.",
      "mandatory_elements": ["visible pores", "natural sebum/oil", "faint acne scars", "razor burn", "harsh direct flash", "red-eye effect", "digital grain", "low dynamic range"]
    },
    "NORMAL_DAY_RULE": {
      "restrictions": ["MANDATORY: Home or Leisure settings.", "FORBIDDEN: Workplaces, uniforms, crime scenes."]
    },
    "HAPPY_MASK_PROTOCOL": {
      "instruction": "All characters must display POSITIVE expressions (smiling, laughing). NO sad/angry faces."
    }
  },
  "response_format": {
    "prompt_delivery_method": "Provide every prompt inside a Markdown code block."
  }
}
"""

# --- THE WEBSITE INTERFACE ---
st.set_page_config(page_title="Lisa v4.3 - AI Generator", page_icon="📸")

st.title("📸 Lisa v4.3: Image Prompt Generator")

# 1. Password Protection
password_input = st.sidebar.text_input("Enter Access Password", type="password")

if password_input == ACCESS_PASSWORD:
    st.sidebar.success("✅ Access Granted")
    
    # 2. Input Area
    st.write("### Paste the Script Below:")
    user_script = st.text_area("Script Input", height=300, placeholder="Paste the true crime script here...")
    
    if st.button("Activate Lisa"):
        if user_script:
            
            # --- THE HYDRA STRATEGY ---
            model_list = [
                "gemini-1.5-flash",
                "gemini-1.5-flash-latest",
                "gemini-pro"
            ]
            
            success = False
            error_log = []

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
                    model = genai.GenerativeModel(model_name)
                    full_prompt = f"{LISA_SYSTEM_PROMPT}\n\nScript:\n{user_script}"
                    response = model.generate_content(full_prompt)
                    
                    st.divider()
                    st.success(f"✅ Success! Connected to Brain: {model_name}")
                    st.write("### 📸 Lisa's Output:")
                    st.markdown(response.text)
                    success = True
                    progress_bar.progress(100)
                    status_text.text("Done.")
                    break
                    
                except Exception as e:
                    error_log.append(f"{model_name} failed: {str(e)}")
                    time.sleep(1)
                    continue
            
            if not success:
                st.error("❌ All Brains Failed.")
                with st.expander("See Error Details"):
                    for err in error_log:
                        st.write(err)

        else:
            st.warning("Please paste a script first.")
            
elif password_input:
    st.sidebar.error("❌ Access Denied.")
else:
    st.info("Please enter the password.")
