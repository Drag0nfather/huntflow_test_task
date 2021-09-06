class BaseConnector:
    """
    Базовый класс подключения к Huntflow API
    """

    headers = {
        'User-Agent': 'App/1.0 (Andrey18651@gmail.com)',
    }

    def __init__(self, token: str):
        self.headers['Authorization'] = f'Bearer {token}'
