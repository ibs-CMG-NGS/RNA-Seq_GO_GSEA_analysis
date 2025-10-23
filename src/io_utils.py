import pandas as pd

def read_excel_sheets(filepath, sheet_names):
    return {sheet: pd.read_excel(filepath, sheet_name=sheet) for sheet in sheet_names}

def save_dataframe(df, path):
    df.to_csv(path, index=False)
