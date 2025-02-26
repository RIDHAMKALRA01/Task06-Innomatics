import streamlit as st
import google.generativeai as genai
from langchain.prompts import PromptTemplate

API_KEY = "AIzaSyCk5E_4Honj7ZXWyoUJ8z_SMcYzK4lNSo8"

# Validate API Key
if not API_KEY:
    st.error("API Key is missing!")
    st.stop()

# Configure Google GenAI
genai.configure(api_key=API_KEY)

# Define LangChain prompt template
travel_prompt = PromptTemplate(
    input_variables=["source", "destination"],
    template="""
    Provide detailed travel options from {source} to {destination} including:
    1. Cab: Estimated cost and duration
    2. Train: Estimated cost and duration
    3. Bus: Estimated cost and duration
    4. Flight: Estimated cost and duration
    Format the response in markdown with clear sections for each travel mode.
    """
)

def find_travel_options(source, destination):
    # Use native Google GenAI
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    prompt = travel_prompt.format(
        source=source,
        destination=destination
    )

    try:
        response = model.generate_content(prompt)
        travel_info = response.text if hasattr(response, "text") else "No response generated."
        return travel_info
    except Exception as e:
        return f"Error generating response: {str(e)}"

def main():
    st.title("AI-Powered Travel Planner")
    
    st.markdown("Enter Your Travel Details Below:")
    
    # Input fields
    source = st.text_input("Enter Source Location")
    destination = st.text_input("Enter Destination Location")

    # Find Travel Options button
    if st.button("Find Travel Options"):
        if not source or not destination:
            st.warning("Please enter both source and destination locations!")
            return

        with st.spinner("Fetching travel recommendations... Please wait!"):
            travel_options = find_travel_options(source, destination)
            st.subheader("Travel Recommendations:")
            st.markdown(travel_options)

if __name__ == "__main__":
    main()