from distutils.core import setup
import py2exe
import discord

setup(
    console=["bot.py"], # Укажите имя вашего файла с кодом бота
    options={
        'py2exe': {
            'packages': ['discord'],
            'bundle_files': 1,
            'optimize': 2,
            'compressed': True
        }
    },
    zipfile=None
)
