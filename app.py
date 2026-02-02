import streamlit as st
import google.generativeai as genai

st.title("🛠 Lucas's Key Diagnostic")

# Lucas's Key
genai.configure(api_key="AIzaSyAuFkvo7ToqHQ4vCpyT2RDvkZGzL6TClXw")

st.write("Asking Google what models this key can use...")

try:
    found_any = False
    # This command asks Google to list ONLY what this key can touch
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.success(f"✅ AVAILABLE: {m.name}")
            found_any = True
            
    if not found_any:
        st.error("❌ NO MODELS FOUND. This Key might be invalid, restricted, or disabled.")
        st.write("Double check that the 'Generative Language API' is enabled in Lucas's Google Cloud Console.")

except Exception as e:
    st.error(f"❌ CRITICAL ERROR: {e}")
    st.write("This usually means the API Key is typed wrong or has been deleted.")
