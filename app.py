import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURATION (THE LOCK) ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- YOUR SECRET JSON RECIPE (HIDDEN) ---
LISA_SYSTEM_PROMPT = """
You are Lisa, an AI Image Prompt Generator Assistant (v4.1).
Your User Nickname is "Oppa sarangheyeo".
Your specialization is Hyper-realistic, raw, unedited 'found footage' style image generation prompts.

Here are your STRICT Protocols (The JSON Rules):
1. **THE_RAFAEL_STANDARD**: Visual fidelity: Images must look like throwaway smartphone snapshots. Skin Texture: Visible pores. Lighting: Diffused window light OR harsh direct flash.
2. **UNIQUE_GENETICS_RULE**: Assign specific, unique facial geometry to every new character.
3. **NORMAL_DAY_RULE**: Setting MUST be 'Home' or 'Leisure'. STRICTLY FORBIDDEN: Workplaces.
4. **SOCIOECONOMIC_CONSISTENCY**: Match environment to financial status.
5. **HAPPY_MASK_PROTOCOL**: POSITIVE/RELAXED expressions only. NO sad/crying.
6. **THE_CAST_FILTER**: Focus only on victims/perpetrators. No police/doctors.
7. **MINOR_CHARACTER_BYPASS**: IF minor: Use 'Candid family photo', 'wholesome', 'safe distance'.

**YOUR TASK:**
The user will paste a True Crime Script. 
You must analyze it and generate specific Midjourney prompts for the main characters based on the rules above.
Output the prompts inside Markdown code blocks.
Start your response with: "Understood, Oppa sarangheyeo."
"""

# --- THE WEBSITE INTERFACE ---
st.set_page_config(page_title="Lisa v4.1 - AI Generator", page_icon="📸")

st.title("📸 Lisa v4.1: Image Prompt Generator")
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
            with st.spinner("Lisa is finding a working brain..."):
                
                # Setup Gemini with Lucas's Key
                genai.configure(api_key="AIzaSyAuFkvo7ToqHQ4vCpyT2RDvkZGzL6TClXw")
                
                # --- SOLOMON'S AUTO-SWITCHER ---
                # We try these models in order. If one fails, we try the next.
                # based on your specific scan results.
                model_list = [
                    "gemini-flash-latest",       # Try 1: The generic alias (Usually safest)
                    "gemini-pro-latest",         # Try 2: The generic Pro alias
                    "gemini-2.0-flash-exp",      # Try 3: Experimental Flash
                    "gemini-1.5-flash",          # Try 4: Old Reliable Flash
                    "gemini-1.5-pro"             # Try 5: Old Reliable Pro
                ]

                success = False
                last_error = ""

                for model_name in model_list:
                    try:
                        # Attempt to use this model
                        model = genai.GenerativeModel(model_name)
                        full_prompt = f"{LISA_SYSTEM_PROMPT}\n\nHere is the Script to analyze:\n{user_script}"
                        
                        # Generate
                        response = model.generate_content(full_prompt)
                        
                        # If we get here, IT WORKED!
                        st.divider()
                        st.success(f"✅ Generated using Engine: {model_name}")
                        st.write("### 📸 Lisa's Output:")
                        st.markdown(response.text)
                        success = True
                        break # Stop the loop
                        
                    except Exception as e:
                        # If it fails, just record the error and continue to the next model
                        last_error = e
                        continue
                
                if not success:
                    st.error("❌ All models failed. The API Key might be hitting a total rate limit.")
                    st.error(f"Last Error details: {last_error}")

        else:
            st.warning("Please paste a script first.")
            
elif password_input:
    st.sidebar.error("❌ Access Denied. Contact Kent for access.")
else:
    st.info("Please enter the password to access Lisa.")
