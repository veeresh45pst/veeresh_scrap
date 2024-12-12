import pandas as pd

def filter_fake_jobs(df):
    """
    Filters out fake job postings from the given DataFrame.

    Args:
        df (pd.DataFrame): DataFrame of job postings.

    Returns:
        valid_jobs (pd.DataFrame): DataFrame of valid job postings.
        fake_jobs (pd.DataFrame): DataFrame of fake job postings.
    """
    fake_keywords = ["cash payment"]
    fake_jobs = df[df["description"].str.contains('|'.join(fake_keywords), case=False, na=False)]
    valid_jobs = df[~df["description"].str.contains('|'.join(fake_keywords), case=False, na=False)]
    return valid_jobs, fake_jobs