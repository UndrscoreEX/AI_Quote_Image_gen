import json
from channels.generic.websocket import WebsocketConsumer
from .db_interactions import DB_interactions , submissions_check
import random
from django.contrib.sessions.backends.db import SessionStore
import openai
import os
openai.api_key = os.getenv('OPEN_AI_Secret_Key')




class FeedConsumer(WebsocketConsumer):

    FULL_TEXT = True

    def connect(self):
        self.accept()
        session_submissions = self.scope["session"].get('submissions')
        sess_key = self.scope["session"].session_key
        session_object = SessionStore(session_key=sess_key)
        session_object.load()

        # print('on connection, the session object should look like this: ', session_object)

        session_object['submissions'] = 5
        session_object.save()
        # print(session_object.get('submissions'))

        # This will not work if there is multiple servers. You will need to get a redis DB for a cache layer and query this each time. 
        try:
            all_theme_tags = [x.name for x in DB_interactions.tags.all()]
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

        sess_key = self.scope["session"].session_key
        session_object = SessionStore(session_key=sess_key)
        session_object.load()
        self.send(text_data=json.dumps({
            
        }))
            
        # print('upon receiving websocket request, the session object should look like this: ', session_object)

        session_submissions = self.scope["session"].get('submissions') 
        # print('sessions found from the old scope way ==',session_submissions)
        # print('sessions found from new SessionObject way ==',session_object['submissions'])


        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        salt = DB_interactions.get_salt()


        try:
            theme_tags = DB_interactions.get_image_tags(theme_tags=message)
            associated_quote_list= theme_tags.quotes_set.all()
            
            # Getting a random quote from the choices (I dont want to program another dynamic window to choose which quote to pull)
            random_option = random.choice(associated_quote_list)
            img_tags_to_focus_on = random_option.image_tag.all()


            book = random_option.book.name
            themes = ', '.join([x.name for x in random_option.theme_tag.all()])
            author = random_option.book.author
            quote = random_option.text
            img_tags = [x.name for x in img_tags_to_focus_on]
            # print(author,book, themes, quote)
        
            joined_img_tags = ', '.join(img_tags)

            # print('image tags to be used', img_tags)
            info_from_db = {
                'chosen_theme' : message,
                'all_themes' : themes,
                'book' : book,
                'author' : author,
                'img_tags' : joined_img_tags,
                'quote': quote
            }

            # 　checks if there are enough tokens. 
            if submissions_check(session_submissions):  
                promt_for_dall_e = f'create an an scene that contains the themes of {joined_img_tags} {salt}'

                # test ones
                test_path = 'testimage.jpeg'

                session_submissions -= 1
                self.scope["session"]['submissions'] = session_submissions
                session_object['submissions'] = session_submissions
                session_object.save()

                # print('after saving the new submission numbers :', session_object_contents['submissions'])
                # print('', self.scope["session"]['submissions'])

                # to check whether I will do paid request or just test it. 
                if self.FULL_TEXT:
                    # Dall-E api call 
                    response = openai.Image.create(
                        prompt= promt_for_dall_e,
                        n=1,
                        size="256x256",
                        # size="1024x1024",
                    )



                    dall_e_image = response["data"][0]["url"]
                    # print('Image URL: ',dall_e_image)
                    # print('simulated succesful request')
                    self.send(text_data=json.dumps({
                        'source' : 'search',
                        'message' : img_tags,
                        'result' : test_path,
                        'submissions_left' : session_submissions,
                        'query_content' : info_from_db,
                        'dall_e_image' : dall_e_image,
                        'prompt_used' : promt_for_dall_e,

                    }))
                    try:
                        DB_interactions.save_new_image(quote=random_option, url=dall_e_image, prompt_text=promt_for_dall_e)
                    except Exception as e:
                        print('image didnt save because ',e)
                # if db search was successful but the api didn't give a successful image back 
                else:
                    print('simulated failed api request')
                    self.send(text_data=json.dumps({
                        'source' : 'search',
                        'message' : [x.name for x in img_tags_to_focus_on],
                        'result' : 'db_fail',
                        'query_content' : info_from_db
                }))
                    
            # if db search was successful but the tokens are insufficient
            else:
                print('simulated failed request due to tokens')
                self.send(text_data=json.dumps({
                    'source' : 'search',
                    'message' : [x.name for x in img_tags_to_focus_on],
                    'result' : 'insf_tokens',
                    'query_content' : info_from_db,

            }))
       
        # if db search was unsuccessful
        except Exception as e:
            print(e)
            print('DB query failure')
            self.send(text_data=json.dumps({
                'source' : 'fail',
                'reason' : e,
            }))
            
        
        




