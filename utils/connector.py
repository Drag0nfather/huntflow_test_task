from typing import Dict

import requests

from utils.base_connector import BaseConnector
from utils.entities import ApplicantEntity, ApplicantStatusesEntity, VacancyEntity
from utils.exceptions import WrongVacancyNameException, WrongStatusNameException
from utils.lib import get_file_name
from utils.serializers import InputApplicantSerializer, ApplicantStatusesSerializer, VacancySerializer
from utils.settings import HUNTFLOW


class HuntFlowApiConnector(BaseConnector):
    """
    Класс с методами для подключения к Huntflow Api, наследуется от BaseConnector
    """

    def get_me(self) -> Dict:
        """
        Возвращает информацию о текущем авторизованном пользователе,
        Тестовый метод для проверки токена
        """
        me = requests.get(f'{HUNTFLOW}/me', headers=self.headers)
        return me.json()

    def resume_upload(self, account_id: int, file: str) -> ApplicantEntity:
        """
        Метод для распознавания файла резюме
        """
        file_name = get_file_name(file)
        with open(f'{file}', 'rb') as f:
            upload_response = requests.request(
                "POST",
                f'{HUNTFLOW}/account/{account_id}/upload',
                headers={**self.headers, **{'X-File-Parse': 'true'}},
                files=[
                    ('file', (file_name, f, 'application/octet-stream'))
                ]
            )
        upload_response_json = upload_response.json()
        serializer = InputApplicantSerializer().dump(upload_response_json)
        entity = ApplicantEntity(**serializer)
        return entity

    def add_applicant(self, account_id: int, upload: ApplicantEntity):
        """
        Метод добавления кандидата в базу HuntFlow
        """
        body = {
            'last_name': upload.fields['name']['last'],
            'first_name': upload.fields['name']['first'],
            'middle_name': (
                upload.fields['name']['middle']
                if upload.fields['name'] else None
            ),
            'phone': (
                upload.fields['phones'][0]
                if upload.fields['phones'] else None
            ),
            'email': (
                upload.fields['email']
                if upload.fields['email'] else None
            ),
            'position': (
                upload.fields['experience'][0]['position']
                if upload.fields['experience'] else None
            ),
            'company': (
                upload.fields['experience'][0]['company']
                if upload.fields['experience'] else None
            ),
            'money': (
                upload.fields['salary']
                if upload.fields['salary'] else None
            ),
            'birthday_day': (
                upload.fields['birthdate']['day']
                if upload.fields['birthdate'] else None
            ),
            'birthday_month': (
                upload.fields['birthdate']['month']
                if upload.fields['birthdate'] else None
            ),
            'birthday_year': (
                upload.fields['birthdate']['year']
                if upload.fields['birthdate'] else None
            ),
            'photo': (
                upload.photo['id']
                if upload.photo else None
            ),
            'externals': [
                {
                    "data": {
                        "body": upload.text
                    },
                    "auth_type": "NATIVE",
                    "files": [
                        {
                            "id": upload.id
                        }
                    ],
                }
            ]
        }
        request = requests.request(
            'POST',
            f'{HUNTFLOW}/account/{account_id}/applicants',
            headers=self.headers,
            json=body
        )
        if request.status_code == 200:
            return {'success': 'True', 'result': request.json()}
        return {'success': 'False', 'result': request.json()}

    def get_statuses(self, account_id: int) -> ApplicantStatusesEntity:
        """
        Метод, возвращающий список этапов подбора компании
        """
        statuses = requests.get(
            f'{HUNTFLOW}/account/{account_id}/vacancy/statuses',
            headers=self.headers
        )
        statuses_json = statuses.json()
        serializer = ApplicantStatusesSerializer().dump(statuses_json)
        entity = ApplicantStatusesEntity(**serializer)
        return entity

    def get_status_id_by_name(self, statuses: ApplicantStatusesEntity, name: str):
        """
        Получение id статуса по названию
        """
        try:
            for status in statuses.items:
                if status['name'] == name:
                    return status['id']
        except Exception:
            raise WrongStatusNameException

    def get_vacancies(self, account_id: int) -> VacancyEntity:
        """
        Метод, возвращающий список вакансий компании
        """
        vacancies = requests.get(
            f'{HUNTFLOW}/account/{account_id}/vacancies',
            headers=self.headers
        )
        vacancies_json = vacancies.json()
        serializer = VacancySerializer().dump(vacancies_json)
        entity = VacancyEntity(**serializer)
        return entity

    def get_vacancy_id_by_name(self, vacancies: VacancyEntity, name: str):
        """
        Получение id вакансии по имени
        """
        try:
            for vacancy in vacancies.items:
                if vacancy['position'] == name:
                    return vacancy['id']
        except Exception:
            raise WrongVacancyNameException

    def add_applicant_to_vacancy(
            self,
            account_id: int,
            vacancy_id: int,
            status_id: int,
            comment: str,
            applicant_id: int):
        """
        Метод, прикрепляющий кандидата к вакансии компании
        """
        body = {
            'vacancy': vacancy_id,
            'status': status_id,
            'comment': comment,
            'files': [
                {
                    'id': applicant_id
                }
            ]
        }
        request = requests.request(
            'POST',
            f'{HUNTFLOW}/account/{account_id}/applicants/{applicant_id}/vacancy',
            headers=self.headers,
            json=body,
        )
        if request.status_code == 200:
            return {'success': 'True', 'result': request.json()}
        return {'success': 'False', 'result': request.json()}
