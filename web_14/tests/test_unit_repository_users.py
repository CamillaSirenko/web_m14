# import unittest
# from unittest.mock import MagicMock
# from libgravatar import Gravatar
# from sqlalchemy.orm import Session
# from src.database.models import Contact
# from src.schemas import UserModel
# from src.repository.users import (
#     get_user_by_email,
#     create_user,
#     update_token,
#     update_user_avatar,
#     confirmed_email,
# )


# class TestUsers(unittest.IsolatedAsyncioTestCase):
#     def setUp(self):
#         self.db = MagicMock(spec=Session)

#     async def test_get_user_by_email(self):
#         user = Contact(email="test@example.com")
#         self.db.query(Contact).filter(Contact.email == "test@example.com").first.return_value = user
#         result = await get_user_by_email("test@example.com", self.db)
#         self.assertEqual(result, user)

#     async def test_create_user_with_gravatar(self):
#         body = UserModel(email="test@example.com")
#         gravatar_mock = MagicMock(spec=Gravatar)
#         gravatar_mock.get_image.return_value = "avatar_url"
#         with unittest.mock.patch("src.users.Gravatar", return_value=gravatar_mock):
#             result = await create_user(body, self.db)
#         self.assertEqual(result.email, body.email)
#         self.assertEqual(result.avatar, "avatar_url")

#     async def test_create_user_without_gravatar(self):
#         body = UserModel(email="test@example.com")
#         gravatar_mock = MagicMock(spec=Gravatar)
#         gravatar_mock.get_image.side_effect = Exception("Failed to fetch Gravatar")
#         with unittest.mock.patch("src.users.Gravatar", return_value=gravatar_mock):
#             result = await create_user(body, self.db)
#         self.assertEqual(result.email, body.email)
#         self.assertIsNone(result.avatar)

#     async def test_update_token(self):
#         user = Contact()
#         await update_token(user, "new_token", self.db)
#         self.assertEqual(user.refresh_token, "new_token")
#         self.db.commit.assert_called_once()

#     async def test_update_user_avatar(self):
#         user = Contact()
#         await update_user_avatar(user, "new_avatar_url", self.db)
#         self.assertEqual(user.avatar, "new_avatar_url")
#         self.db.commit.assert_called_once()

#     async def test_confirmed_email(self):
#         user = Contact(email="test@example.com", confirmed=False)
#         self.db.query().filter().first.return_value = user
#         await confirmed_email("test@example.com", self.db)
#         self.assertTrue(user.confirmed)
#         self.db.commit.assert_called_once()


# if __name__ == "__main__":
#     unittest.main()

 
