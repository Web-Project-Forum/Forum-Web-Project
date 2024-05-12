import unittest
from unittest.mock import patch
from data.models import Category
from services import category_service


def fake_category():
    category = Category(
        id = 1,
        name = "Category Name",
        is_private = 0,
        is_locked = 0)
    return category

class CategoryServiceTests(unittest.TestCase):

    @patch('services.category_service.read_query')
    def test_all(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Category Name', 0, 0)]
        # Act
        categories = category_service.all(search=None, skip=0, take=1)
        expected_category = fake_category()
        # Assert
        self.assertEqual([expected_category], list(categories))

    
    @patch('services.category_service.read_query')
    def test_get_by_id(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Category Name', 0, 0)]
        # Act
        category = category_service.get_by_id(1)
        expected_category = fake_category()
        # Assert
        self.assertEqual(expected_category, category)


    @patch('services.category_service.read_query')
    def test_exists(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Category Name', 0)]
        # Act
        exists = category_service.exists(1)
        # Assert
        self.assertTrue(exists)


    @patch('services.category_service.insert_query')
    def test_create(self, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1  
        category = Category(id = 1, name='Category Name', is_private=0, is_locked=0)
        
        # Act
        created_category = category_service.create(category)
        expected_output = fake_category()
        # Assert
        self.assertEqual(expected_output, created_category)

    
    @patch('services.category_service.update_query')
    def test_delete(self, mock_update_query):
        # Arrange
        category_id = 1
        # Act
        category_service.delete(category_id)
        # Assert
        mock_update_query.assert_any_call('DELETE FROM categories WHERE categories_id = ?', (category_id,))
        mock_update_query.assert_any_call('DELETE FROM categories WHERE id = ?', (category_id,))


    @patch('services.category_service.update_query')
    def test_update_category(self, mock_update_query):
        # Arrange
        mock_update_query.return_value = [(1, 'Category Name', 0, 0)]
        # Act
        old_category = Category(id=1, name='Old Name', is_private=0, is_locked=0)
        new_category = Category(id=1, name='New Name', is_private=0, is_locked=0)
        categories = category_service.update(old_category, new_category)
        expected_topic = new_category
        # Assert
        self.assertEqual(expected_topic, categories)


    @patch('services.category_service.read_query')
    def test_get_private_categories(self, mock_read_query):
        # Arrange
        user_id = 1
        mock_read_query.return_value = [(1,), (2,), (3,)]
        # Act
        private_categories = category_service.get_private_categories(user_id)
        mock_read_query.assert_called_once_with(
            'SELECT category_id from permissions where user_id = ?', (user_id,))
        # Assert
        self.assertEqual(private_categories, {1, 2, 3})