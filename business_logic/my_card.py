from os.path import join as join_path
from uuid import uuid4

from PyQt5 import QtGui, QtWidgets

from pyui import Ui_MyCard

from .constructor import WindowConstructor
from .utils import remove_image_if_exists, select_image


class MyCard(WindowConstructor):
    def __init__(self, pushButton_myCard: QtWidgets.QPushButton) -> None:
        super().__init__(Ui_MyCard)
        self.pushButton_mainWindow = pushButton_myCard

    def openEvent(self) -> None:
        super().openEvent()
        self.worksheet = self.workbook.active
        self.fill_window()

    def fill_window(self) -> None:
        # Check for the existence of information in the first line.
        if self.worksheet["B1"].value:
            self.ui_window.lineEdit_clanName.setText(self.worksheet.title)
            if image_path := self.worksheet["A1"].value:
                self.set_icon(image_path)
            if self.worksheet["F1"].value == "Чоловіча":
                self.ui_window.comboBox_sex.setItemText(0, "Чоловіча")
            else:
                self.ui_window.comboBox_sex.setItemText(0, "Жіноча")
                self.ui_window.comboBox_sex.setItemText(1, "Чоловіча")

            self.ui_window.lineEdit_lname.setText(self.worksheet["G1"].value)
            self.ui_window.lineEdit_fname.setText(self.worksheet["H1"].value)
            self.ui_window.lineEdit_patronymic.setText(self.worksheet["I1"].value)
            self.ui_window.lineEdit_yearOfBirth.setText(self.worksheet["J1"].value)
            self.ui_window.lineEdit_yearOfDeath.setText(self.worksheet["K1"].value)
            self.ui_window.lineEdit_placeOfBirth.setText(self.worksheet["L1"].value)
            self.ui_window.lineEdit_placeOfDeath.setText(self.worksheet["M1"].value)
            self.ui_window.plainTextEdit_addinfo.setPlainText(
                self.worksheet["N1"].value
            )

    def set_avatar(self) -> None:
        image_name = select_image()
        if image_name:
            remove_image_if_exists(self.worksheet["A1"].value)
            self.worksheet["A1"] = image_name
            self.set_icon(image_name)

    def set_my_card_button_label(self) -> None:
        self.pushButton_mainWindow.setText(
            f"Рід: {self.worksheet.title}\n"
            + f"{self.worksheet['H1'].value} {self.worksheet['G1'].value}"
        )
        if image_name := self.worksheet["A1"].value:
            icon1 = QtGui.QIcon()
            icon1.addPixmap(
                QtGui.QPixmap(join_path("avatars", image_name)),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off,
            )
            self.pushButton_mainWindow.setIcon(icon1)

    def save(self) -> None:
        family_member = {  # Order matters.
            "sex": self.ui_window.comboBox_sex.currentText().strip(),
            "last_name": self.ui_window.lineEdit_lname.text().strip(),
            "first_name": self.ui_window.lineEdit_fname.text().strip(),
            "patronymic": self.ui_window.lineEdit_patronymic.text().strip(),
            "year_of_birth": self.ui_window.lineEdit_yearOfBirth.text().strip(),
            "year_of_death": self.ui_window.lineEdit_yearOfDeath.text().strip(),
            "place_of_birth": self.ui_window.lineEdit_placeOfBirth.text().strip(),
            "place_of_death": self.ui_window.lineEdit_placeOfDeath.text().strip(),
            "add_info": self.ui_window.plainTextEdit_addinfo.toPlainText().strip()
            or " ",
            "family_name": self.ui_window.lineEdit_clanName.text().strip(),
        }

        if self.is_input_valid(family_member):
            self.worksheet.title = family_member["family_name"]
            del family_member["family_name"]
            for column, value in enumerate(family_member.values()):
                self.worksheet.cell(row=1, column=column + 6, value=value)

            if not self.worksheet["B1"].value:
                # Assign unique ID to the member.
                self.worksheet["B1"] = str(uuid4())

            self.set_my_card_button_label()
            self.close()
