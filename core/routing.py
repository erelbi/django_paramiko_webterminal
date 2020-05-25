from app.consumers import NoseyConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path


application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("notifications/", NoseyConsumer),
    ])
})