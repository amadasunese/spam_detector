import unittest
from spamdetector import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_spam_prediction(self):
        response = self.app.post('/predict', data={'text': 'URGENT! You have won'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('spam', response.json)
        self.assertTrue(response.json['spam'])

    def test_ham_prediction(self):
        response = self.app.post('/predict', data={'text': 'How are you today?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('spam', response.json)
        self.assertFalse(response.json['spam'])

    def test_no_text_provided(self):
        response = self.app.post('/predict', data={})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
