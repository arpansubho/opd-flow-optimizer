import pandas as pd

file_path = "e:/TERM 6/MlOps/A1/opd_flow_optimizer_synthetic_fixed.xlsx"
df = pd.read_excel(file_path)

print("Columns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nData Types:")
print(df.dtypes)
print("\nMissing Values:")
print(df.isnull().sum())
