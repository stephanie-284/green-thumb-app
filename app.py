import streamlit as st
import google.generativeai as genai

# 1. SETUP & FAVICON
# To use a custom favicon, you can use an emoji or a URL to an image
st.set_page_config(
    page_title="Green-Thumb Garden Planner", 
    page_icon="🌴", # You can replace this with a URL to a .png or .ico file later
    layout="wide"
)

# Accessing the secret key
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("API Key not found. Please check your Streamlit Secrets.")

model = genai.GenerativeModel('gemini-3-flash-preview')

# 2. UI STYLING (The "First Round" of UI)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f1;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
    }
    </style>
    """, unsafe_allow_index=True)

# 3. SIDEBAR FORM
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/photos_96dp.png", width=100) # Placeholder for a logo
    st.title("Green-Thumb")
    st.markdown("---")
    
    # Using a form prevents the app from refreshing every time you type a letter
    with st.form("garden_form"):
        zip_code = st.text_input("Zip Code", placeholder="30060")
        light_level = st.selectbox("Sunlight", ["Full Sun", "Partial Shade", "Full Shade"])
        recipe_choice = st.selectbox("Style", ["Lush Tropical", "Dwarf Evergreens", "Native Pollinators", "Modern Minimalist"])
        thriving_plants = st.text_input("What is already thriving here?", placeholder="e.g. Ivy, Ferns")
        
        # The button is now inside the sidebar form
        submit_button = st.form_submit_button("Create My Garden Plan")

# 4. MAIN CONTENT AREA
st.title("🌿 Your Personal Landscape Architect")
st.write("Enter your yard's details on the left to see your 3-year transformation plan.")

if submit_button:
    if not zip_code:
        st.info("Please enter your Zip Code in the sidebar to begin.")
    else:
        with st.spinner("Designing your oasis..."):
            context = f"Thriving plants: {thriving_plants}." if thriving_plants else "Standard conditions."
            
            prompt = f"""
            Act as an expert ecological landscape designer. 
            Location: Zip Code {zip_code}. Light: {light_level}. Style: {recipe_choice}.
            Context: {context}
            User Goal: Low-maintenance, NO grass. Provide a 3-year plan with bold headers.
            """

            try:
                response = model.generate_content(prompt)
                st.markdown("### Your Custom 3-Year Roadmap")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
