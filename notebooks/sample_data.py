import pandas as pd
import os

# --- 配置 ---
# 定义源文件和目标文件的路径
SOURCE_FILE_PATH = os.path.join('data', 'processed', 'field_of_study_processed.csv')
SAMPLE_FILE_PATH = os.path.join('data', 'processed', 'field_of_study_processed_sample.csv')
SAMPLE_SIZE = 1000  # 你可以根据需要调整样本大小，比如 500 或 2000

# --- 主逻辑 ---
def create_sample_dataset():
    """
    读取处理过的数据，创建一个随机样本，并将其保存为新的 CSV 文件。
    """
    print(f"正在从 {SOURCE_FILE_PATH} 读取数据...")
    
    # 检查源文件是否存在
    if not os.path.exists(SOURCE_FILE_PATH):
        print(f"错误：源文件未找到！请确认路径 '{SOURCE_FILE_PATH}' 是否正确。")
        return

    # 读取完整的处理后数据
    df = pd.read_csv(SOURCE_FILE_PATH)
    
    print(f"原始数据集包含 {len(df)} 行。")
    print(f"正在创建 {SAMPLE_SIZE} 行的随机样本...")
    
    # 创建随机样本
    # 使用 random_state 可以确保每次生成的样本都是一样的，方便复现
    sample_df = df.sample(n=SAMPLE_SIZE, random_state=42)
    
    # 保存样本数据到新的 CSV 文件
    # index=False 表示不把 DataFrame 的索引写入到 CSV 文件中
    sample_df.to_csv(SAMPLE_FILE_PATH, index=False)
    
    print(f"成功！样本文件已保存至: {SAMPLE_FILE_PATH}")

if __name__ == "__main__":
    create_sample_dataset()