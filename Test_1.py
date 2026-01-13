import pandas as pd

def analyze_excel(file_path):
    df = pd.read_excel(file_path)
    df['minimum_nights'] = df['minimum_nights'].abs()
    df['price'] = (df['price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).
                   str.strip().astype(float))
    df['service_fee'] = (df['service_fee'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).
                           str.strip().astype(float))
    rows, cols = df.shape
    format_info = df.dtypes
    missing_counts = df.isnull().sum()
    print("Количество пропусков по столбцам:\n", missing_counts)

    # count_over_365 = (df['minimum_nights'] > 365).sum()
    # print(f"Количество значений в 'minimum_nights' более 365: {count_over_365}")
    mask = df['minimum_nights'] > 365
    count = mask.sum()
    print(f"Количество значений > 365: {count}")

    # Получаем имя первого столбца
    first_col_name = df.columns[0]
    # Фильтрация по условию > 365
    filtered_df = df[df['minimum_nights'] > 365]
   # Выводим пары: значение из первого столбца - значение из minimum_nights
    for val1, val_min in zip(filtered_df[first_col_name], filtered_df['minimum_nights']):
        print(f"{val1} - {val_min}")

    cols_to_analyze = ['minimum_nights', 'price', 'service_fee']
    for col in cols_to_analyze:
        print(f"{col}:")
        print(f"  мин - {df[col].min()}")
        print(f"  макс - {df[col].max()}")
        print(f"  среднее - {df[col].mean()}\n")

    return rows, cols, format_info
# print(f"Количество строк: {rows}")
# print(f"Количество столбцов: {cols}")
# print(f"Формат каждого столбца:\n{format_info}")

rows, cols, formats = analyze_excel('airbnb_open_data.xlsx')
print(f"Количество строк: {rows}")
print(f"Количество столбцов: {cols}")
print(f"Формат каждого столбца:\n{formats}")
