import psycopg2
import pandas as pd

from sqlalchemy import create_engine
gst_input = pd.read_excel("Input Reco Raj 2022-23.xlsx")#, nrows=500) #, type_backend='pyarrow')

gst_input = gst_input.loc[:, ~gst_input.columns.str.contains('^Unnamed')]
gst_input.columns = gst_input.columns.str.replace(' ', '_').str.lower().str.replace('%', 'percent')
column_headers = list(gst_input.columns)

gst_input['office_code'] = gst_input['keywords'].str[3:9]
gst_input['regional_code'] = gst_input['keywords'].str[3:5]
gst_input['status'] = "To be updated"
#print(column_headers)

# remove united india entries
gst_input = gst_input[~gst_input["supplier_gstin"].str.contains("AAACU5552C")]
gst_input = gst_input[~gst_input["#"].str.contains("R2A")]
gst_input.rename(columns={'#':'purchaser'}, inplace=True)

gst_input.columns = [c.lower() for c in gst_input.columns]
engine = create_engine("postgresql://barneedhar:barneedhar@localhost:5432/flask_db")
gst_input.to_sql("entries", engine, if_exists = "append", index=False)#, index_label='id')


