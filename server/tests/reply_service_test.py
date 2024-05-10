import unittest
from unittest.mock import patch
from data.models import Reply, ReplyResponse, OrderUpdate, Product, User
from server.services import reply_service as service

TEST_TEXT = "anything"
TEST_TOPICS_ID = 2
TEST_AUTHOR_ID = 1


def create_reply(reply_id):
    return Reply(
        id = reply_id,
        text = TEST_TEXT,
        topics_id = TEST_TOPICS_ID,
        author_id = TEST_AUTHOR_ID)

class OrdersService_Should(unittest.TestCase):
    def test_get_by_id_returns_correct_reply(self):
        with patch('services.reply_service.read_query') as get_reply_func:
            # Arrange
            test_id = 5
            get_reply_func.return_value = [
                (test_id, TEST_TEXT, TEST_TOPICS_ID, TEST_AUTHOR_ID)]
            expected = create_reply(test_id)

            # Act
            result = service.get_by_id(test_id)

            # Assert
            self.assertEqual(expected, result)

    def test_create_returns_reply_with_generated_id(self):
        # Arrange
        test_reply = Reply(text=TEST_TEXT, topics_id=TEST_TOPICS_ID, author_id=TEST_AUTHOR_ID)
        # Act
        result = create_reply(test_reply)

        # Assert
        self.assertIsInstance(result.id, int)
        self.assertEqual(result.text, TEST_TEXT)
        self.assertEqual(result.topics_id, TEST_TOPICS_ID)
        self.assertEqual(result.author_id, TEST_AUTHOR_ID)