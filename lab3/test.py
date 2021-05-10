import unittest
import aiohttp
from unittest import IsolatedAsyncioTestCase

from database import cache, database
from app import bot


class TestDatabase(IsolatedAsyncioTestCase):
    async def test_crud(self):
        await database.insert_users(1111, "1 2 3")
        self.assertEqual(await database.select_users(1111), ('1 2 3',))
        await database.delete_users(1111)
        self.assertEqual(await database.select_users(1111), None)


class TestCache(unittest.TestCase):
    def test_connection(self):
        self.assertTrue(cache.ping())

    def test_response_type(self):
        cache.setex("test_type", 10, "Hello")
        response = cache.get("test_type")
        self.assertEqual(type(response), str)


class TestBot(IsolatedAsyncioTestCase):

    async def test_bot_auth(self):
        bot.bot._session = aiohttp.ClientSession()
        bot_info = await bot.bot.get_me()
        await bot.bot._session.close()

        self.assertEqual(bot_info["username"], "lab3_deadlines_bot")


if __name__ == '__main__':
    unittest.main()
