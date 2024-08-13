import librosa
import numpy as np
from scipy.spatial.distance import euclidean

# 加载音频文件
def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    return y, sr

# 提取MFCC特征
def extract_mfcc(y, sr):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return mfcc

# 计算特征之间的欧式距离
def compare_mfcc(mfcc1, mfcc2):
    distances = np.linalg.norm(mfcc1 - mfcc2, axis=0)
    return np.mean(distances)

# 滑动窗口匹配
def find_match(y_full, sr_full, y_query, sr_query, hop_length=512):
    mfcc_full = extract_mfcc(y_full, sr_full)
    mfcc_query = extract_mfcc(y_query, sr_query)
    
    min_distance = float('inf')
    best_start = 0
    
    # 滑动窗口遍历
    for i in range(0, mfcc_full.shape[1] - mfcc_query.shape[1], hop_length):
        window = mfcc_full[:, i:i + mfcc_query.shape[1]]
        distance = compare_mfcc(window, mfcc_query)
        
        if distance < min_distance:
            min_distance = distance
            best_start = i
    
    best_time = librosa.frames_to_time(best_start, sr=sr_full, hop_length=hop_length)
    return best_time, min_distance

# 示例使用
# 使用相对路径指向子文件夹中的音频文件
y_full, sr_full = load_audio('audio/episode_1.mp3')  # 指定相对路径
y_query, sr_query = load_audio('audio/cut1.mp3')  # 指定相对路径

# 使用绝对路径（如果文件在不同目录下或在其他地方）
# y_full, sr_full = load_audio('/path/to/your_project_directory/audio_files/full_audio.mp3')
# y_query, sr_query = load_audio('/path/to/your_project_directory/audio_files/query_audio.mp3')

best_time, min_distance = find_match(y_full, sr_full, y_query, sr_query)

print(f'Best match starts at: {best_time} seconds with a distance of {min_distance}')
