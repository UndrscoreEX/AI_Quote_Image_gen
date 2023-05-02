"""
ASGI config for quote_ai project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import ai_image_gen.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quote_ai.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : AuthMiddlewareStack( 
            URLRouter( 
                ai_image_gen.routing.websocket_urlpatterns
            )   
    )
})  

# Fix this and figure out how to use this with Mysql. That is the poblem so far. `________