from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, InvalidRefreshTokenException
from twitchAPI.chat import Chat, EventData
from .utils import PasswdModal, checkTokens, CONFIG_FILE
from jsoncrypt import Encrypt, Decrypt


'''
Para usar la API del chat de Twitch es necesario crear una nueva aplicación
para obtener el ID de la aplicación así como la clave secreta.
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


class TwitchCon():
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    async def on_ready(ready_event: EventData):
        print('Bot is ready for work, joining channels')
        await ready_event.chat.join_room(TARGET_CHANNEL)

    async def connectToChat(self):
        """Esta función inicia la conexión al chat y devuelve la instancia de Twitch y el chat

        Returns:
            list: la instancia de Twitch y del chat
        """

        twitch = await Twitch(APP_ID, APP_SECRET)
        auth = UserAuthenticator(twitch, USER_SCOPE)
        token = None
        refresh_token = None
        have_tokens = checkTokens()

        if have_tokens:
            try:
                password = PasswdModal(self.parent)
                decrypted_dict = Decrypt.jsonfile(CONFIG_FILE, password=password)
                if not decrypted_dict:
                    return [-1, -1]

                token = decrypted_dict['token']
                refresh_token = decrypted_dict['refresh_token']

                # Se llama a la función user_refresh si hay que refrescar el token
                twitch.user_auth_refresh_callback = self.user_refresh
                await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
            except InvalidRefreshTokenException:
                # Si sale este error es que el token de refresco no es valido
                # así que procedemos a borrar el archivo y devolvemos None
                return [None, None]
        else:
            token, refresh_token = await auth.authenticate()
            await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
            # Save token and refresh_token
            self.saveTokens(token, refresh_token)

        # create chat instance
        chat = await Chat(twitch)

        return [twitch, chat]

    async def sendCommand(self, chat, command=''):
        """Envía un comando al chat

        Args:
            chat: La instancia del chat al que se mandara el comando
            command (str, optional): El comando a enviar. por defecto es ''.
        """
        await chat.send_message(TARGET_CHANNEL, command)

    async def user_refresh(self, token: str, refresh_token: str):
        """Esta función se llama cuando es necesario actualizar el token del usuario

        Args:
            token (str): El nuevo token
            refresh_token (str): El token de refresco
        """
        self.saveTokens(token, refresh_token)

    def saveTokens(self, token: str, refresh_token: str, ):
        """Guarda el token y el token de refresco en el keyring del sistema
        para que dichos datos estén en un lugar seguro

        Args:
            token (str): El token
            refresh_token (str): el token de refresco
        """

        password = PasswdModal(self.parent)
        data_encrypted = Encrypt.dictionary({
            'token': token,
            'refresh_token': refresh_token
        }, password=password)

        with open(CONFIG_FILE, 'w') as f:
            f.write(data_encrypted)
            f.close()
