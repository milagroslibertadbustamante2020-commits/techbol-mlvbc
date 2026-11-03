# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'clave-secreta-techbol-mlvbc'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'techbol.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
