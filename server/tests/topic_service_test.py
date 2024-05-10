import unittest
from unittest.mock import patch
from data.models import Topic
from services import topic_service

def fake_topic():
    topic = Topic(
        id=1,
        title="Title",
        content="Content",
        best_reply_id=0,
        locked=False,
        categories_id=1,
        author_id=1
    )
    return topic

class TopicsService_Should(unittest.TestCase):

    @patch('services.topic_service.read_query')
    def test_get_all(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Title', 'Content', 0, False, 1, 1)]
        # Act
        topics = topic_service.all()
        expected_topic = fake_topic()
        # Assert
        self.assertEqual([expected_topic], topics)


    @patch('services.topic_service.read_query')
    def test_get_all_non_private_for_user(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Title', 'Content', 0, False, 1, 1)]

        # Act
        topics = topic_service.all_non_private_for_user(user_id=1, search="test")
        expected_topic = fake_topic()
        # Assert
        self.assertEqual([expected_topic], topics)
    
    
    @patch('services.topic_service.read_query')
    def test_get_all_non_private(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Title', 'Content', 0, False, 1, 1)]

        # Act
        topics = topic_service.all_non_private(search="test")
        expected_topic = fake_topic()
        # Assert
        self.assertEqual([expected_topic], topics)


    @patch('services.topic_service.read_query')
    def test_get_by_id(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Title', 'Content', 0, False, 1, 1)]
        # Act
        topics = topic_service.get_by_id(1)
        expected_topic = fake_topic()
        # Assert
        self.assertEqual(expected_topic, topics)


    @patch('services.topic_service.read_query')
    def test_get_many(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Title', 'Content', 0, False, 1, 1),
                                         (2, 'Title', 'Content', 0, False, 1, 1)]
        # Act
        topics = topic_service.get_many([1, 2])
        expected_topic = fake_topic()
        expected_topic2 = Topic(
        id=2, title="Title", content="Content", best_reply_id=0, 
        locked=False, categories_id=1, author_id=1)

        # Assert
        self.assertEqual([expected_topic, expected_topic2], topics)


    @patch('services.topic_service.read_query')
    def test_get_by_category(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Title', 'Content', 0, False, 1, 1)]
        # Act
        topics = topic_service.get_by_category(1)
        topics = list(topics)
        expected_topic = fake_topic()
        # Assert
        self.assertEqual([expected_topic], topics)

    def test_sorting_by_best_reply_id(self):
        # Arrange
        topics = [
            Topic(id=1, title="Title 1", content="Content 1", best_reply_id=0, locked=False,
        categories_id=1, author_id=1),
            Topic(id=2, title="Title 2", content="Content 2", best_reply_id=0, locked=False,
        categories_id=1, author_id=1),
            Topic(id=3, title="Title 3", content="Content 3", best_reply_id=0, locked=False,
        categories_id=1, author_id=1)]
        
        # Act
        sorted_topics = topic_service.sorting(topics, attribute='best_reply_id')
        expected_sorted_topics = [
            Topic(id=1, title="Title 1", content="Content 1", best_reply_id=0, locked=False,
        categories_id=1, author_id=1),
            Topic(id=2, title="Title 2", content="Content 2", best_reply_id=0, locked=False,
        categories_id=1, author_id=1),
            Topic(id=3, title="Title 3", content="Content 3", best_reply_id=0, locked=False,
        categories_id=1, author_id=1)]
        # Assert
        self.assertEqual(expected_sorted_topics, sorted_topics)


    @patch('services.topic_service.insert_query')
    def test_create_topic(self, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1

        topic = Topic(id=1, title='Title', content='Content', best_reply_id=0, locked=False, categories_id=1, author_id=1)
        # Act
        created_topic = topic_service.create(topic)
        expected_output = fake_topic()
        # Assert
        self.assertEqual(expected_output, created_topic)


    @patch('services.topic_service.read_query')
    def test_exists(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Title', 'Content', 0, False, 1, 1)]
        # Act
        exists = topic_service.exists(1)
        
        # Assert
        self.assertTrue(exists)
    

    @patch('services.topic_service.update_query')
    def test_update_topic(self, mock_update_query):
        # Arrange
        mock_update_query.return_value = [(1, 'Title', 'Content', 0, False, 1, 1)]
        # Act
        old_topic = Topic(id=1, title='Title', content='Content', best_reply_id=0, locked=False, categories_id=1, author_id=1)
        new_topic = Topic(id=1, title='New_Title', content='New_Content', best_reply_id=0, locked=False, categories_id=1, author_id=1)
        topics = topic_service.update(old_topic, new_topic)
        expected_topic = new_topic
        # Assert
        self.assertEqual(expected_topic, topics)
