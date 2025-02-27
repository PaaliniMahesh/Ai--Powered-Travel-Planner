import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Set page config
st.set_page_config(page_title="AI Powered Travel Planner", layout="centered", page_icon="✈️")

st.title("🌍 AI Powered Travel Planner ✈️")
st.write("Enter details to get estimated travel costs for various travel modes.")

# User Inputs
source = st.text_input("📍 Source:")
destination = st.text_input("🎯 Destination:")

# Optional: Basic gradient background
st.markdown(
    """
    <style>
        .st-emotion-cache-1y4p8pa {
            background: linear-gradient(to right, #4facfe, #00f2fe);
            padding: 15px;
            border-radius: 10px;
            color: white;
            text-align: center;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("Get Travel Plan"):
    if source and destination:
        with st.spinner("Fetching all travel options..."):
            # Define enhanced prompt template
            chat_template = ChatPromptTemplate.from_messages([
                ("system", """
                You are an AI travel assistant designed to provide detailed travel options between two cities in India.
                For the given source and destination, your response should be structured into:

                1. **Train Options (2 best trains)**:
                    - Train Name
                    - Departure Time
                    - Arrival Time
                    - Duration
                    - Fare (INR)

                2. **Bus Options (2 best buses)**:
                    - Bus Type (AC Sleeper, Non-AC Sleeper, etc.)
                    - Departure Time
                    - Arrival Time
                    - Duration
                    - Fare (INR)

                3. **Flight Options (2 best flights if available)**:
                    - Flight Name (Airline)
                    - Departure Time
                    - Arrival Time
                    - Duration
                    - Fare (INR)
                
                4. **If there is no direct flight, provide:**
                    - Nearest Airport to Source
                    - Nearest Airport to Destination
                    - Suggested mode (train, bus, or cab) to cover the remaining distance
                    - Estimated cost and time for these modes.

                5. **Recommendation**:
                    - Based on cost, duration, and convenience, recommend the best travel mode.
                    - Also, suggest the best time to travel (morning, afternoon, night) for this route.

                Provide all details in **structured and user-friendly format**.
                """),
                ("human", "Plan my travel from {source} to {destination}.")
            ])

            # Initialize the Google GenAI chat model
            chat_model = ChatGoogleGenerativeAI(api_key="your api key", model="gemini-1.5-pro")

            # Define parser to parse output as plain text
            parser = StrOutputParser()

            # Create the chain (Prompt -> Model -> Output Parser)
            chain = chat_template | chat_model | parser

            # Prepare input and invoke chain
            raw_input = {"source": source, "destination": destination}
            response = chain.invoke(raw_input)

            # Display result
            st.success("Possible Travel Routes and Budget Breakdown", icon="🔍")

            # Render each sectionA
            travel_lines = response.split("\n")
            for line in travel_lines:
                if line.strip():
                    st.markdown(f"✅ {line}")

    else:
        st.error("⚠️ Please enter both source and destination to continue.")
