import os
import pandas as pd
from groq import Groq

# Initialize the Groq client with your API key
client = Groq(
    api_key="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",
)

# Define the CSV files to process
csv_files = ["real_jobs.csv", "under_review_jobs.csv"]
output_files = []

def process_csv_file(file_path):
    """
    Process a CSV file by sending its content to the Groq API for classification.
    
    Args:
    file_path (str): The path to the CSV file to process.
    
    Returns:
    pd.DataFrame: The classified jobs with added category and legit/fake columns.
    """
    if os.path.exists(file_path):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        
        # Convert the DataFrame to a string to send to the Groq API
        csv_content = df.to_string(index=False)
    else:
        print(f"File not found: {file_path}")
        return None

    # Create a chat completion request to the Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Classify the following jobs as 'Fake' or 'Legit' and assign a category to each:\n\n{csv_content}",
            }
        ],
        model="llama3-8b-8192",
        stream=False,
    )

    # Get the response from the Groq API
    response_content = chat_completion.choices[0].message.content

    # Parse the response (assuming the API returns a formatted table)
    lines = response_content.splitlines()[1:]
    data = [line.split(",") for line in lines]
    classified_jobs = pd.DataFrame(data)

    return classified_jobs

for csv_file in csv_files:
    classified_jobs = process_csv_file(csv_file)
    if classified_jobs is not None:
        # Save the classified jobs to a new CSV file
        output_file = f"classified_{os.path.splitext(csv_file)[0]}.txt"
        classified_jobs.to_csv(output_file, index=False, header=False)
        output_files.append(output_file)

if output_files:
    print(f"Classified files saved: {', '.join(output_files)}")
    for file in output_files:
        print(f"Opening {file}...")
        import webbrowser
        webbrowser.open('file://' + os.path.realpath(file))
else:
    print("No files processed.")