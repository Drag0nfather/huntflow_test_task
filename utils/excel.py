from pandas import read_excel

from utils.exceptions import ExcelFileNotFoundException


def convert_excel_to_list(filename: str) -> list:
    """
    Экспорт Excel файла в список словарей
    """
    try:
        df = read_excel(f'{filename}').to_dict(orient='records')
        return df
    except Exception:
        raise ExcelFileNotFoundException


def check_upload_field(filename: str) -> bool:
    """
    Проверка, существует ли поле upload в Excel файле
    """
    try:
        df = read_excel(f'{filename}')
        if 'upload' in df.columns:
            return True
        df.insert(5, 'upload', 0)
        df.to_excel(f'{filename}', index=False)
        return True
    except Exception:
        raise ExcelFileNotFoundException


def add_success_point_to_applicant(filename: str, applicant: str) -> bool:
    """
    Добавление в колонку upload статуса обработки кандидата
    """
    df = read_excel(f'{filename}')
    applicant_index = df.index[df['ФИО'] == applicant][0]
    df.at[applicant_index, 'upload'] = 1
    df.to_excel(f'{filename}', index=False)
    return True
