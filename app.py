import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Green-Thumb AI", page_icon="🌿", layout="centered")

# Custom Styling for the "Airy" look
st.markdown("""
    <style>
    .main { background-color: #f4f7f4; }
    .stButton>button { 
        background-color: #2e7d32; 
        color: white; 
        border-radius: 25px; 
        padding: 0.6rem 2rem;
        border: none;
    }
    h1, h2, h3 { color: #1b5e20; }
    .stSelectbox, .stTextInput { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# This tells Streamlit to look in your secrets.toml file (locally) 
# or the "Secrets" dashboard (when live on the web)
API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

# Header Section
st.title("🌿 Green-Thumb")
st.markdown("### Your 3-Year Garden Sanctuary")
st.write("Designed for black-thumbs, green-thumbs, and everyone under the oaks.")

# 2. Input Canvas
with st.expander("📍 Step 1: Tell us about your yard", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        zip_code = st.text_input("Zip Code", placeholder="e.g. 30060")
    with col2:
        light_level = st.selectbox("Light Level", ["Full Sun", "Part Shade/Dappled", "Deep Shade"])
    
    thriving_plants = st.text_input("What is already growing well in this spot? (e.g. Hostas, Ivy, Moss, etc.)")

recipe_choice = st.selectbox("Step 2: Choose your Vibe (Recipe)", [
    "Dwarf Evergreens (The Winter Flow)", 
    "Songbird Sanctuary (Native Berries)", 
    "Moonlight Path (White Blooms & Silver)"
])

# 3. Generation Logic
if st.button("Generate My Personalized Plan"):
    if not zip_code:
        st.warning("Please enter a zip code so we can map your Hardiness Zone!")
    else:
        with st.spinner("Consulting the horticultural brain..."):
            # The "Horticulture Prompt" Logic
            oak_context = "The user has large oaks; prioritize acid-loving plants and protect root zones." if under_oaks else ""
            
            prompt = f"""
            Act as an expert ecological landscape designer. 
            Location: Zip Code {zip_code}. Light: {light_level}. Recipe: {recipe_choice}.
            User Goal: Low-maintenance, NO manicured grass, year-round flow. 
            {oak_context}

            Structure your response with:
            1. **Your Zone:** Identify the USDA Hardiness Zone.
            2. **The 3-Year Roadmap:** - Year 1: The 'Bones' (Dwarf structural plants).
               - Year 2: The 'Soul' (Mid-layer texture and seasonal color).
               - Year 3: The 'Seal' (Evergreen groundcovers to replace grass/weeds).
            3. **Black-Thumb Safety Tip:** One easy hack to keep these specific plants alive.
            
            Use supportive, clear, and 'airy' formatting. Focus on DWARF versions of plants.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                
                # Success Sidebar
                st.sidebar.success("✅ Plan Generated")
                st.sidebar.info("Next Step: Save this plan. We'll start your Price Watch for Year 1 'Bones' soon!")
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# Footer
st.markdown("---")
st.caption("MVP 1.0 | Built with Gemini & Streamlit")
