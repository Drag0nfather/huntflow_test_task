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
