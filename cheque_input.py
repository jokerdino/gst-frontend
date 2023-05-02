import pandas as pd
from sqlalchemy import create_engine


def upload_cheque_entries(file):
    df_cheque = pd.read_excel(file)
    engine = create_engine("postgresql://barneedhar:barneedhar@localhost:5432/flask_db")
    df_cheque.to_sql("cheques", engine, if_exists = "append", index=False)

#upload_cheque_entries(df_cheque)
