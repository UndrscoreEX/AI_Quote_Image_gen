import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import ai_image_gen.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quote_ai.settings')

application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : AuthMiddlewareStack( 
            URLRouter( 
                ai_image_gen.routing.websocket_urlpatterns
            )   
    )
})  
