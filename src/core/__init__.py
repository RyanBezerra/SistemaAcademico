"""
Sistema - Core Module
Módulo principal com lógica de negócio e gerenciamento da aplicação
"""

from .app import MainApp, AppManager
from .database import DatabaseManager, db_manager

__all__ = ['MainApp', 'AppManager', 'DatabaseManager', 'db_manager']
