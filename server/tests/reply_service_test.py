import unittest
from unittest.mock import patch
from data.models import Reply
from services import reply_service 

TEST_TEXT = "anything"
TEST_TOPICS_ID = 2
TEST_AUTHOR_ID = 1


def fake_reply():
    reply = Reply(
        id = 1,
        text = "anything",
        topics_id = 2,
        author_id = 1)
    return reply

class RepliesService_Should(unittest.TestCase):
    @patch('services.reply_service.read_query')
    def test_get_all(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, TEST_TEXT, TEST_TOPICS_ID, TEST_AUTHOR_ID)]
        # Act
        replies = reply_service.all(search="test")
        replies = list(replies)
        expected_output = fake_reply()
        # Assert
        self.assertEqual([expected_output], replies)


    @patch('services.reply_service.read_query')
    def test_get_by_id(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, TEST_TEXT, TEST_TOPICS_ID, TEST_AUTHOR_ID)]
        # Act
        topics = reply_service.get_by_id(1)
        expected_output = fake_reply()
        # Assert
        self.assertEqual(expected_output, topics)

   

    @patch('services.reply_service.insert_query')
    def test_create_reply(self, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1
        # Act
        reply = Reply(id=1, text=TEST_TEXT, topics_id=TEST_TOPICS_ID, author_id=TEST_AUTHOR_ID)
        created_reply = reply_service.create(reply)
        expected_output = fake_reply()
        # Assert
        self.assertEqual(expected_output, created_reply)

    @patch('services.reply_service.read_query')
    def test_get_by_topic(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, TEST_TEXT, TEST_TOPICS_ID, TEST_AUTHOR_ID)]
        # Act
        replies = reply_service.get_by_topic(2)
        replies = list(replies)
        expected_output = fake_reply()
         # Assert
        self.assertEqual([expected_output], replies)
