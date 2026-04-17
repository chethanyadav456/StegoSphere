import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.utils import formataddr
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QLineEdit, 
                            QTabWidget, QWidget, QVBoxLayout, QMessageBox, QHBoxLayout, QFrame)
from PyQt6.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from lsb import hide_text_in_image, extract_text_from_image
import os
import config

class SteganographyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StegoSphere")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)  # Set minimum size to allow resizing
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
                background: #1e1e1e;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #2d2d2d;
                color: #ffffff;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #0d47a1;
                color: white;
                border-bottom-color: #1e1e1e;
            }
            QPushButton {
                background-color: #0d47a1;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #404040;
                border-radius: 4px;
                background: #333333;
                color: #ffffff;
                font-size: 13px;
                min-height: 20px;
                selection-background-color: #0d47a1;
                selection-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #0d47a1;
            }
            QLineEdit::placeholder {
                color: #888888;
            }
            QLabel {
                color: #ffffff;
                font-size: 13px;
                padding-bottom: 2px;
            }
            QFrame {
                background-color: transparent;
                border-radius: 5px;
                padding: 10px;
            }
            /* Media Query for 1920x1080 */
            @media screen and (min-width: 1920px) {
                QMainWindow {
                    min-width: 1200px;
                    min-height: 800px;
                }
                QTabWidget::pane {
                    padding: 20px;
                }
                QTabBar::tab {
                    padding: 15px 30px;
                    font-size: 14px;
                }
                QPushButton {
                    padding: 12px 25px;
                    font-size: 14px;
                }
                QLineEdit {
                    padding: 12px;
                    font-size: 14px;
                }
                QLabel {
                    font-size: 14px;
                }
            }
        """)

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.enc_tab = QWidget()
        self.dec_tab = QWidget()

        self.tabs.addTab(self.enc_tab, "Encrypt")
        self.tabs.addTab(self.dec_tab, "Decrypt")

        self.init_encrypt_tab()
        self.init_decrypt_tab()

    def init_encrypt_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Image preview section
        preview_frame = QFrame()
        preview_layout = QVBoxLayout()
        preview_frame.setLayout(preview_layout)
        
        self.image_preview_enc = QLabel()
        self.image_preview_enc.setMinimumSize(500, 300)
        self.image_preview_enc.setMaximumHeight(350)
        self.image_preview_enc.setScaledContents(False)
        self.image_preview_enc.setStyleSheet("""
            QLabel {
                border: 2px dashed #404040;
                border-radius: 5px;
                background-color: #1e1e1e;
            }
        """)
        self.image_preview_enc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview_enc.setText("No image selected")
        
        self.label = QLabel("No file selected")
        self.label.setStyleSheet("color: #888888;")
        
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogOpenButton))
        self.upload_button.clicked.connect(self.upload_file)

        preview_layout.addWidget(self.image_preview_enc)
        preview_layout.addWidget(self.label)
        preview_layout.addWidget(self.upload_button)
        preview_layout.setSpacing(10)
        layout.addWidget(preview_frame)

        # Input section
        input_frame = QFrame()
        input_layout = QVBoxLayout()
        input_frame.setLayout(input_layout)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter text to hide")
        self.text_input.setMinimumHeight(40)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        
        self.receiver_email = QLineEdit()
        self.receiver_email.setPlaceholderText("Enter receiver's email")
        self.receiver_email.setMinimumHeight(40)

        text_label = QLabel("Text to Hide:")
        input_layout.addWidget(text_label)
        input_layout.addWidget(self.text_input)
        
        password_label = QLabel("Password:")
        input_layout.addWidget(password_label)
        input_layout.addWidget(self.password_input)
        
        receiver_label = QLabel("Receiver Email:")
        input_layout.addWidget(receiver_label)
        input_layout.addWidget(self.receiver_email)
        
        layout.addWidget(input_frame)

        # Encrypt button
        self.encrypt_button = QPushButton("Encrypt & Send Email")
        self.encrypt_button.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogApplyButton))
        self.encrypt_button.clicked.connect(self.encrypt_and_send)
        layout.addWidget(self.encrypt_button)

        self.enc_tab.setLayout(layout)

    def init_decrypt_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Image preview section
        preview_frame = QFrame()
        preview_layout = QVBoxLayout()
        preview_frame.setLayout(preview_layout)
        
        self.image_preview_dec = QLabel()
        self.image_preview_dec.setMinimumSize(500, 300)
        self.image_preview_dec.setMaximumHeight(350)
        self.image_preview_dec.setScaledContents(False)
        self.image_preview_dec.setStyleSheet("""
            QLabel {
                border: 2px dashed #404040;
                border-radius: 5px;
                background-color: #1e1e1e;
            }
        """)
        self.image_preview_dec.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview_dec.setText("No image selected")
        
        self.image_label_dec = QLabel("No file selected")
        self.image_label_dec.setStyleSheet("color: #888888;")
        
        self.upload_button_dec = QPushButton("Upload Steganographed Image")
        self.upload_button_dec.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogOpenButton))
        self.upload_button_dec.clicked.connect(self.upload_image_dec)
        
        preview_layout.addWidget(self.image_preview_dec)
        preview_layout.addWidget(self.image_label_dec)
        preview_layout.addWidget(self.upload_button_dec)
        layout.addWidget(preview_frame)

        # Password input section
        input_frame = QFrame()
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)
        input_frame.setLayout(input_layout)
        
        self.password_input_dec = QLineEdit()
        self.password_input_dec.setPlaceholderText("Enter password")
        self.password_input_dec.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input_dec.setMinimumHeight(40)
        
        password_label_dec = QLabel("Password:")
        input_layout.addWidget(password_label_dec)
        input_layout.addWidget(self.password_input_dec)
        layout.addWidget(input_frame)

        # Decrypt button
        self.decrypt_button = QPushButton("Extract Text")
        self.decrypt_button.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogApplyButton))
        self.decrypt_button.clicked.connect(self.decrypt_and_extract)
        layout.addWidget(self.decrypt_button)

        # Extracted text section
        result_frame = QFrame()
        result_layout = QVBoxLayout()
        result_frame.setLayout(result_layout)
        
        self.extracted_text_label = QLabel("Extracted Text: ")
        self.extracted_text_label.setWordWrap(True)
        self.extracted_text_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                background-color: #1e1e1e;
                border-radius: 5px;
            }
        """)
        
        result_layout.addWidget(QLabel("Result:"))
        result_layout.addWidget(self.extracted_text_label)
        layout.addWidget(result_frame)

        self.dec_tab.setLayout(layout)

    def upload_file(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if self.image_path:
            self.label.setText(f"Selected: {os.path.basename(self.image_path)}")
            pixmap = QPixmap(self.image_path)
            scaled_pixmap = pixmap.scaled(self.image_preview_enc.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_preview_enc.setPixmap(scaled_pixmap)

    def upload_image_dec(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image_path_dec = file_path
            self.image_label_dec.setText(f"Selected: {os.path.basename(file_path)}")
            pixmap = QPixmap(self.image_path_dec)
            scaled_pixmap = pixmap.scaled(self.image_preview_dec.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_preview_dec.setPixmap(scaled_pixmap)

    def encrypt_and_send(self):
        if not hasattr(self, 'image_path') or not self.text_input.text() or not self.password_input.text():
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        text_to_hide = self.text_input.text()
        password = self.password_input.text()

        output_image = "steganographed_image.png"
        
        try:
            hide_text_in_image(self.image_path, text_to_hide, password, output_image)
            self.send_email(output_image, password)
            QMessageBox.information(self, "Success", "Encryption and Email Sent Successfully! ✅")
        except ValueError as ve:
             QMessageBox.critical(self, "Error", f"Steganography failed: {str(ve)}")
        except Exception as e:
             QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def decrypt_and_extract(self):
        password = self.password_input_dec.text()

        if not password or not hasattr(self, "image_path_dec"):
            QMessageBox.warning(self, "Input Error", "Please provide all inputs!")
            return

        extracted_text = extract_text_from_image(self.image_path_dec, password)
        self.extracted_text_label.setText(f"Extracted Text: {extracted_text}")
        QMessageBox.information(self, "Success", "Text Extracted Successfully! ✅")

    def send_email(self, file_path, decryption_key):
        try:
            # Get email addresses from config and input
            sender = config.SENDER_EMAIL.strip()
            sender_pass = config.SENDER_PASSWORD.strip()
            receiver = self.receiver_email.text().strip().encode('ascii', 'ignore').decode('ascii')

            if not config.has_email_credentials():
                QMessageBox.warning(
                    self,
                    "Configuration Error",
                    "Missing email configuration. Set STEGOSPHERE_SENDER_EMAIL and "
                    "STEGOSPHERE_SENDER_PASSWORD before using email delivery.",
                )
                return
            
            if not receiver:
                QMessageBox.warning(self, "Input Error", "Please enter receiver's email!")
                return

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "StegoSphere Image & Decryption Key"

            # Create plain text body
            body = f"Decryption Key: {decryption_key}\nUse the correct password to extract hidden text."
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # Attach the file
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(file_path)}"')
                msg.attach(part)

            # Send email
            with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
                server.login(sender, sender_pass)
                server.sendmail(sender, receiver, msg.as_string())

            QMessageBox.information(self, "Success", "Email Sent Successfully! ✅")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Email sending failed: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = SteganographyApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
