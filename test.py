import unittest, os

import src.jobDatabase
import src.jobCrawler

class TestStringMethods(unittest.TestCase):

    def test_database(self):
        sqlConnection = src.jobDatabase.initalizeDatabase("test.db");
        src.jobDatabase.insertPost(sqlConnection, "test")
        src.jobDatabase.fetchByPosts(sqlConnection, ["test"])

        for row in sqlConnection['cursor']:
            self.assertEqual(row[0], 'test')

        src.jobDatabase.closeConnection(sqlConnection)
        os.remove("test.db")

    def test_crawler(self):
        result = src.jobCrawler.crawlCraigslistListPage('https://phoenix.craigslist.org', 'JobBot - Test', 'csr', 20, 85212, [])
        self.assertTrue(isinstance( result, list))

if __name__ == '__main__':
    unittest.main()