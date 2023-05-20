from django.test import TestCase
from .db_interactions import DB_interactions
from .consumers import FeedConsumer



class Websocket_tests(TestCase):
    def test_get_session_submissions(self):
        self.assertTrue(FeedConsumer.get_session_submissions)

    def test_get_session_object(self):
        self.assertTrue(FeedConsumer.get_session_object)

    
# check for API failure error handling

# check for initial db failure

# check for response success

# test for all DB_interaction functions
class DB_interaction_test(TestCase):

    def test_get_image_tags(self):
        self.assertTrue(DB_interactions.get_image_tags)

    def test_get_salt(self):
        self.assertTrue(DB_interactions.get_salt)

    def test_get_saved_images(self):
        self.assertTrue(DB_interactions.get_saved_images)
        


