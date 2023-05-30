import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quote_ai.settings')
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import ai_image_gen.routing
from daphne.server import Server




application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : AuthMiddlewareStack( 
            URLRouter( 
                ai_image_gen.routing.websocket_urlpatterns
            )   
    )
})  

if __name__ == "__main__":
    server = Server(application)
    server.run(application, host='0.0.0.0', port=2020)