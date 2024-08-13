
import pandas as pd
import re

# Load the Excel file
excel_file_path = '/mnt/data/字幕時間表.xlsx'
sheets = pd.read_excel(excel_file_path, sheet_name=None)

# Load all three VTT files
vtt_files = {
    '第一集': '/mnt/data/[你好，我是誰] - 第01集｜經典再現 - Still Me_zh-TW.vtt',
    '第二集': '/mnt/data/[你好，我是誰] - 第02集｜經典再現 - Still Me_zh-TW.vtt',
    '第三集': '/mnt/data/[你好，我是誰] - 第03集 ｜經典再現- Still Me_zh-TW.vtt',
}

# Function to extract time intervals and subtitles from VTT file
def extract_vtt_data(vtt_file_path):
    with open(vtt_file_path, 'r', encoding='utf-8') as file:
        vtt_content = file.read()
    
    vtt_pattern = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3})\n(.*?)\n", re.DOTALL)
    vtt_matches = vtt_pattern.findall(vtt_content)
    
    vtt_df = pd.DataFrame(vtt_matches, columns=['Time', 'Subtitle'])
    vtt_df['Subtitle'] = vtt_df['Subtitle'].apply(lambda x: x.replace('\n', ' ').strip())
    
    return vtt_df

# Process each episode
for episode, vtt_file in vtt_files.items():
    df_episode = sheets[episode]
    vtt_df = extract_vtt_data(vtt_file)
    
    # Match subtitles between Excel and VTT and add the time intervals
    df_episode['時間'] = df_episode['字幕'].apply(lambda x: vtt_df[vtt_df['Subtitle'] == x]['Time'].iloc[0] if not vtt_df[vtt_df['Subtitle'] == x].empty else None)
    
    # Update the sheets dictionary with the modified DataFrame
    sheets[episode] = df_episode

# Save the updated Excel file
updated_excel_path = '/mnt/data/字幕時間表_更新_完整.xlsx'
with pd.ExcelWriter(updated_excel_path, engine='xlsxwriter') as writer:
    for sheet_name, df in sheets.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)
