class HuntFlowBaseException(Exception):
    pass


class ExcelFileNotFoundException(HuntFlowBaseException):
    """
    Обработка ошибки отсутствия Excel файла
    """

    def __init__(self, message='Excel-файл не найден, убедитесь, что он находится в корне проекта'):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
