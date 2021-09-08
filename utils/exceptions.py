class HuntFlowBaseException(Exception):
    pass


class ExcelFileNotFoundException(HuntFlowBaseException):
    """
    Обработка ошибки отсутствия Excel файла
    """

    def __init__(
            self,
            message=('Excel-файл не найден, '
                     'убедитесь, что он находится в корне '
                     'проекта в папке Resumes')):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class WrongVacancyNameException(HuntFlowBaseException):
    """
    Обработка ошибки неверного названия вакансии в таблице
    """

    def __init__(
            self,
            message=(
                    'Передано неверное название вакансии, '
                    'убедитесь, что в табилце указано такое '
                    'же название вакансии, как на сайте')):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class WrongStatusNameException(HuntFlowBaseException):
    """
    Обработка ошибки неверного названия статуса в таблице
    """

    def __init__(
            self,
            message=(
                    'Передано неверное название статуса, '
                    'убедитесь, что в табилце указан такое '
                    'же статус, как на сайте')):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
