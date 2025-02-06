import pandas as pd


def clean_data(df):
    """
    Clean and preprocess the DataFrame:
    - Handle missing values.
    - Transform 'created_utc' to a readable datetime.
    - Apply any relevant transformations before saving to CSV.
    """

    # Replace NaN values with 'N/A'
    df = df.fillna('N/A')

    # Convert 'created_utc' to readable datetime
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')

    # Format 'created_utc' to SQL-compatible format (YYYY-MM-DD HH:MM:SS)
    df['created_utc'] = df['created_utc'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Convert 'score' and 'num_comments' to integer if they're not already
    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].astype(int)

    return df
