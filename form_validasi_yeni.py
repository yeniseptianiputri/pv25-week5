import sys
import re
import csv
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QComboBox, QTextEdit
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt


class FormValidationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form Validasi - YENI SEPTIANI PUTRI (F1D022027)")
        self.setFixedSize(420, 650)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Masukkan nama lengkap")
        self.name_input.setEnabled(True)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Contoh: email@domain.com")
        self.email_input.setEnabled(True)

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Usia dalam angka, contoh: 22")
        self.age_input.setEnabled(True)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Contoh: +62 812 3456 7890")
        self.phone_input.setEnabled(True)

        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Tulis alamat lengkap di sini")
        self.address_input.setEnabled(True)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["-- Pilih Jenis Kelamin --", "Laki-laki", "Perempuan"])

        self.education_input = QComboBox()
        self.education_input.addItems([
            "-- Pilih Pendidikan --",
            "SMA",
            "S1 Teknik Informatika",
            "S2",
            "S3"
        ])

        layout.addWidget(QLabel("Nama:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Usia:"))
        layout.addWidget(self.age_input)
        layout.addWidget(QLabel("Nomor HP:"))
        layout.addWidget(self.phone_input)
        layout.addWidget(QLabel("Alamat:"))
        layout.addWidget(self.address_input)
        layout.addWidget(QLabel("Jenis Kelamin:"))
        layout.addWidget(self.gender_input)
        layout.addWidget(QLabel("Pendidikan:"))
        layout.addWidget(self.education_input)

        self.save_button = QPushButton("Simpan")
        self.save_button.clicked.connect(self.validate_and_save)

        self.clear_button = QPushButton("Hapus Semua Data")
        self.clear_button.clicked.connect(self.clear_csv)

        layout.addWidget(self.save_button)
        layout.addWidget(self.clear_button)

        info_label = QLabel("Dibuat oleh: YENI SEPTIANI PUTRI\nNIM: F1D022027")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()

    def validate_and_save(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        age = self.age_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.toPlainText().strip()
        gender = self.gender_input.currentText()
        education = self.education_input.currentText()

        if not name:
            self.show_warning("Nama wajib diisi.")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.show_warning("Format email tidak valid.")
            return
        if not age.isdigit():
            self.show_warning("Usia harus berupa angka.")
            return
        phone_digits = re.sub(r"[^\d]", "", phone)
        if len(phone_digits) < 10 or len(phone_digits) > 13:
            self.show_warning("Nomor HP harus 10-13 digit.")
            return
        if not address:
            self.show_warning("Alamat wajib diisi.")
            return
        if gender == "-- Pilih Jenis Kelamin --":
            self.show_warning("Pilih jenis kelamin.")
            return
        if education == "-- Pilih Pendidikan --":
            self.show_warning("Pilih pendidikan.")
            return

        self.save_to_csv([name, email, age, phone, address, gender, education])
        self.show_success("Data berhasil disimpan.")
        self.clear_fields()

    def save_to_csv(self, data):
        file_exists = os.path.isfile("data_pengguna.csv")
        with open("data_pengguna.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Nama", "Email", "Usia", "Nomor HP", "Alamat", "Jenis Kelamin", "Pendidikan"])
            writer.writerow(data)

    def clear_csv(self):
        confirm = QMessageBox.question(self, "Konfirmasi", "Yakin ingin menghapus semua data?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            open("data_pengguna.csv", "w").close()
            QMessageBox.information(self, "Sukses", "Semua data telah dihapus!")

    def show_warning(self, message):
        QMessageBox.warning(self, "Validasi Gagal", message)

    def show_success(self, message):
        QMessageBox.information(self, "Sukses", message)

    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.age_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.education_input.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormValidationApp()
    window.show()
    sys.exit(app.exec_())


