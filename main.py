import os
import streamlit as st
from langchain_openai import ChatOpenAI  # Correct import
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime

# Load environment variables
load_dotenv()

# Fetch API Key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI API Key missing! Please add it to the .env file.")
    st.stop()

# Initialize OpenAI Chat Model
try:
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",  # Ensure this model is available; otherwise, use "gpt-3.5-turbo"
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY
    )
except Exception as e:
    st.error(f"❌ OpenAI Initialization Error: {str(e)}")
    st.stop()

# Define workout plan prompt template
workout_prompt = PromptTemplate(
    input_variables=["fitness_level", "goal", "duration", "equipment"],
    template=(
        "Create a personalized workout plan for a {fitness_level} individual "
        "whose goal is {goal}. The workout should last {duration} minutes "
        "and use {equipment} equipment. Provide step-by-step exercises with "
        "sets, reps, and rest intervals."
    ),
)

# Function to generate workout plan
def generate_workout(fitness_level, goal, duration, equipment):
    prompt = workout_prompt.format(
        fitness_level=fitness_level,
        goal=goal,
        duration=duration,
        equipment=equipment,
    )
    try:
        response = llm.invoke(prompt)
        return response.content  # Extract content from the response
    except Exception as e:
        st.error(f"❌ Error generating workout: {str(e)}")
        return f"An error occurred: {str(e)}"

# Function to create a PDF
def create_pdf(workout_plan, fitness_level, goal, duration, equipment):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Personalized Workout Plan", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Fitness Level: {fitness_level}", ln=True)
    pdf.cell(200, 10, txt=f"Goal: {goal}", ln=True)
    pdf.cell(200, 10, txt=f"Duration: {duration} minutes", ln=True)
    pdf.cell(200, 10, txt=f"Equipment: {equipment}", ln=True)
    pdf.ln(10)
    
    pdf.multi_cell(0, 10, workout_plan)
    
    filename = f"Workout_Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# Streamlit App
def main():
    # Custom CSS for styling
    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }
        .stSelectbox, .stNumberInput {
            background-color: white;
            border-radius: 5px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🏋️‍♀️ Personalized Workout Planner")
    st.markdown("Generate a custom workout plan tailored to your needs!")

    # Sidebar for inputs
    with st.sidebar:
        st.header("Workout Preferences")
        fitness_level = st.selectbox(
            "Fitness Level",
            ["Beginner", "Intermediate", "Advanced"]
        )
        goal = st.selectbox(
            "Fitness Goal",
            ["Weight Loss", "Muscle Gain", "Endurance", "General Fitness"]
        )
        duration = st.number_input(
            "Duration (minutes)",
            min_value=10,
            max_value=120,
            value=30,
            step=5
        )
        equipment = st.selectbox(
            "Equipment Available",
            ["Bodyweight", "Dumbbells", "Gym Equipment", "Resistance Bands"]
        )
        
        generate_button = st.button("Generate Workout Plan")

    # Main content area
    if "workout_history" not in st.session_state:
        st.session_state.workout_history = []

    if generate_button:
        with st.spinner("Generating your workout plan..."):
            workout_plan = generate_workout(fitness_level, goal, duration, equipment)
            st.session_state.workout_history.append({
                "plan": workout_plan,
                "fitness_level": fitness_level,
                "goal": goal,
                "duration": duration,
                "equipment": equipment,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.success("✅ Workout plan generated successfully!")

        # Display workout plan
        st.subheader("Your Workout Plan")
        st.markdown(workout_plan)

        # Download as PDF
        pdf_file = create_pdf(workout_plan, fitness_level, goal, duration, equipment)
        with open(pdf_file, "rb") as file:
            st.download_button(
                label="Download as PDF",
                data=file,
                file_name=pdf_file,
                mime="application/pdf"
            )

    # Workout History Section
    if st.session_state.workout_history:
        st.subheader("Workout History")
        for i, entry in enumerate(st.session_state.workout_history):
            with st.expander(f"Workout {i+1} - {entry['date']}"):
                st.write(f"**Fitness Level:** {entry['fitness_level']}")
                st.write(f"**Goal:** {entry['goal']}")
                st.write(f"**Duration:** {entry['duration']} minutes")
                st.write(f"**Equipment:** {entry['equipment']}")
                st.markdown(entry['plan'])

if __name__ == "__main__":
    main()