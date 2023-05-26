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

    def get_session_submissions(self):
        return self.scope["session"].get('submissions')
    
    def get_session_object(self):
        sess_key = self.scope["session"].session_key
        session_object = SessionStore(session_key=sess_key)
        return session_object
        
        

    def connect(self):
        self.accept()
        session_submissions = self.get_session_submissions()

        session_object = self.get_session_object()
        session_object.load()

        images = DB_interactions.get_saved_images()
        print('the 5 random images are :',images)

        # ::::: to give extra tokens upon hard refresh, use this:
        session_object['submissions'] = 5
        session_object.save()

        # :::: This will not work if there is multiple servers. You will need to get a redis DB for a cache layer and query this each time. 
        try:
            all_theme_tags = [x.name for x in DB_interactions.tags.all()]
            self.send(text_data=json.dumps({
                'type': 'DB_Success',
                'result' : 'initial DB setup',
                'message': all_theme_tags,
                'submissions_left' : session_submissions
            }))
        except:
            self.send(text_data=json.dumps({
                'type': 'DB_fail',
            }))



    def receive(self, text_data):

        session_object = self.get_session_object()
        session_object.load()
            

        session_submissions = self.get_session_submissions()

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        salt = DB_interactions.get_salt()
        print(salt)



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
                'quote': quote,

            }

            # 　checks if there are enough tokens. 
            if submissions_check(session_submissions):  
                promt_for_dall_e = f'create an an scene that contains the themes of {joined_img_tags} {salt}'

                session_submissions -= 1
                self.scope["session"]['submissions'] = session_submissions
                session_object['submissions'] = session_submissions
                session_object.save()


                # to check whether I will do paid request or just test it. 
                if self.FULL_TEXT:
                    # Dall-E api call 
                    response = openai.Image.create(
                        # prompt= 'simulate something that will be blocked by Dall E',
                        prompt= promt_for_dall_e,
                        n=1,
                        # size="256x256",
                        size ='512x512',
                        # size="1024x1024",
                    )



                    dall_e_image = response["data"][0]["url"]
                    print('Image URL: ',dall_e_image)
                    # print('simulated succesful request')
                    self.send(text_data=json.dumps({
                        'type' : 'search',
                        'message' : img_tags,
                        'result' : dall_e_image,
                        'submissions_left' : session_submissions,
                        'query_content' : info_from_db,
                        'prompt_used' : promt_for_dall_e,

                    }))

                    # :::: to save to db for the carousel

                    # try:
                    #     DB_interactions.save_new_image(quote=random_option, url=dall_e_image, prompt_text=promt_for_dall_e)
                    # except Exception as e:
                    #     print('image didnt save because ',e)


                # if db search was successful but the api didn't give a successful image back 
                else:
                    print('simulated failed api request')
                    self.send(text_data=json.dumps({
                        'type' : 'API_fail',
                        'message' : [x.name for x in img_tags_to_focus_on],
                        'result' : 'API_fail',
                        'query_content' : info_from_db
                }))
                    
            # if db search was successful but the tokens are insufficient
            else:
                print('simulated failed request due to tokens')
                self.send(text_data=json.dumps({
                    'type' : 'insf_tokens',
                    'message' : [x.name for x in img_tags_to_focus_on],
                    'result' : 'insf_tokens',
                    'query_content' : info_from_db,

            }))
       
        # if db search was unsuccessful
        except Exception as e:
            print('error is :',e)
            print('DB query failure')
            self.send(text_data=json.dumps({
                'type' : 'search_fail',
                'result' : str(e),
            }))
            print('sldjfjhakl;djfalsdj')
            
        
        
    def disconnect(self, close_code):
        pass



