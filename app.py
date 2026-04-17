import streamlit as st
import google.generativeai as genai

# 1. Setup and Security
st.set_page_config(page_title="Yard to Garden Planner")

# Accessing the secret key we set up
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("API Key not found. Please check your Streamlit Secrets.")

# Using the Gemini 3 model that worked in your test
model = genai.GenerativeModel('gemini-3-flash-preview')

# 2. The User Interface
st.title("Yard to Garden Planner")
st.markdown("### Turn grass and weeds into a low-maintenance oasis for your specific location.")

with st.sidebar:
    st.header("Your Yard Details")
    zip_code = st.text_input("Zip Code", placeholder="xxxxx")
    light_level = st.selectbox("Light", ["Full Sun", "Part Sun / Part Shade", "Full Shade"])
    recipe_choice = st.selectbox("Choose a Style", ["Dwarf Evergreens", "Native Pollinators", "Lush Tropical", "Modern Minimalist"])
    
    # New soil/environment logic replacing the Oak checkbox
    thriving_plants = st.text_input("What is growing well here now?", placeholder="e.g. Ivy, Moss, Azaleas")

# 3. The Logic Engine
if st.button("Create My Garden Oasis Plan"):
    if not zip_code:
        st.warning("Please enter a zip code to get started.")
    else:
        with st.spinner("Consulting the horticultural brain..."):
            # Determine context based on thriving plants
            if thriving_plants:
                context = f"The following plants are already thriving here: {thriving_plants}. Use this to infer soil pH and light levels."
            else:
                context = "Assume standard gardening conditions for this zip code."

            # Constructing the instructions
            prompt = f"""
            Act as an expert ecological landscape designer. 
            Location: Zip Code {zip_code}. Light: {light_level}. Style: {recipe_choice}.
            User Goal: Low-maintenance, NO manicured grass, year-round flow. 
            Context: {context}

            Please provide a specific 3-year planting and maintenance plan. 
            Include specific plant names that thrive in this climate zone.
            Format with bold headers for each year.
            """

            try:
                response = model.generate_content(prompt)
                
                st.success("Your 3-Year Plan is Ready!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.markdown("---")
st.caption("Built for those who want a low-maintenance garden, not a high-maintenance yard.")
