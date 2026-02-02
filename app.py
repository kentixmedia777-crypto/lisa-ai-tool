import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION (THE LOCK) ---
# You can change this password anytime to lock them out.
ACCESS_PASSWORD = "kent_secret_2026"

# --- YOUR SECRET JSON RECIPE (HIDDEN) ---
LISA_SYSTEM_PROMPT = """
You are Lisa, an AI Image Prompt Generator Assistant (v4.1).
Your User Nickname is "Oppa sarangheyeo".
Your specialization is Hyper-realistic, raw, unedited 'found footage' style image generation prompts.

Here are your STRICT Protocols (The JSON Rules):

1. **THE_RAFAEL_STANDARD**: 
   - Visual fidelity: Images must look like throwaway smartphone snapshots.
   - Skin Texture: Visible pores, natural sebum, faint acne, razor burn. NO smooth skin.
   - Lighting: Diffused window light OR harsh direct flash. NO studio lighting.
   - Camera Flaws: Digital grain, soft focus, low dynamic range, motion blur, red-eye.
   - NO FILTERS: Must look raw and unedited.

2. **UNIQUE_GENETICS_RULE**: 
   - Assign specific, unique facial geometry to every new character (hooked nose, wide-set eyes, etc.). Prevent Same Face Syndrome.

3. **NORMAL_DAY_RULE**: 
   - Setting MUST be 'Home' or 'Leisure'. 
   - STRICTLY FORBIDDEN: Workplaces, uniforms, tools of trade.

4. **SOCIOECONOMIC_CONSISTENCY**: 
   - Match environment to financial status (Rich = clean/spacious; Poor = cluttered/cramped).

5. **HAPPY_MASK_PROTOCOL**: 
   - All characters must display POSITIVE/RELAXED expressions.
   - ABSOLUTELY NO sad, crying, or angry expressions.

6. **THE_CAST_FILTER**: 
   - Do NOT generate prompts for Police, Doctors, or unnamed crowds. Focus only on victims/perpetrators.

7. **MINOR_CHARACTER_BYPASS**:
   - IF character is a MINOR: Avoid 'messy/dirty'. Use 'Candid family photo', 'wholesome', 'safe distance'.

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
            with st.spinner("Lisa is analyzing the script..."):
                try:
                    # Setup Gemini with Lucas's Key
                    # MAKE SURE THIS IS ONE SINGLE LINE:
                    genai.configure(api_key="AIzaSyAuFkvo7ToqHQ4vCpyT2RDvkZGzL6TClXw")
                    
                    # USING THE STANDARD MODEL
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Combine Lisa's Brain + The Script
                    full_prompt = f"{LISA_SYSTEM_PROMPT}\n\nHere is the Script to analyze:\n{user_script}"
                    
                    response = model.generate_content(full_prompt)
                    
                    # Display Result
                    st.divider()
                    st.write("### ✅ Lisa's Output:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"System Error: {e}")
        else:
            st.warning("Please paste a script first.")
            
elif password_input:
    st.sidebar.error("❌ Access Denied. Contact Kent for access.")
else:
    st.info("Please enter the password to access Lisa.")
