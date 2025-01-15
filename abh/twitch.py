from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, InvalidRefreshTokenException
from twitchAPI.chat import Chat, EventData
import keyring

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
TARGET_CHANNEL = 'rafalagoon'  # El chat a conectarse
SERVICE_NAME = 'animal-brawl-helper'  # El nombre del servicio en el keyring donde se guardaran los tokens


async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)


async def connectToChat():
    """Esta función inicia la conexión al chat y devuelve la instancia de Twitch y el chat

    Returns:
        list: la instancia de Twitch y del chat
    """

    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token = None
    refresh_token = None
    have_tokens = False

    # Comprobamos si los tokens se encuentran en el keyring
    try:
        cred1 = keyring.get_credential(SERVICE_NAME, 'token')
        token = cred1.password
        cred2 = keyring.get_credential(SERVICE_NAME, 'refresh_token')
        refresh_token = cred2.password
        have_tokens = True
    except:
        have_tokens = False

    if have_tokens:
        try:
            # Se llama a la función user_refresh si hay que refrescar el token
            twitch.user_auth_refresh_callback = user_refresh
            await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
        except InvalidRefreshTokenException:
            # Si sale este error es que el token de refresco no es valido
            # así que procedemos a borrar el archivo y devolvemos None
            return [None, None]
    else:
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
        # Save token and refresh_token
        saveToken(token, refresh_token)

    # create chat instance
    chat = await Chat(twitch)

    return [twitch, chat]


async def sendCommand(chat, command=''):
    """Envía un comando al chat

    Args:
        chat: La instancia del chat al que se mandara el comando
        command (str, optional): El comando a enviar. por defecto es ''.
    """
    await chat.send_message(TARGET_CHANNEL, command)


async def user_refresh(token: str, refresh_token: str):
    """Esta función se llama cuando es necesario actualizar el token del usuario

    Args:
        token (str): El nuevo token
        refresh_token (str): El token de refresco
    """
    saveToken(token, refresh_token)


def saveToken(token: str, refresh_token: str):
    """Guarda el token y el token de refresco en el keyring del sistema
    para que dichos datos estén en un lugar seguro

    Args:
        token (str): El token
        refresh_token (str): el token de refresco
    """
    keyring.set_password(SERVICE_NAME, 'token', token)
    keyring.set_password(SERVICE_NAME, 'refresh_token', refresh_token)
