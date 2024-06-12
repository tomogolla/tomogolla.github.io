import os
import time
import anthropic

# Set the custom working directory to the root of the project
project_directory = 'C:/Users/Administrator/Desktop/personal project/project_folder'  # Change this to the path of your project folder
os.chdir(project_directory)

# Define the input and output folders
input_folder = 'input'
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

# Define the file paths for input and output
source_file_path = os.path.join(input_folder, 'Source_File_2.txt')
new_script_structure_path = os.path.join(input_folder, 'Zurafit.txt')

# Print the file paths to confirm they are correct
print("Source File Path:", source_file_path)
print("New Script Structure Path:", new_script_structure_path)

# Initialize the Anthropic client with the API key from environment variable
api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("API key is not set. Please set the ANTHROPIC_API_KEY environment variable.")

client = anthropic.Client(
    api_key=api_key,
)

def call_claude_api(prompt, max_tokens=1500):
    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # Access the content of the response
        if response and response.content:
            return response.content[0].text
        else:
            print("No valid content found in the response.")
            return None
    except anthropic.AuthenticationError as e:
        print(f"Authentication error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def analyze_script(script):
    prompt = f"Analyze this please: {script}"
    return call_claude_api(prompt)

def get_answers_from_analysis(script_analysis):
    if script_analysis is None:
        return None
    prompt = (
        f"Based on the analysis: {script_analysis}\n"
        "Please answer the following questions:\n"
        "1. What are the pain points?\n"
        "2. What is their core problem?\n"
        "3. What are the symptoms?\n"
        "4. What do they feel emotionally about the problem?\n"
        "5. Give me a situation of how they experience their problem & how people react to them."
    )
    return call_claude_api(prompt)

def get_unique_mechanism(script_analysis):
    if script_analysis is None:
        return None
    prompt = (
        f"Based on the analysis: {script_analysis}\n"
        "Please answer the following:\n"
        "What is the unique mechanism problem and what is the unique mechanism solution?"
    )
    return call_claude_api(prompt)

def transform_script(script_analysis, new_script_structure):
    if script_analysis is None:
        return None
    prompt = (
        f"I'm going to give you a complete different script, its about pain, but the reason why I'm giving you this is because the structure of this script is amazing. I want to follow the structure line by line but I want to change the words to meet for neuropathy based on the analysis: {script_analysis}. Please take that information and paste it into this new script whilst following the new script's structure:\n\n"
        f"{new_script_structure}"
    )
    return call_claude_api(prompt, max_tokens=3000)

def process_file(source_file_path, new_script_structure_path, zurafit_file_path, output_folder):
    with open(source_file_path, 'r', encoding='utf-8') as file:
        source_script = file.read()

    with open(new_script_structure_path, 'r', encoding='utf-8') as file:
        new_script_structure = file.read()

    with open(zurafit_file_path, 'r', encoding='utf-8') as file:
        zurafit_script = file.read()

    script_analysis = analyze_script(source_script)
    if script_analysis is None:
        print("Failed to analyze script. Exiting.")
        return

    time.sleep(1)  # Ensure there is a delay between requests
    questions_answers = get_answers_from_analysis(script_analysis)
    if questions_answers is None:
        print("Failed to get answers from analysis. Exiting.")
        return

    time.sleep(1)
    unique_mechanism_answers = get_unique_mechanism(script_analysis)
    if unique_mechanism_answers is None:
        print("Failed to get unique mechanism answers. Exiting.")
        return

    time.sleep(1)
    transformed_script = transform_script(script_analysis, zurafit_script)
    if transformed_script is None:
        print("Failed to transform script. Exiting.")
        return

    if script_analysis:
        with open(os.path.join(output_folder, 'script_analysis.txt'), 'w', encoding='utf-8') as file:
            file.write(script_analysis)
    if questions_answers:
        with open(os.path.join(output_folder, 'questions_answers.txt'), 'w', encoding='utf-8') as file:
            file.write(questions_answers)
    if unique_mechanism_answers:
        with open(os.path.join(output_folder, 'unique_mechanism_answers.txt'), 'w', encoding='utf-8') as file:
            file.write(unique_mechanism_answers)
    if transformed_script:
        with open(os.path.join(output_folder, 'transformed_script.txt'), 'w', encoding='utf-8') as file:
            file.write(transformed_script)

    print('Processing complete. Check the output folder for results.')

if __name__ == "__main__":
    # Call the process_file function
    process_file(source_file_path, new_script_structure_path, new_script_structure_path, output_folder)
