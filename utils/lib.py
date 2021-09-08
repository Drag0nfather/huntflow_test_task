from typing import Optional
import os


def get_file_name(file: Optional[str]) -> Optional[str]:
    """
    Возвращает имя файла резюме
    """
    return file.split('/')[-1] if file else None


def normalize(string: str) -> str:
    """
    Приводит букву "й" в Unicode к единому виду
    """
    string = string.strip()
    old_chars = chr(1080) + chr(774)
    new_chars = chr(1081)
    return string.replace(old_chars, new_chars)


def get_full_path(folder: str, filename: str) -> str:
    """
    Возвращает полное имя файла с расширением по имени папки и названию резюме
    """
    files = os.listdir(f'./Resumes/{folder}')
    for file in files:
        if normalize(file).startswith(normalize(filename)):
            full_path = f'./Resumes/{folder}/{file}'
            return full_path
