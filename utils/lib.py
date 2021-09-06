from typing import Optional


def get_file_name(file: Optional[str]) -> Optional[str]:
    """
    Возвращает имя файла резюме
    """
    return file.split('/')[-1] if file else None
