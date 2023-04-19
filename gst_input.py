import pandas as pd

gst_input = pd.read_excel("Input Reco Raj 2022-23.xlsx", nrows=1000)#, type_backend='pyarrow')

gst_input = gst_input[~gst_input["#"].str.contains("R2A")]

#gst_input = gst_input[gst_input['Match Result'] != "Matching" ]

#gst_input = gst_input[gst_input['Match Result'] != "Almost Matching"]#str.contains("Matching")]

#remove R2A from column #


#keep only select rows from match result column

#column name = Match Result
#"Missing in GSTR-2A"
#"Not Matching"

print(gst_input.head())

gst_input.to_excel("dummy.xlsx")
