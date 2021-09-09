from utils.argparse import parse_arguments
from utils.connector import HuntFlowApiConnector
from utils.excel import (add_success_point_to_applicant, check_upload_field,
                         convert_excel_to_list)
from utils.exceptions import PathNotFoundException, TokenNotFoundException
from utils.lib import get_full_path
from utils.settings import ACCOUNT_ID


def main(token: str, path: str):
    # Проверка, что в таблице существует поле upload,
    # добавление его в противном случае
    check_upload_field(path)
    # Получение списка кандидатов из таблицы Excel в виде списка словарей
    applicants = convert_excel_to_list(path)
    # Создание экземпляра класса подключения к HuntFlow Api
    connector = HuntFlowApiConnector(token=token)
    # Получение списка всех вакансий
    vacancies = connector.get_vacancies(ACCOUNT_ID)
    # Получение списка всех статусов кандидатов
    statuses = connector.get_statuses(ACCOUNT_ID)
    for applicant in applicants:
        if applicant['upload'] == 0:
            print(applicant['ФИО'])
            # Получаем все поля кандидата из таблицы Excel
            name = applicant['ФИО']
            position = applicant['Должность']
            salary = applicant['Ожидания по ЗП']
            comment = applicant['Комментарий']
            status = applicant['Статус']
            # Получение пути к резюме кандидата
            full_file_name = get_full_path(position, name)
            # Распознавание файла резюме HuntFlow Api
            upload = connector.resume_upload(ACCOUNT_ID, full_file_name)
            print('Резюме распознано системой HuntFlow')
            # Добавление к кандидату поля зарплаты из таблицы
            upload.fields['salary'] = salary
            # Добавления кандидата в базу HuntFlow
            add = connector.add_applicant(ACCOUNT_ID, upload)
            print('Кандидат добавлен в базу HuntFlow')
            # Получение id прикрепленного кандидата
            applicant_id = int(add['result']['id'])
            # Получение id вакансии, на которую будет прикреплен кандидат
            vacancy_id = connector.get_vacancy_id_by_name(vacancies, position)
            # Получение id статуса, который будет присвоен кандидату
            status_id = connector.get_status_id_by_name(statuses, status)
            # Прикрепление кандидата к вакансии в HuntFlow
            connector.add_applicant_to_vacancy(
                ACCOUNT_ID,
                vacancy_id,
                status_id,
                comment,
                applicant_id
            )
            # Добавление кандидату флага успешного прикрепления
            add_success_point_to_applicant(path, name)
            print('Кандидат успешно прикреплен к вакансии в HuntFlow \n')
        continue
    print('Все кандидаты успешно обработаны')
    return


if __name__ == '__main__':
    args = parse_arguments()
    try:
        token = args.token
    except Exception:
        raise TokenNotFoundException
    try:
        path = args.path
    except Exception:
        raise PathNotFoundException
    main(token, path)
