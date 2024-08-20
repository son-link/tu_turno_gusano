from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.chat import Chat, EventData
'''
Para usar la API del chat de Twitch es necesario crear una nueva aplicación
para obtener el ID de la apliación así como la clave secreta.
Para ello tienes que ir a https://dev.twitch.tv/console
y crear una con los siguientes datos:

* Nombre: el que quieras
* URL de redireccionamiento de OAuth: http://localhost:17563
* Categoría: Chat Bot
* Tipo de cliente: Confidencial
'''

APP_ID = ''  # El ID de cliente proporcionado por Twitch
APP_SECRET = ''  # El secreto
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = ''  # El chat a conectarse


async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)


async def connectToChat():
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)

    return [twitch, chat]


async def sendCommand(chat, command=''):
    await chat.send_message(TARGET_CHANNEL, command)
