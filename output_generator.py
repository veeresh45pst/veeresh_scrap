import pandas as pd

def generate_output(jobs_data):
    # You can format the data as per your needs
    df = pd.DataFrame(jobs_data)
    return df  # Or you can return the data in another format (e.g., JSON, database entry)