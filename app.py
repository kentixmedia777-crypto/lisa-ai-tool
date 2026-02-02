import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION (THE LOCK) ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- YOUR SECRET JSON RECIPE (HIDDEN) ---
LISA_SYSTEM_PROMPT = """
You are Lisa, an AI Image Prompt Generator Assistant (v4.1).
Your User Nickname is "Oppa sarangheyeo".
Your specialization is Hyper-realistic, raw, unedited 'found footage' style image generation prompts.

Here are your STRICT Protocols (The JSON Rules):
1. **THE_RAFAEL_STANDARD**: Visual fidelity: Images must look like throwaway smartphone snapshots. Skin Texture: Visible pores, natural sebum. Lighting: Diffused window light OR harsh direct flash.
2. **UNIQUE_GENETICS_RULE**: Assign specific, unique facial geometry to every new character.
3. **NORMAL_DAY_RULE**: Setting MUST be 'Home' or 'Leisure'. STRICTLY FORBIDDEN: Workplaces.
4. **SOCIOECONOMIC_CONSISTENCY**: Match environment to financial status.
5. **HAPPY_MASK_PROTOCOL**: POSITIVE/RELAXED expressions only. NO sad/crying.
6. **THE_CAST_FILTER**: Focus only on victims/perpetrators. No police/doctors.
7. **MINOR_CHARACTER_BYPASS**: IF minor: Use 'Candid family photo', 'wholesome'.

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
            with st.spinner("Lisa is attempting to connect to Google Brain..."):
                try:
                    # Setup Gemini with Lucas's Key
                    genai.configure(api_key="AIzaSyAuFkvo7ToqHQ4vCpyT2RDvkZGzL6TClXw")
                    
                    # --- SOLOMON'S SMART SELECTOR ---
                    # This logic tries multiple models until one works.
                    model = None
                    model_attempts = [
                        'gemini-1.5-flash',
                        'gemini-1.5-pro',
                        'gemini-1.5-flash-001',
                        'gemini-1.5-pro-001',
                        'gemini-pro',
                        'gemini-1.0-pro'
                    ]
                    
                    last_error = ""
                    success_model = ""

                    for m_name in model_attempts:
                        try:
                            # Try to initialize the model
                            test_model = genai.GenerativeModel(m_name)
                            # Combine Prompt
                            full_prompt = f"{LISA_SYSTEM_PROMPT}\n\nHere is the Script to analyze:\n{user_script}"
                            # Try to Generate
                            response = test_model.generate_content(full_prompt)
                            # If we get here, it worked!
                            model = test_model
                            success_model = m_name
                            break # Stop the loop, we found a winner
                        except Exception as e:
                            last_error = e
                            continue # Try the next one
                    
                    if model:
                        # Display Result
                        st.divider()
                        st.write(f"### ✅ Lisa's Output (Engine: {success_model}):")
                        st.markdown(response.text)
                    else:
                        st.error(f"System Error: Could not connect to any Gemini models. Last Error: {last_error}")
                    
                except Exception as e:
                    st.error(f"Critical System Error: {e}")
        else:
            st.warning("Please paste a script first.")
            
elif password_input:
    st.sidebar.error("❌ Access Denied. Contact Kent for access.")
else:
    st.info("Please enter the password to access Lisa.")
