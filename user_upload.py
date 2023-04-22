import pandas as pd
from sqlalchemy import create_engine

user_upload = pd.read_csv("user.csv")


engine = create_engine("postgresql://barneedhar:barneedhar@localhost:5432/flask_db")
user_upload.to_sql("user", engine, if_exists = "append", index=False)#, index_label='id')
#gst_input = gst_input[gst_input['Match Result'] != "Matching" ]
