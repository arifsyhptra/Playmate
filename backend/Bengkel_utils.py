import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "WO.xlsx")

def get_wo_head():
    print(">>> mulai baca excel:", DATA_PATH)

    df = pd.read_excel(DATA_PATH, sheet_name="WO", engine="openpyxl")

    print(">>> excel terbaca")

    return df.head(5).to_dict(orient="records")