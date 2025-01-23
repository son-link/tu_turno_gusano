import certifi
from cx_Freeze import Executable, setup

build_options = {
    'packages': ['certifi'],
    'include_files': [(certifi.where(), 'cacert.pem'), ('turno_gusano/theme.json', 'theme.json')],
    'excludes': []
}

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", None, None, "Animal Brawl Helper (nombre temporal), es una pequeña aplicación que genera un comando para Twitch para jugar a un juego para Twitch y que actualmente está en desarrollo", "IconId", None),
    ],
    "Icon": [
        ("IconId", "abh/icon.ico"),
    ],
}

bdist_msi_options = {
    "add_to_path": True,
    "data": msi_data,
}

build_exe_options = {
    'packages': ['certifi'],
    'include_files': [(certifi.where(), 'cacert.pem'), ('abh/theme.json', 'theme.json')],
    'excludes': [],
    "include_msvcr": True
}

executables = [
    Executable(
        "animal-brawl-helper.py",
        copyright="Copyright (C) 2024-2025 Alfonso Saavedra 'Son Link'",
        base="gui",
        icon="abh/icon.png",  # Cambiar a .ico en Windows
        shortcut_name="Animal Brawl Helper",
        shortcut_dir="MyProgramMenu",
    )
]

setup(
    name="Animal Brawl Helper",
    version="0.2.0",
    description="Animal Brawl Helper es una pequeña aplicación que genera un comando para Twitch para jugar a un juego para Twitch, Animal Brawl, y que actualmente está en desarrollo.",
    executables=executables,
    requires=['requests'],
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
)
