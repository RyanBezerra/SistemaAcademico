"""
Tela de Login
Sistema de autenticação para a aplicação
"""

import sys
import json
import hashlib
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFrame, QGridLayout, QSizePolicy, QMessageBox,
                             QCheckBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Signal
from PySide6.QtGui import QFont, QCursor
from ..core.database import db_manager

class LoginWindow(QMainWindow):
    # Sinal emitido quando o login é bem-sucedido
    login_successful = Signal(str)  # Emite o nome do usuário
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Centralizar janela
        self._center_window()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Criar layout da tela
        self._create_login_layout(main_layout)
        
        # Aplicar estilos
        self._apply_styles()
        
        # Testar conexão com banco de dados
        self._test_database_connection()
        
        # Configurar animações
        self._setup_animations()
        
    def _center_window(self):
        """Centraliza a janela na tela"""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
    
    def _create_login_layout(self, parent_layout):
        """Cria o layout principal da tela de login"""
        right_panel = self._create_right_panel()
        parent_layout.addStretch()
        parent_layout.addWidget(right_panel)
        parent_layout.addStretch()
    
    
    def _create_right_panel(self):
        """Cria o painel direito com o formulário de login"""
        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_panel.setMaximumWidth(520)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(60, 60, 60, 60)
        right_layout.setSpacing(30)
        right_layout.addStretch()
        
        # Container do formulário
        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(25)
        
        # Título do formulário
        form_title = QLabel("Bem-vindo de volta!")
        form_title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        form_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        form_layout.addWidget(form_title)
        
        # Subtítulo
        form_subtitle = QLabel("Faça login para acessar sua conta")
        form_subtitle.setFont(QFont("Segoe UI", 12))
        form_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        form_layout.addWidget(form_subtitle)
        
        # Campo de email/usuário
        email_container = QVBoxLayout()
        email_container.setSpacing(8)
        
        email_label = QLabel("Nome de Usuário")
        email_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        email_label.setStyleSheet("color: #2c3e50;")
        email_container.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu nome de usuário")
        self.email_input.setFont(QFont("Segoe UI", 12))
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #000000;
                outline: none;
            }
        """)
        email_container.addWidget(self.email_input)
        form_layout.addLayout(email_container)
        
        # Campo de senha
        password_container = QVBoxLayout()
        password_container.setSpacing(8)
        
        password_label = QLabel("Senha")
        password_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #2c3e50;")
        password_container.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Segoe UI", 12))
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #000000;
                outline: none;
            }
        """)
        password_container.addWidget(self.password_input)
        form_layout.addLayout(password_container)
        
        # Opções de login
        options_layout = QHBoxLayout()
        options_layout.setSpacing(0)
        
        # Checkbox "Lembrar-me"
        self.remember_checkbox = QCheckBox("Lembrar-me")
        self.remember_checkbox.setFont(QFont("Segoe UI", 10))
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #7f8c8d;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #000000;
                border-radius: 3px;
                background-color: #000000;
            }
        """)
        options_layout.addWidget(self.remember_checkbox)
        
        # Link "Esqueci minha senha"
        forgot_link = QLabel("<a href='#' style='color: #000000; text-decoration: none;'>Esqueci minha senha</a>")
        forgot_link.setFont(QFont("Segoe UI", 10))
        forgot_link.setAlignment(Qt.AlignmentFlag.AlignRight)
        forgot_link.setOpenExternalLinks(False)
        forgot_link.linkActivated.connect(self._show_forgot_password)
        options_layout.addWidget(forgot_link)
        
        form_layout.addLayout(options_layout)
        
        # Botão de login
        self.login_button = QPushButton("Entrar")
        self.login_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                padding: 14px;
                border: 2px solid #000000;
                border-radius: 8px;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #333333;
                border-color: #333333;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
                border-color: #1a1a1a;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                border-color: #cccccc;
                color: #666666;
            }
        """)
        self.login_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button.clicked.connect(self._attempt_login)
        form_layout.addWidget(self.login_button)
        
        # Divisor
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #ecf0f1;")
        form_layout.addWidget(divider)
        
        # Link para criar conta
        signup_container = QHBoxLayout()
        signup_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        signup_text = QLabel("Não tem uma conta?")
        signup_text.setFont(QFont("Segoe UI", 10))
        signup_text.setStyleSheet("color: #7f8c8d;")
        signup_container.addWidget(signup_text)
        
        signup_link = QLabel("<a href='#' style='color: #000000; text-decoration: none; font-weight: bold;'>Criar conta</a>")
        signup_link.setFont(QFont("Segoe UI", 10))
        signup_link.setOpenExternalLinks(False)
        signup_link.linkActivated.connect(self._show_signup)
        signup_container.addWidget(signup_link)
        
        form_layout.addLayout(signup_container)
        
        # Espaçador
        form_layout.addStretch()
        
        right_layout.addWidget(form_container)
        right_layout.addStretch()
        
        return right_panel
    
    def _apply_styles(self):
        """Aplica estilos globais com melhor portabilidade"""
        self.setStyleSheet("""
            /* Estilos globais da aplicação */
            QMainWindow {
                background: #ffffff !important;
                background-color: #ffffff !important;
                color: #1e293b;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Widget principal */
            QWidget {
                background: #ffffff !important;
            }
            
            QFrame#mainContainer {
                background: #ffffff !important;
                background-color: #ffffff !important;
            }
            
            QFrame#rightPanel {
                background: #ffffff !important;
                background-color: #ffffff !important;
            }
            
            QFrame#formContainer {
                background: #ffffff !important;
                background-color: #ffffff !important;
                border-radius: 0px;
            }
            
            /* Todos os QFrame devem ter background branco por padrão */
            QFrame {
                background: #ffffff !important;
                background-color: #ffffff !important;
            }
            
            /* Labels padrão */
            QLabel {
                color: #1e293b;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent !important;
            }
            
            /* Inputs padrão */
            QLineEdit, QTextEdit {
                font-family: 'Segoe UI', Arial, sans-serif;
                border-radius: 8px;
                padding: 8px 12px;
                background: #ffffff !important;
            }
            
            /* Comboboxes */
            QComboBox {
                font-family: 'Segoe UI', Arial, sans-serif;
                border-radius: 8px;
                padding: 8px 12px;
                background: #ffffff !important;
            }
            
            /* Botões padrão */
            QPushButton {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: 600;
                border-radius: 8px;
                padding: 8px 16px;
            }
        """)
    
    def _setup_animations(self):
        """Configura animações para a interface"""
        # Animação de fade para o botão de login
        self.login_animation = QPropertyAnimation(self.login_button, b"geometry")
        self.login_animation.setDuration(200)
        self.login_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
    
    def _test_database_connection(self):
        """Testa a conexão com o banco de dados"""
        if not db_manager.test_connection():
            self._show_error("Erro ao conectar com o banco de dados. Verifique sua conexão com a internet.")
            return False
        
        # Criar usuário padrão se não existir nenhum
        self._create_default_user_if_needed()
        return True
    
    def _create_default_user_if_needed(self):
        """Cria um usuário padrão se não existir nenhum usuário no banco"""
        users = db_manager.get_all_users()
        if not users:
            # Criar usuário administrador padrão
            success = db_manager.create_user(
                nome="admin",
                idade=25,
                senha="123456",
                nota=10.0
            )
            if success:
                print("Usuário administrador padrão criado (usuário: admin, senha: 123456)")
            else:
                print("Erro ao criar usuário administrador padrão")
    
    def _attempt_login(self):
        """Tenta fazer login com as credenciais fornecidas"""
        username = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self._show_error("Por favor, preencha todos os campos.")
            return
        
        # Desabilitar botão durante autenticação
        self.login_button.setEnabled(False)
        self.login_button.setText("Autenticando...")
        
        try:
            # Autenticar usuário no banco de dados
            user = db_manager.authenticate_user(username, password)
            
            if user:
                # Login bem-sucedido
                user_name = user['nome']
                self._show_success(f"Bem-vindo, {user_name}!")
                
                # Emitir sinal de sucesso com informações do usuário
                self.login_successful.emit(user_name)
                
                # Fechar janela de login
                self.close()
                return
            else:
                # Login falhou
                self._show_error("Nome de usuário ou senha incorretos.")
        
        except Exception as e:
            self._show_error(f"Erro ao conectar com o banco de dados: {str(e)}")
        
        finally:
            # Reabilitar botão
            self.login_button.setEnabled(True)
            self.login_button.setText("Entrar")
    
    def _show_error(self, message):
        """Mostra mensagem de erro"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erro de Login")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    def _show_success(self, message):
        """Mostra mensagem de sucesso"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Login Realizado")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    def _show_forgot_password(self):
        """Mostra diálogo para recuperação de senha"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Recuperar Senha")
        msg.setText("Para recuperar sua senha, entre em contato com o administrador do sistema.")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    def _show_signup(self):
        """Abre a tela de cadastro"""
        # Redirecionar para o sistema unificado de autenticação
        from auth_window import AuthWindow
        self.auth_window = AuthWindow()
        self.auth_window.signup_successful.connect(self._on_signup_success)
        self.auth_window.show()
    
    def _on_signup_success(self, user_name):
        """Chamado quando o cadastro é bem-sucedido"""
        # Fechar janela de autenticação
        if hasattr(self, 'auth_window'):
            self.auth_window.close()
        
        # Emitir sinal de login bem-sucedido
        self.login_successful.emit(user_name)
        
        # Fechar janela de login
        self.close()
    
    def keyPressEvent(self, event):
        """Permite login com Enter"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self._attempt_login()
        else:
            super().keyPressEvent(event)

def main():
    app = QApplication(sys.argv)
    
    # Criar e mostrar a janela de login
    login_window = LoginWindow()
    login_window.show()
    
    # Executar a aplicação
    sys.exit(app.exec())

if __name__ == '__main__':
    main()