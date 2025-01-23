import pandas as pd
from tkinter import filedialog, Tk, Label, Button
import os

def select_file(prompt):
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        raise ValueError("No file selected.")
    return file_path

def compare_files(initial_file, retest_file, output_file):
    # Load the Excel files
    initial_df = pd.read_excel(initial_file, usecols=['Plugin ID', 'Risk', 'Host', 'Name'])
    retest_df = pd.read_excel(retest_file, usecols=['Plugin ID', 'Risk', 'Host', 'Name'])

    # Merge the dataframes to find common and different items
    merged_df = pd.merge(
        initial_df,
        retest_df,
        on=['Plugin ID', 'Host', 'Name'],
        how='outer',
        suffixes=('_Initial', '_Retest'),
        indicator=True
    )

    # Determine old risks and risk level changes
    merged_df['是否為舊有風險'] = merged_df['_merge'].apply(lambda x: '是' if x == 'both' else '否')
    merged_df['等級是否改變'] = merged_df.apply(
        lambda row: '是' if row['Risk_Initial'] != row['Risk_Retest'] else '否' 
        if pd.notna(row['Risk_Initial']) and pd.notna(row['Risk_Retest']) else 'N/A',
        axis=1
    )

    # Select desired columns for output
    result_df = merged_df[
        ['Plugin ID', 'Risk_Retest', 'Host', 'Name', '是否為舊有風險', '等級是否改變']
    ]
    result_df.rename(columns={
        'Risk_Retest': 'Risk (Retest)'
    }, inplace=True)

    # Save to Excel
    result_df.to_excel(output_file, index=False, sheet_name='比較結果')
    print(f"Comparison result saved to {output_file}")

def main():
    # Initialize Tkinter root
    root = Tk()
    root.title("選擇檔案")
    root.geometry("400x200")

    initial_file_var = [None]
    retest_file_var = [None]

    def select_initial_file():
        try:
            initial_file_var[0] = select_file("請選擇初測的 Excel 檔案：")
            initial_label.config(text=f"初測檔案已選擇: {os.path.basename(initial_file_var[0])}")
        except ValueError as e:
            initial_label.config(text="未選擇初測檔案")

    def select_retest_file():
        try:
            retest_file_var[0] = select_file("請選擇複測的 Excel 檔案：")
            retest_label.config(text=f"複測檔案已選擇: {os.path.basename(retest_file_var[0])}")
        except ValueError as e:
            retest_label.config(text="未選擇複測檔案")

    def run_comparison():
        if not initial_file_var[0] or not retest_file_var[0]:
            result_label.config(text="請選擇初測和複測檔案！", fg="red")
            return

        output_file = os.path.join(os.getcwd(), "復測報告.xlsx")
        compare_files(initial_file_var[0], retest_file_var[0], output_file)
        result_label.config(text=f"比較完成，檔案已儲存至: {output_file}", fg="green")
        root.destroy()

    # UI Components
    initial_button = Button(root, text="選擇初測檔案", command=select_initial_file)
    initial_button.pack(pady=10)
    initial_label = Label(root, text="未選擇初測檔案")
    initial_label.pack()

    retest_button = Button(root, text="選擇複測檔案", command=select_retest_file)
    retest_button.pack(pady=10)
    retest_label = Label(root, text="未選擇複測檔案")
    retest_label.pack()

    compare_button = Button(root, text="開始比較", command=run_comparison, bg="lightblue")
    compare_button.pack(pady=20)

    result_label = Label(root, text="")
    result_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
