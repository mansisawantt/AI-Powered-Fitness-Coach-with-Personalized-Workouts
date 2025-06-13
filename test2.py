from langchain.prompts import PromptTemplate

# Define a template with placeholders
prompt = PromptTemplate(
    input_variables=["name", "age"],
    template="Hello, my name is {name} and I am {age} years old."
)

# Format the prompt with actual values
formatted_prompt = prompt.format(name="Manasi", age=24)

print(formatted_prompt)
