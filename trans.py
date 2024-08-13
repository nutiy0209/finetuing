import pandas as pd
import json

# Function to convert a row into JSONL format based on the required format
def row_to_jsonl(row):
    data = {"messages": [{"role": "system", "content": row["system"].replace("\n", "")}]}
    for i in range(4):
        assistant_key = f"asistance(對話){'' if i == 0 else f'.{i}'}"
        user_key = f"user(對話){'' if i == 0 else f'.{i}'}"
        if pd.notna(row.get(assistant_key)):
            data["messages"].append({"role": "assistant", "content": row[assistant_key].replace("\n", "")})
        if pd.notna(row.get(user_key)):
            data["messages"].append({"role": "user", "content": row[user_key].replace("\n", "")})
    return data

# Load the Excel file
excel_path = "ft_value.xlsx"
df = pd.read_excel(excel_path, sheet_name='聊天')  # Specify the correct sheet name

# Convert all rows in the '聊天' sheet to JSONL format
chat_jsonl_data = df.apply(row_to_jsonl, axis=1)

# Convert to a list of dictionaries and save the JSONL format data
chat_jsonl_list = chat_jsonl_data.tolist()
jsonl_path = "test1.jsonl"

with open(jsonl_path, 'w', encoding='utf-8') as f:
    for entry in chat_jsonl_list:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

print(f"JSONL file saved at: {jsonl_path}")
