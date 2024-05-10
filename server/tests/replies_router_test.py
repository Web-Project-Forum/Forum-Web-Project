import unittest
from unittest.mock import Mock, patch
from common.responses import Unauthorized
from data.models import User
from routers import replies as replies_router

mock_reply_service = Mock(spec='services.reply_service')
mock_topic_service = Mock(spec='services.topic_service')
mock_category_service = Mock(spec='services.category_service')
mock_users_service = Mock(spec='services.users_service')

replies_router.reply_service = mock_reply_service
replies_router.topic_service = mock_topic_service
replies_router.category_service = mock_category_service
replies_router.users_service = mock_users_service


def fake_reply():
    reply = Mock()

    return reply


def fake_admin():
    admin = Mock()
    admin.is_admin = lambda: True

    return admin


def fake_user():
    admin = Mock()
    admin.is_admin = lambda: False

    return admin

class ReplysRouter_Should(unittest.TestCase):

    def setUp(self) -> None:
        mock_reply_service.reset_mock()
        mock_topic_service.reset_mock()
        mock_category_service.reset_mock()
        mock_users_service.reset_mock()

    def test_get_replies_returns_all_replies(self):
        with patch('routers.replies.get_user_or_raise_401') as get_user_func:
            # Arrange
            test_repies = [fake_reply(), fake_reply()]
            get_user_func.return_value = fake_admin()
            mock_reply_service.all = lambda: test_repies

            # Act
            result = replies_router.get_replies()

            # Assert
            self.assertEqual(test_repies, result)

