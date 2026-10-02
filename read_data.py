import pandas as pd

file_path = "data/كتالوج_بيع_البرفانات_والمسكات.xlsx"

excel_file = pd.ExcelFile(file_path)
print("sheets:", excel_file.sheet_names)
print("-" * 50)

for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print(f"\nsheet: {sheet_name}")
    print(f"number of rows: {len(df)}")
    print(f"columns: {list(df.columns)}")
    print(df.head(3))
    print("-" * 50)