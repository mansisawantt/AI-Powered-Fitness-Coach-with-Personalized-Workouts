from langchain_openai import ChatOpenAI  # Use ChatOpenAI instead of OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from logger import log_message
import os

# Load environment variables
load_dotenv()

# Fetch API Key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    log_message(" OpenAI API Key missing!", "error")
    raise ValueError("OpenAI API Key not found. Please add it to .env")

# Initialize OpenAI Chat Model
try:
    llm = ChatOpenAI(model="gpt-4o", 
                        temperature=0.7, 
                        openai_api_key=OPENAI_API_KEY)

except Exception as e:
    log_message(f" OpenAI Initialization Error: {str(e)}", "error")
    raise e


# Define a workout plan prompt template
workout_prompt = PromptTemplate(
    input_variables=["fitness_level", "goal", "duration", "equipment"],
    template=(
        "Create a personalized workout plan for a {fitness_level} individual "
        "whose goal is {goal}. The workout should last {duration} minutes "
        "and use {equipment} equipment. Provide step-by-step exercises."
    ),
)

# Function to generate a workout plan
def generate_workout(fitness_level, goal, duration, equipment):
    prompt = workout_prompt.format(
        fitness_level=fitness_level,
        goal=goal,
        duration=duration,
        equipment=equipment,
    )

    try:
        response = llm.invoke(prompt)  # Use ChatOpenAI's invoke method
        log_message("Workout plan generated successfully!")
        return response.content  # Extract content
    except Exception as e:
        log_message(f" Error generating workout: {str(e)}", "error")
        return f"An error occurred: {str(e)}"


# Test the function
if __name__ == "__main__":
    test_workout = generate_workout("Beginner", "Weight Loss", "24", "Bodyweight")
    print("\nGenerated Workout Plan:\n", test_workout)