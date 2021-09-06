from typing import Dict

import requests

from utils.base_connector import BaseConnector
from utils.entities import ApplicantEntity, ApplicantStatusesEntity, VacancyEntity
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
            'middle_name': upload.fields['name']['middle'],
            'phone': upload.fields['phones'][0],
            'email': upload.fields['email'],
            'position': upload.fields['position'],
            'company': upload.fields['experience'][0]['position'],
            'money': upload.fields['salary'],
            'birthday_day': upload.fields['birthdate']['day'],
            'birthday_month': upload.fields['birthdate']['month'],
            'birthday_year': upload.fields['birthdate']['year'],
            'photo': upload.photo['id'],
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
