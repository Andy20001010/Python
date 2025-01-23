import pandas as pd
from tkinter import filedialog
import tkinter as tk

# Function 1: Host and Risk type analysis, with proper 'None' handling
def analyze_risk_by_host(df, writer):
    risk_types = ['Critical', 'High', 'Medium', 'Low', 'None']
    host_risk_counts = {col: [] for col in ['Host'] + risk_types}

    df_unique_by_host_and_plugin = df.drop_duplicates(subset=['Host', 'Plugin ID'])
    grouped = df_unique_by_host_and_plugin.groupby('Host')

    for host, group in grouped:
        host_risk_counts['Host'].append(host)
        total_count = len(group)
        other_risks_count = 0
        for risk in risk_types[:-1]:
            count = (group['Risk'] == risk).sum()
            host_risk_counts[risk].append(count)
            other_risks_count += count
        
        none_count = total_count - other_risks_count
        host_risk_counts['None'].append(none_count)

    result_df_analysis = pd.DataFrame(host_risk_counts)
    result_df_analysis.to_excel(writer, sheet_name='風險數量列表', index=False)

# Function 2: Filter Risk >= Low, with proper sorting
def filter_risk_above_low(df, writer, separate_file_path=None):
    risk_levels = ['Low', 'Medium', 'High', 'Critical']
    df_unique_by_host_and_plugin = df.drop_duplicates(subset=['Host', 'Plugin ID'])
    filtered_df = df_unique_by_host_and_plugin[df_unique_by_host_and_plugin['Risk'].isin(risk_levels)]
    result_df_filter = filtered_df[['Plugin ID', 'Risk', 'Host', 'Name']]
    result_df_filter['Risk'] = pd.Categorical(result_df_filter['Risk'], categories=risk_levels, ordered=True)
    result_df_filter = result_df_filter.sort_values('Risk', ascending=False)

    # 寫入主 Excel
    result_df_filter.to_excel(writer, sheet_name='弱點列表', index=False)

    # 如果需要單獨輸出該結果的 Excel
    if separate_file_path:
        with pd.ExcelWriter(separate_file_path, engine='xlsxwriter') as separate_writer:
            result_df_filter.to_excel(separate_writer, sheet_name='弱點列表', index=False)

# Function 3: Extract Risk >= Low data, remove duplicate ids, and format vertically with spacing
def extract_vertical_risk_data_with_spacing(df, writer):
    risk_levels = ['Low', 'Medium', 'High', 'Critical']
    # 去除重複的 Plugin ID
    df_unique = df.drop_duplicates(subset=['Plugin ID'])
    # 篩選 Risk 欄位符合風險等級的資料
    filtered_df = df_unique[df_unique['Risk'].isin(risk_levels)]
    # 設定風險等級的順序
    filtered_df['Risk'] = pd.Categorical(filtered_df['Risk'], categories=risk_levels, ordered=True)
    # 根據風險等級排序，從高到低
    filtered_df = filtered_df.sort_values('Risk', ascending=False)
    
    # 準備所需欄位
    columns = ['Risk', 'Name', 'CVE', 'Plugin ID', 'Description', 'Solution', 'See Also']
    result = []

    # 組織數據為直式格式，並在每個弱點之間加入空白行
    for _, row in filtered_df.iterrows():
        for col in columns:
            result.append([col, row[col]])  # 每個欄位作為直式顯示
        result.append(['', ''])  # 插入空白行

    # 轉換為 DataFrame
    result_df_vertical = pd.DataFrame(result, columns=['Field', 'Value'])

    # 將結果寫入 Excel
    result_df_vertical.to_excel(writer, sheet_name='弱點說明表格', index=False, header=False)

# Function 4: Count occurrences of each risk level from previous data, remove duplicate IDs
def count_risk_levels(df, writer):
    risk_levels = ['Critical', 'High', 'Medium', 'Low']
    df_unique = df.drop_duplicates(subset=['Plugin ID'])
    risk_counts = df_unique['Risk'].value_counts().reindex(risk_levels).fillna(0).astype(int)
    result_df_counts = pd.DataFrame({'Var1': risk_levels, 'Freq': risk_counts.values})
    result_df_counts.to_excel(writer, sheet_name='弱點數量', index=False)

# Main function to handle Excel writing and call the functions
def run_analysis_and_filter():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        save_path = "合併結果.xlsx"
        separate_risk_file_path = "弱點列表.xlsx"

        with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
            analyze_risk_by_host(df, writer)
            filter_risk_above_low(df, writer, separate_file_path=separate_risk_file_path)
            extract_vertical_risk_data_with_spacing(df, writer)
            count_risk_levels(df, writer)
        
        print(f"Results saved to {save_path}")
        print(f"Filtered risk list saved to {separate_risk_file_path}")
    else:
        print("File selection canceled.")
    
    # Close the Tkinter window after processing
    root.destroy()

# Initialize the Tkinter window
root = tk.Tk()
root.title("CSV Analyzer and Filter")

# Create a button to start the process
open_button = tk.Button(root, text="選擇檔案", command=run_analysis_and_filter)
open_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
