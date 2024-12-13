import pandas as pd

# Read the Excel file
dr = pd.read_excel('news_catalog_unique_sample.xlsx')
# Create a dictionary to store the data
data_dict = {}
data_list = []

# Iterate through each row in the DataFrame
for index, row in dr.iterrows():
    # Convert row to dictionary and store in data_dict
    # Using index as key to maintain unique entries
    data = row.to_dict()
    if data['Link'] in data_dict:
        print(f"Duplicate : {data['Link']}")
    else:
        data_dict[data['Link']] = data
        data_list.append(data)

# for data_info in data_list:
#     print(data_info)
#     if 'df' not in locals():
#         df = pd.DataFrame([data_info])
#     else:
#         # Append the new session_info to existing DataFrame
#         df = pd.concat([df, pd.DataFrame([data_info])], ignore_index=True)
# output_file = 'news_catalog_unique.xlsx'
# df.to_excel(output_file, index=False)
