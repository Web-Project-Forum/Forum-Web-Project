import unittest
from unittest.mock import patch
from data.models import ConversationsReport, MessageModel, Messages
from services import message_service
from datetime import datetime

def fake_message():
    message = Messages(
        id=1,
        text="Test message",
        date=datetime(2024, 5, 14, 12, 30),
        sender_id=1,
        receiver_id=2
    )
    return message

class MessagesService_Should(unittest.TestCase):

    
    @patch('services.message_service.read_query')
    def test_get_all(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'username1', 'user'), (2, 'username2', 'admin')]

        # Act
        conversations_reports = message_service.all(123)
        expected_reports = [
            ConversationsReport(id=1, username='username1', role='user'),
            ConversationsReport(id=2, username='username2', role='admin')
        ]
        conversations_reports = list(conversations_reports)
        # Assert 
        self.assertEqual(expected_reports, conversations_reports)

   

    @patch('services.message_service.insert_query')
    @patch('services.message_service.datetime')
    def test_create(self, mock_datetime, mock_insert_query):
        # Arrange
        mock_datetime.now.return_value = datetime(2024, 5, 14, 12, 30)
        mock_insert_query.return_value = 1
        
        message = MessageModel(text="Test message")      
        
        expected_message = fake_message()
        expected_message.date = "12:30:00, 05/14/2024"  # Convert datetime to string format
        
        # Act
        created_message = message_service.create(message, 1, 2)
        
        # Assert
        self.assertEqual(expected_message, created_message)


    @patch('services.message_service.read_query')
    @patch('services.message_service.datetime')
    def test_get_messages_with(self, mock_datetime, mock_read_query):
        mock_datetime.now.return_value = datetime(2024, 5, 14, 12, 30)
        mock_read_query.return_value = [(1, "Test message", datetime(2024, 5, 14, 12, 30), 1, 2)]

        message = message_service.get_messages_with(1, 2)
        message = list(message)
        expected_output = fake_message()

        self.assertEqual([expected_output], message)