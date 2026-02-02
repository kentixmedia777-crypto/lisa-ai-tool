import streamlit as st
import google.generativeai as genai

st.title("🛠 Solomon's Diagnostic Tool")

# Your API Key
genai.configure(api_key="AIzaSyBYGKCsOg0-1VmyGAypodNqwcQHSo1fun4")

st.write("Contacting Google to see available AI models...")

try:
    # This asks Google to list every model this Key can access
    found_any = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.success(f"✅ FOUND: {m.name}")
            found_any = True
            
    if not found_any:
        st.error("❌ No models found. The API Key might be invalid or has no credits.")

except Exception as e:
    st.error(f"❌ CONNECTION ERROR: {e}")
    st.write("This usually means the 'Generative Language API' is not enabled for this Key.")
