import ttkbootstrap.localization
ttkbootstrap.localization.initialize_localities = bool

import ttkbootstrap as ttk
import ttkbootstrap.constants as constants
from ttkbootstrap.style import Style
from os import path
from .twitch import TwitchCon, TARGET_CHANNEL
from twitchAPI.type import ChatEvent
from twitchAPI.chat import EventData
import asyncio
import sys

LOCAL_DIR = path.dirname(path.realpath(__file__))


class TurnoGusano(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        style = Style()
        style.load_user_themes(f'{LOCAL_DIR}/theme.json')
        style.theme_use(themename='animalbrawl')
        master.place_window_center()
        self.master = master
        self.twitchCon = TwitchCon(master)
        self.twitch = None
        self.chat = None
        self.__passwd = None

        self.master['padx'] = 5
        self.master['pady'] = 5

        # Pestaña del juego
        self.notebook = ttk.Notebook(self.master, padding=10)
        self.notebook.pack(expand=True)

        frame1 = ttk.Frame(self.notebook, padding=10)
        frame2 = ttk.Frame(self.notebook, padding=10)

        frame1.pack(fill='both', padx=10, pady=10, expand=True)
        frame2.pack(fill='both', padx=10, pady=10, expand=True)

        # add frames to notebook

        self.notebook.add(frame1, text='Juego')
        self.notebook.add(frame2, text='Configuración')

        self.actions = ['', '', '']
        self.combosOptions = [
            '',
            'Saltar',
            'Voltear',
            'Disparar',
            'Puñetazo'
        ]
        self.optsActions = {
            '': '',
            'Saltar': 'j',
            'Voltear': 'f',
            'Disparar': 's',
            'Puñetazo': 'p'
        }

        # self.skins = ['elephant giraffe hippo monkey panda parrot penguin pig rabbit snake']
        '''self.skinsValues = {
            'Cerdo': 'pig',
            'Conejo': 'rabbit',
            'Elefante': 'elephant',
            'Hipopótamo': 'hippo',
            'Jirafa': 'giraffe',
            'Loro': 'parrot',
            'Mono': 'monkey',
            'Panda': 'panda',
            'Pingüino': 'penguin',
            'Serpiente': 'snake',
        }'''

        self.skinsValues = {
            'Cerdo': 'pig',
            'Gato': 'cat01',
            'La papa': 'lapapa',
            'Mono': 'monkey',
            'Perro': 'dog01',
            'Pingüino': 'penguin',
            'Zorro': 'fox'
        }

        # self.hats = ['txapela tophat barretina fez sombrero tricornio']
        self.hatsValues = [
            'Txapela',
            'Tophat',
            'Barretina',
            'Fez',
            'Sombrero',
            'Tricornio'
        ]

        # iconos
        copy_img = path.join(LOCAL_DIR, 'assets/icons/copy.png')
        self.icon_copy = ttk.PhotoImage(file=copy_img)

        twitch_img = path.join(LOCAL_DIR, 'assets/icons/twitch.png')
        self.icon_twitch = ttk.PhotoImage(file=twitch_img)

        send_img = path.join(LOCAL_DIR, 'assets/icons/send.png')
        self.icon_send = ttk.PhotoImage(file=send_img)

        play_img = path.join(LOCAL_DIR, 'assets/icons/play.png')
        self.icon_play = ttk.PhotoImage(file=play_img)

        # Interfaz

        text1 = ttk.Label(frame1, text='Selecciona tus acciones')
        text1.grid(row=0, column=0, columnspan=3, sticky=constants.W)

        text2 = ttk.Label(frame1, text='Acción')
        text2.grid(row=1, column=0, pady=10)

        text3 = ttk.Label(frame1, text='Angulo')
        text3.grid(row=1, column=1, pady=10)

        text4 = ttk.Label(frame1, text='Fuerza')
        text4.grid(row=1, column=2, pady=10)

        # 1ª acción

        self.setvar('action1', '')
        self.accion1 = ttk.Combobox(
            frame1,
            values=self.combosOptions,
            state='readonly',
        )
        self.accion1.bind(
            '<<ComboboxSelected>>',
            lambda event, entry=self.accion1: self.update_value(entry.get(), 'action1'))
        self.accion1.grid(row=2, column=0, sticky=constants.W, pady=5)

        self.angle1Frame = ttk.Frame(frame1)
        # self.angle1Frame.grid(row=2, column=1, sticky=constants.W, padx=10)
        self.setvar('angle1', 0)

        angle1Label = ttk.Label(self.angle1Frame, textvariable='angle1', anchor=constants.CENTER)
        angle1Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.angle1 = ttk.Scale(
            self.angle1Frame,
            from_=0,
            to=120,
            command=lambda x, y='angle1': self.update_value(x, y),
            state=constants.DISABLED,
            bootstyle=constants.PRIMARY,
        )
        self.angle1.pack()

        self.force1Frame = ttk.Frame(frame1)
        # self.force1Frame.grid(row=2, column=2, sticky=constants.W, padx=10)
        self.setvar('force1', 1)

        angle1Label = ttk.Label(self.force1Frame, textvariable='force1', anchor=constants.CENTER)
        angle1Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.force1 = ttk.Scale(
            self.force1Frame,
            from_=1,
            to=10,
            command=lambda x, y='force1': self.update_value(x, y),
            state=constants.DISABLED,
            bootstyle=constants.PRIMARY
        )
        self.force1.pack()

        # 2ª acción

        self.setvar('action2', '')
        self.accion2 = ttk.Combobox(
            frame1,
            values=self.combosOptions,
            state='readonly',
        )
        self.accion2.bind(
            '<<ComboboxSelected>>',
            lambda event, entry=self.accion2: self.update_value(entry.get(), 'action2'))
        self.accion2.grid(row=3, column=0, sticky=constants.W, pady=5)

        self.angle2Frame = ttk.Frame(frame1)
        # self.angle2Frame.grid(row=3, column=1, sticky=constants.W, padx=10)
        self.setvar('angle2', 0)

        angle2Label = ttk.Label(self.angle2Frame, textvariable='angle2', anchor=constants.CENTER)
        angle2Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.angle2 = ttk.Scale(
            self.angle2Frame,
            from_=0,
            to=120,
            command=lambda x, y='angle2': self.update_value(x, y),
            state=constants.DISABLED
        )
        self.angle2.pack()

        self.force2Frame = ttk.Frame(frame1)
        # self.force2Frame.grid(row=3, column=2, sticky=constants.W, padx=10)
        self.setvar('force2', 1)

        force2Label = ttk.Label(self.force2Frame, textvariable='force2', anchor=constants.CENTER)
        force2Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.force2 = ttk.Scale(
            self.force2Frame,
            from_=1,
            to=10,
            command=lambda x, y='force2': self.update_value(x, y),
            state=constants.DISABLED
        )
        self.force2.pack()

        # 3ª acción

        self.setvar('action3', '')
        self.accion3 = ttk.Combobox(
            frame1,
            values=self.combosOptions,
            state='readonly',
        )
        self.accion3.bind(
            '<<ComboboxSelected>>',
            lambda event, entry=self.accion3: self.update_value(entry.get(), 'action3'))
        self.accion3.grid(row=4, column=0, sticky=constants.W, pady=5)

        self.angle3Frame = ttk.Frame(frame1)
        # self.angle3Frame.grid(row=4, column=1, sticky=constants.W, padx=10)
        self.setvar('angle3', 0)

        angle3Label = ttk.Label(self.angle3Frame, textvariable='angle3', anchor=constants.CENTER)
        angle3Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.angle3 = ttk.Scale(
            self.angle3Frame,
            from_=0,
            to=120,
            command=lambda x, y='angle3': self.update_value(x, y),
            state=constants.DISABLED
        )
        self.angle3.pack()

        self.force3Frame = ttk.Frame(frame1)
        # self.force3Frame.grid(row=4, column=2, sticky=constants.W, padx=10)
        self.setvar('force3', 1)

        force3Label = ttk.Label(self.force3Frame, textvariable='force3', anchor=constants.CENTER)
        force3Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.force3 = ttk.Scale(
            self.force3Frame,
            from_=1,
            to=10,
            command=lambda x, y='force3': self.update_value(x, y),
            state=constants.DISABLED
        )
        self.force3.pack()

        # Este botón copia el comando al portapapeles
        self.btnCopy = ttk.Button(
            master=frame1,
            text="Copiar",
            command=self.toClipboard,
            bootstyle=constants.PRIMARY,
            width=6,
            state=constants.DISABLED,
            image=self.icon_copy,
            compound=ttk.LEFT,
        )
        self.btnCopy.grid(row=5, column=0, pady=10, sticky=constants.W)

        self.commandText = ttk.Label(frame1, textvariable='command', anchor=constants.W)
        self.commandText.grid(row=5, column=1, columnspan=2, pady=10, sticky=constants.W)
        self.setvar('command', '')

        # Este botón copia el comando al portapapeles
        self.btnConTwitch = ttk.Button(
            master=frame1,
            text="Conectar a Twitch",
            command=self.connectTwitch,
            bootstyle=constants.PRIMARY,
            image=self.icon_twitch,
            compound=ttk.LEFT
        )
        self.btnConTwitch.grid(row=6, column=0, pady=10, sticky=constants.W)

        self.btnPlayTwitch = ttk.Button(
            master=frame1,
            text="Jugar",
            bootstyle=constants.PRIMARY,
            state=constants.DISABLED,
            image=self.icon_play,
            compound=ttk.LEFT,
            command=self.sendPlay
        )
        self.btnPlayTwitch.grid(row=6, column=1, pady=10, sticky=constants.W)

        self.btnSendTwitch = ttk.Button(
            master=frame1,
            text="Enviar al chat",
            command=self.toChat,
            bootstyle=constants.PRIMARY,
            state=constants.DISABLED,
            image=self.icon_send,
            compound=ttk.LEFT
        )
        self.btnSendTwitch.grid(row=6, column=2, padx=10, sticky=constants.W, columnspan=2)

        # A partir de aquí van las opciones extra del juego

        # Aquí almacenaremos los comandos de configuración
        self.setvar('commandConf', '')

        text2 = ttk.Label(frame2, text='Otras acciones')
        text2.grid(row=0, column=4, columnspan=3, sticky=constants.W)

        # Skin

        labelSkins = ttk.Label(frame2, text='Skin')
        labelSkins.grid(row=1, column=4, sticky=constants.W)

        self.setvar('skin', 'Pingüino')
        self.skinCombo = ttk.Combobox(
            frame2,
            values=[
                'Cerdo',
                'Gato',
                'La papa',
                'Mono',
                'Perro',
                'Pingüino',
                'Zorro',
            ],
            state='readonly',
            textvariable='skin'
        )
        self.skinCombo.grid(row=1, column=5, sticky=constants.W, padx=5)

        self.btnCopySkin = ttk.Button(
            master=frame2,
            image=self.icon_copy,
            command=lambda: self.genCommandSkin('copy')
        )
        self.btnCopySkin.grid(row=1, column=6, sticky=constants.W, padx=5)

        self.btnTwitchSkin = ttk.Button(
            master=frame2,
            image=self.icon_send,
            state=constants.DISABLED,
            command=lambda: self.genCommandSkin('chat')
        )
        self.btnTwitchSkin.grid(row=1, column=7, sticky=constants.W, padx=5)

        # Sombreros

        labelHats = ttk.Label(frame2, text='Sombrero')
        labelHats.grid(row=2, column=4, sticky=constants.W)

        self.setvar('hat', 'Tricornio')
        self.hatCombo = ttk.Combobox(
            frame2,
            values=self.hatsValues,
            state='readonly',
            textvariable='hat'
        )
        self.hatCombo.grid(row=2, column=5, sticky=constants.W, padx=5)

        self.btnCopyHat = ttk.Button(
            master=frame2,
            image=self.icon_copy,
            command=lambda: self.genCommandHat('copy')
        )
        self.btnCopyHat.grid(row=2, column=6, sticky=constants.W, padx=5)

        self.btnTwitchHat = ttk.Button(
            master=frame2,
            image=self.icon_send,
            state=constants.DISABLED,
            command=lambda: self.genCommandHat('chat')
        )
        self.btnTwitchHat.grid(row=2, column=7, sticky=constants.W, padx=5)

        # Pronunciación
        labelPron = ttk.Label(frame2, text='Pronunciación')
        labelPron.grid(row=3, column=4, sticky=constants.W)

        self.setvar('pronunciation', '')
        self.pronunciarEntry = ttk.Entry(
            master=frame2,
            textvariable='pronunciation',
        )
        self.pronunciarEntry.grid(row=3, column=5, padx=5, sticky=constants.W)

        self.btnCopyPron = ttk.Button(
            master=frame2,
            image=self.icon_copy,
            command=lambda: self.genCommandPron('copy')
        )
        self.btnCopyPron.grid(row=3, column=6, sticky=constants.W, padx=5)

        self.btnTwitchPron = ttk.Button(
            master=frame2,
            image=self.icon_send,
            state=constants.DISABLED,
            command=lambda: self.genCommandPron('chat')
        )
        self.btnTwitchPron.grid(row=3, column=7, sticky=constants.W, padx=5)

        # Fin

        # En estos arrays vamos a almacenar varios de los widgets
        # para poder usarlos más adelante
        self.anglesFrames = [self.angle1Frame, self.angle2Frame, self.angle3Frame]
        self.forcesFrames = [self.force1Frame, self.force2Frame, self.force3Frame]
        self.anglesWidgets = [self.angle1, self.angle2, self.angle3]
        self.shotForceWidgets = [self.force1, self.force2, self.force3]

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.mainloop()

    def update_value(self, value, name):
        index = int(name[-1]) - 1

        if name.startswith('action'):
            command = self.optsActions[value]
            self.setvar(name, command)

            if command == 's':
                self.anglesWidgets[index].configure(state=constants.NORMAL)
                self.shotForceWidgets[index].configure(
                    state=constants.NORMAL,
                    to=10,
                    value=1
                )
                self.setvar(f'force{index + 1}', 1)
                self.anglesFrames[index].grid(row=index + 2, column=1, sticky=constants.W, padx=10)
                self.forcesFrames[index].grid(row=index + 2, column=2, sticky=constants.W, padx=10)
            elif command == 'j':
                # self.anglesWidgets[index].configure(state=constants.DISABLED)
                self.anglesFrames[index].grid_forget()
                self.forcesFrames[index].grid(row=index + 2, column=2, sticky=constants.W, padx=10)
                self.shotForceWidgets[index].configure(
                    state=constants.NORMAL,
                    to=5,
                    value=1
                )
                self.setvar(f'force{index + 1}', 1)
            else:
                # self.anglesWidgets[index].configure(state=constants.DISABLED)
                # self.shotForceWidgets[index].configure(state=constants.DISABLED)
                self.anglesFrames[index].grid_forget()
                self.forcesFrames[index].grid_forget()

        else:
            self.setvar(name, f'{float(value):.0f}')

        self.genCommand()

    def genCommand(self):
        command = '!turn '
        totalActions = 0
        self.btnCopy.configure(state=constants.DISABLED)

        for i in range(0, 3):
            action = self.master.getvar(f'action{i+1}')
            angle = self.master.getvar(f'angle{i+1}')
            force = self.master.getvar(f'force{i+1}')

            command += self.master.getvar(f'action{i+1}')
            if action:
                totalActions += 1

            if action == 's':
                command += f'{angle}x{force}'

            if action == 'j':
                command += f'{force}'

            if i < 2:
                command += ' '

        if totalActions == 3:
            self.btnCopy.configure(state=constants.NORMAL)

        self.setvar('command', command)

    def genCommandHat(self, target):
        hat = self.getvar('hat').lower()
        self.setvar('commandConf', f'!hat {hat}')
        if target == 'copy':
            self.toClipboard(True)
        elif target == 'chat':
            self.toChat(True)

    def genCommandPron(self, target):
        pron = self.getvar('pronunciation')
        self.setvar('commandConf', f'!pronunciation {pron}')
        if target == 'copy':
            self.toClipboard(True)
        elif target == 'chat':
            self.toChat(True)

    def genCommandSkin(self, target):
        skin = self.skinsValues[self.getvar('skin')]
        self.setvar('commandConf', f'!skin {skin}')
        if target == 'copy':
            self.toClipboard(True)
        elif target == 'chat':
            self.toChat(True)

    def toClipboard(self, conf=False):
        self.clipboard_clear()
        if conf:
            self.clipboard_append(self.getvar('commandConf'))
        else:
            self.clipboard_append(self.getvar('command'))

    def connectTwitch(self):
        self.twitch, self.chat = asyncio.run(self.twitchCon.connectToChat())
        if not self.twitch:
            self.connectTwitch()

        if self.twitch == -1 and self.chat == -1:
            self.twitch = None
            self.chat = None
            return

        self.btnConTwitch.configure(state=constants.DISABLED)
        self.chat.register_event(ChatEvent.READY, self.on_ready)
        self.chat.start()

    async def on_ready(self, ready_event: EventData):
        print('Bot is ready for work, joining channels')
        await ready_event.chat.join_room(TARGET_CHANNEL)
        self.btnPlayTwitch.configure(state=constants.NORMAL)
        self.btnSendTwitch.configure(state=constants.NORMAL)
        self.btnTwitchHat.configure(state=constants.NORMAL)
        self.btnTwitchPron.configure(state=constants.NORMAL)
        self.btnTwitchSkin.configure(state=constants.NORMAL)

    def sendPlay(self):
        self.setvar('command', '!play')
        self.toChat()

    def toChat(self, conf=False):
        if conf:
            asyncio.run(self.twitchCon.sendCommand(self.chat, self.getvar('commandConf')))
        else:
            asyncio.run(self.twitchCon.sendCommand(self.chat, self.getvar('command')))

    def on_closing(self):
        if self.chat:
            self.chat.stop()
            asyncio.run(self.twitch.close())

        sys.exit()


def run():
    app = ttk.Window(
        title='Animal Brawl Helper',
        iconphoto=f'{LOCAL_DIR}/icon.png',
        resizable=[False, False]
    )
    TurnoGusano(app)
    asyncio.run(app.mainloop())
