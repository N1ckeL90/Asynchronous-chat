import unittest
from server import create_response


class TestServer(unittest.TestCase):

    def test_response_alert(self):
        """ Тест корректного формирования ответа от сервера (при диапазоне кода ответа от 200 до 299 включительно
        выводится alert с сообщением"""
        response = create_response([200, 'OK'])
        self.assertTrue('alert' in response)

    def test_error_is_not_empty(self):
        """ Проверка, что текст ошибки не пустой"""
        response = create_response([400, 'Bad Request'])
        self.assertNotEqual(response['error'], '')


if __name__ == '__main__':
    unittest.main()
