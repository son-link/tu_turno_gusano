import ttkbootstrap as ttk
import tkinter as tk
import os
import pathlib


def getAppDataDir():
    """Return the O.S. default user appdata dir"""

    path = ''
    if os.getenv('HOME'):
        path = os.getenv('HOME')  # Linux
    elif os.getenv('APPDATA'):
        path = os.getenv('APPDATA')  # Windows

    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return path


CONFIG_DIR = getAppDataDir()
CONFIG_FILE = os.path.join(CONFIG_DIR, '.animal_brawl_helper.cfg')


def PasswdModal(parent):
    password = ttk.StringVar()

    def __checkPass():
        if password.get():
            modal.destroy()

    modal = tk.Toplevel(parent)
    # modal.geometry('128x128')
    modal.title('Iniciando sesión en Twitch')
    data_file_exists = os.path.isfile(CONFIG_FILE)

    frame = ttk.Frame(modal, padding=5)
    frame.pack(expand=True)

    label = ttk.Label(frame, text='Introduce la contraseña:')
    label.pack(expand=True, pady=5)

    passwdEntry = ttk.Entry(frame, show='*', textvariable=password)
    passwdEntry.pack(expand=True, pady=5)

    if not data_file_exists:
        label2 = ttk.Label(frame, text='Esta contraseña sirve para encriptar los datos de acceso a Twitch. Guárdala en un sitio seguro')
        label2.pack(expand=True, pady=5)

    btn = ttk.Button(
        frame,
        text='Aceptar',
        command=__checkPass)
    btn.pack(expand=True, pady=5)

    modal.wait_window()

    return password.get()


def checkTokens():
    return os.path.isfile(CONFIG_FILE)
