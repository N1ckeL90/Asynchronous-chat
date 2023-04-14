import unittest
from client import process_response_from_server


class TestClient(unittest.TestCase):

    def test_200_response(self):
        """Тест корректного разбора ответа 200"""
        msg = process_response_from_server({'response': 200})
        self.assertEqual(msg, '200: Ok')

    def test_400_message(self):
        """Тест корректного вывода текста ошибки"""
        msg = process_response_from_server({'response': 400, 'error': 'Bad request'})
        self.assertNotEqual(msg, '')


if __name__ == '__main__':
    unittest.main()
