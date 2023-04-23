import json
from channels.generic.websocket import WebsocketConsumer
from .db_interactions import DB_interactions
import random



class FeedConsumer(WebsocketConsumer):


    def connect(self):
        self.accept()
        try:
            all_theme_tags = [x.name for x in DB_interactions.tags.all()]
            print(all_theme_tags)
            self.send(text_data=json.dumps({
                'type': 'DB_Success',
                'message': all_theme_tags,
                
            }))
        except:
            self.send(text_data=json.dumps({
                'type': 'DB_fail',
            }))

    # def disconnect(self, close_code):
    #     pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        try:
            theme_tags = DB_interactions.get_image_tags(theme_tags=message)
            associated_quote_list= theme_tags.quotes_set.all()
            
            # Getting a random quote from the choices (I dont want to program another dynamic window to choose which quote to pull)
            img_tags_to_focus_on = random.choice(associated_quote_list).image_tag.all()
            print([x.name for x in img_tags_to_focus_on])

            # request to dahlia api

            # test ones
            req = True
            test_path = 'testimage.jpeg'


            if req:
                print('simulated succesful request')
                self.send(text_data=json.dumps({
                    'source' : 'search',
                    'message' : [x.name for x in img_tags_to_focus_on],
                    'result' : test_path,
                }))

            # if db search was successful but the api didn't give a successful image back 
            else:
                print('simulated failed request')
                self.send(text_data=json.dumps({
                    'source' : 'search',
                    'message' : [x.name for x in img_tags_to_focus_on],
                    'result' : 'fail',
            }))

        except:
            self.send(text_data=json.dumps({
                'source' : 'fail'
            }))
            
        
        




