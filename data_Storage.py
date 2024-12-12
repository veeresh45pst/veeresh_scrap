import pandas as pd

def save_to_csv(jobs_data, filename="jobs.csv"):
    df = pd.DataFrame(jobs_data)
    df.to_csv(filename, index=False)
    return filename

def load_data(filename="jobs.csv"):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame()