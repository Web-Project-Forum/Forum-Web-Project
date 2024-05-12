import unittest
from unittest.mock import MagicMock, patch
from data.models import User
from services import users_service


def fake_user():
    user = User(
        id = 1,
        username = "name",
        password = "password",
        role = "user",
        email = "email@abc.com")
    return user

class UsersServiceTests(unittest.TestCase):

    @patch('services.users_service.read_query')
    def test_find_by_username(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'name', 'password', 'user', 'email@abc.com')]
        # Act
        user = users_service.find_by_username('name')
        # Assert
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'name')


    @patch('services.users_service.insert_query')
    def test_create(self, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1 
        # Act
        user = users_service.create('name', 'password', 'test@example.com')
        # Assert
        self.assertEqual(user.username, 'name')


    @patch('services.users_service.jwt.encode')
    def test_create_token(self, mock_jwt_encode):
        # Arrange
        mock_jwt_encode.return_value = 'encoded_token'
        user = User(id=1, username='name', password='password', role='user', email='email@abc.com')
        # Act
        token = users_service.create_token(user)
        # Assert
        self.assertEqual(token, 'encoded_token')


    @patch('services.users_service.jwt.decode')
    def test_is_authenticated(self, mock_jwt_decode):
        # Arrange
        mock_jwt_decode.return_value = {'id': 1, 'username': 'test_user'}
        # Act
        mock_read_query = MagicMock()
        mock_read_query.return_value = [(1,)]
        # Assert
        with patch('services.users_service.read_query', mock_read_query):
            self.assertTrue(users_service.is_authenticated('valid_token'))

    
