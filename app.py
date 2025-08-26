import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import io
import requests
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Animal Breed Identifier",
    page_icon="🐾",
    layout="wide"
)

# Initialize Gemini API
def configure_genai():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Please set GEMINI_API_KEY in your .env file")
        st.stop()
    genai.configure(api_key=api_key)

configure_genai()

# Function to get Gemini response
def get_gemini_response(image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([image, prompt])
    return response.text

# Function to identify animal breed
def identify_animal_breed(image):
    prompt = """
    Analyze this image and identify the animal and its specific breed. 
    Provide a detailed response in the following format:
    
    **Animal:** [Animal type]
    **Breed:** [Specific breed if identifiable]
    
    **Physical Characteristics:**
    - [Characteristic 1]
    - [Characteristic 2]
    - [Characteristic 3]
    
    **Temperament:**
    - [Temperament trait 1]
    - [Temperament trait 2]
    
    **Care Requirements:**
    - [Care requirement 1]
    - [Care requirement 2]
    
    **Safety Assessment:**
    - [Danger level: Low/Medium/High]
    - [Potential risks]
    - [Safety precautions]
    
    **Additional Information:**
    [Any other relevant information about this animal breed]
    
    If the image doesn't contain a recognizable animal, please state that clearly.
    """
    return get_gemini_response(image, prompt)

# Function to get animal facts
def get_animal_facts(animal_type):
    prompt = f"""
    Provide interesting facts about {animal_type} in a bullet point format.
    Include information about their:
    - Natural habitat
    - Diet
    - Social behavior
    - Unique adaptations
    - Conservation status (if applicable)
    """
    # For text-only prompts, we can use a different approach
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Main app
def main():
    st.title("🐾 Animal Breed Identification System")
    st.markdown("Upload an image of an animal to identify its breed and learn about its characteristics.")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.header("Instructions")
        st.write("1. Upload a clear image of an animal")
        st.write("2. The AI will identify the animal and its breed")
        st.write("3. View detailed information about the animal")
        st.write("4. Learn about safety considerations")
        
        st.header("Supported Animals")
        st.write("Dogs, Cats, Birds, Exotic Pets, and more!")
    
    # File upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Process the image
        with st.spinner("Analyzing image..."):
            try:
                # Identify animal breed
                response = identify_animal_breed(image)
                
                # Display results
                st.success("Analysis Complete!")
                
                # Create tabs for different information sections
                tab1, tab2, tab3 = st.tabs(["Breed Information", "Safety Assessment", "Animal Facts"])
                
                with tab1:
                    st.subheader("Breed Identification & Characteristics")
                    st.markdown(response)
                
                with tab2:
                    # Extract safety information
                    if "**Safety Assessment:**" in response:
                        safety_section = response.split("**Safety Assessment:**")[1].split("**Additional Information:**")[0]
                        st.markdown(safety_section)
                    else:
                        st.info("Safety assessment information not available for this animal.")
                
                with tab3:
                    # Extract animal type for facts
                    if "**Animal:**" in response:
                        animal_type = response.split("**Animal:**")[1].split("**Breed:**")[0].strip()
                        st.subheader(f"Interesting Facts About {animal_type}s")
                        facts = get_animal_facts(animal_type)
                        st.markdown(facts)
                    else:
                        st.info("Animal facts not available.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please try again with a different image.")

    else:
        # Show sample images
        st.subheader("Try with these sample images:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/800px-Cat_November_2010-1a.jpg", 
                    caption="Sample Cat", use_column_width=True)
        
        with col2:
            st.image("https://imgs.search.brave.com/8UIgd2rGu-w5WNHs1LSAieexcDqKt4liuafSLSDQwHk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWFn/ZXMuZnJlZWltYWdl/cy5jb20vaW1hZ2Vz/L2xhcmdlLXByZXZp/ZXdzL2NlNy9oYXBw/eS1ibGFjay1kb2ct/MDQxMC01NzAxNTc5/LmpwZz9mbXQ", 
                    caption="Sample Dog", use_column_width=True)
        
        with col3:
            st.image("https://imgs.search.brave.com/Pgcb9_lcz5h2RJHmkh0swRhKkdKQsfqRGeYICMzK1qg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvNDgy/NTMwMTE5L3Bob3Rv/L29wZXJhLWJpcmQt/MS5qcGc_cz02MTJ4/NjEyJnc9MCZrPTIw/JmM9Q2E1bi0wOEZO/OW9YZExrM1Vza2lx/ZmpnbXZiXzQ2RHU0/ZlJZQkRGR3UyUT0", 
                    caption="Sample Bird", use_column_width=True)

if __name__ == "__main__":
    main()