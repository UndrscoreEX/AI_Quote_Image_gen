import json
from channels.generic.websocket import WebsocketConsumer
from .db_interactions import DB_interactions , submissions_check
import random


class FeedConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        session_submissions = self.scope["session"].get('submissions')
        print(session_submissions)
        
        # This will not work if there is multiple servers. You will need to get a redis DB for a cache layer and query this each time. 

        try:
            all_theme_tags = [x.name for x in DB_interactions.tags.all()]
            print(all_theme_tags)
            self.send(text_data=json.dumps({
                'type': 'DB_Success',
                'message': all_theme_tags,
                'submissions_left' : session_submissions
            }))
        except:
            self.send(text_data=json.dumps({
                'type': 'DB_fail',
            }))

    # def disconnect(self, close_code):
    #     pass

    def receive(self, text_data):

        # can this be edited in browser? Not important for this project, but ill need to use a redis cache layer in a full production. 
        session_submissions = self.scope["session"].get('submissions')
        print('sessions found ==',session_submissions)

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        try:
            theme_tags = DB_interactions.get_image_tags(theme_tags=message)
            associated_quote_list= theme_tags.quotes_set.all()
            
            # Getting a random quote from the choices (I dont want to program another dynamic window to choose which quote to pull)
            random_option = random.choice(associated_quote_list)
            img_tags_to_focus_on = random_option.image_tag.all()


            #other info about the record 
            # messages is chosen theme

            book = random_option.book.name
            themes = ','.join([x.name for x in random_option.theme_tag.all()])
            author = random_option.book.author
            quote = random_option.text
            print(author,book, themes, quote)
            img_tags = [x.name for x in img_tags_to_focus_on]
        
            # print(dir(random_option),'afsadfdsafsdjkhfkldsaj')
            print('image tags to be used', img_tags)
            info_from_db = {
                'chosen_theme' : message,
                'all_themes' : themes,
                'book' : book,
                'author' : author,
                'img_tags' : [x.name for x in img_tags_to_focus_on],
                'quote': quote
            }
            info = json.dumps(info_from_db)
            print(info)
            if submissions_check(session_submissions):  
                #¥¥¥¥¥¥¥¥ request to dahlia api

                # test ones
                req = True
                test_path = 'testimage.jpeg'

                session_submissions -= 1
                self.scope["session"]['submissions'] = session_submissions
                print(self.scope["session"]['submissions'])

                if req:
                    print('simulated succesful request')
                    self.send(text_data=json.dumps({
                        'source' : 'search',
                        'message' : img_tags,
                        'result' : test_path,
                        'submissions_left' : session_submissions,
                        'query_content' : info_from_db

                    }))

                # if db search was successful but the api didn't give a successful image back 
                else:
                    print('simulated failed request')
                    self.send(text_data=json.dumps({
                        'source' : 'search',
                        'message' : [x.name for x in img_tags_to_focus_on],
                        'result' : 'db_fail',
                        'query_content' : info_from_db
                }))
                
            else:
                print('simulated failed request')
                self.send(text_data=json.dumps({
                    'source' : 'search',
                    'message' : [x.name for x in img_tags_to_focus_on],
                    'result' : 'insf_tokens',
                    'query_content' : info_from_db,

            }))

        except:
            self.send(text_data=json.dumps({
                'source' : 'fail'
            }))
            
        
        




