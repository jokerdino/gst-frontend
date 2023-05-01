import pandas as pd
from sqlalchemy import create_engine
df_cheque = pd.read_excel("idfc working.xlsx")


def upload_cheque_entries(input_df):
    engine = create_engine("postgresql://barneedhar:barneedhar@localhost:5432/flask_db")
    input_df.to_sql("cheques", engine, if_exists = "append", index=False)

#upload_cheque_entries(df_cheque)
