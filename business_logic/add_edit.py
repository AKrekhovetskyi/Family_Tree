from typing import Any
from uuid import uuid4

from pyui import Ui_AddEdit

from .constructor import WindowConstructor
from .utils import remove_image_if_exists, select_image


class AddEdit(WindowConstructor):
    def __init__(self) -> None:
        super().__init__(Ui_AddEdit)

    def openEvent(self) -> None:
        super().openEvent()
        self.ui_window.comboBox_clan.addItems(self.workbook.sheetnames)
        self.fill_clans_and_members()
        self.refill_window()
        self.ui_window.comboBox_clan.currentIndexChanged.connect(
            self.fill_clans_and_members
        )

    def closeEvent(self, *args: Any) -> None:
        self.ui_window.comboBox_clan.disconnect()
        self.ui_window.comboBox_clan.clear()
        super().closeEvent(*args)

    def refill_window(self) -> None:
        row_index = self.ui_window.comboBox_addEdit.currentIndex()
        if row_index == 0:
            self.ui_window.lineEdit_lname.clear()
            self.ui_window.lineEdit_fname.clear()
            self.ui_window.lineEdit_patronymic.clear()
            self.ui_window.lineEdit_placeOfBirth.clear()
            self.ui_window.lineEdit_placeOfDeath.clear()
            self.ui_window.lineEdit_yearOfBirth.clear()
            self.ui_window.lineEdit_yearOfDeath.clear()
            self.ui_window.plainTextEdit_addinfo.clear()
            self.set_icon("Add_image.png")
        else:
            clan_index = self.ui_window.comboBox_clan.currentIndex()
            sheet = self.workbook[self.workbook.sheetnames[clan_index]]
            row = sheet[row_index]
            if row[5].value == "Чоловіча":
                self.ui_window.comboBox_sex.setItemText(0, "Чоловіча")
                self.ui_window.comboBox_sex.setItemText(1, "Жіноча")
            else:
                self.ui_window.comboBox_sex.setItemText(0, "Жіноча")
                self.ui_window.comboBox_sex.setItemText(1, "Чоловіча")

            self.ui_window.lineEdit_lname.setText(row[6].value)
            self.ui_window.lineEdit_fname.setText(row[7].value)
            self.ui_window.lineEdit_patronymic.setText(row[8].value)
            self.ui_window.lineEdit_yearOfBirth.setText(row[9].value)
            self.ui_window.lineEdit_yearOfDeath.setText(row[10].value)
            self.ui_window.lineEdit_placeOfBirth.setText(row[11].value)
            self.ui_window.lineEdit_placeOfDeath.setText(row[12].value)
            self.ui_window.plainTextEdit_addinfo.setPlainText(row[13].value)
            self.set_icon(row[0].value or "Add_image.png")

    def fill_clans_and_members(self) -> None:
        clan_name = self.ui_window.comboBox_clan.currentText()
        worksheet = self.workbook[clan_name]
        count = self.ui_window.comboBox_addEdit.count()

        if count > 1:
            self.ui_window.comboBox_addEdit.setCurrentIndex(0)
            for _ in range(1, count):
                self.ui_window.comboBox_addEdit.removeItem(1)
        if worksheet["B1"].value:
            for row_number in range(1, worksheet.max_row + 1):
                self.ui_window.comboBox_addEdit.insertItem(
                    row_number,
                    f"{worksheet[row_number][7].value} "
                    f"{worksheet[row_number][6].value}, "
                    f"{worksheet[row_number][9].value} р.н.",
                )

    def set_avatar(self) -> None:
        image_name = select_image()
        if image_name:
            clan_index = self.ui_window.comboBox_clan.currentIndex()
            worksheet = self.workbook[self.workbook.sheetnames[clan_index]]
            row_index = self.ui_window.comboBox_addEdit.currentIndex()

            if row_index == 0:  # If "Add" is selected.
                if not worksheet[worksheet.max_row][1].value:
                    row_index = worksheet.max_row
                else:
                    row_index = worksheet.max_row + 1
            remove_image_if_exists(worksheet[row_index][0].value)
            worksheet.cell(row_index, 1, image_name)
            self.set_icon(image_name)

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
            "family_name": " ",
        }
        clan_index = self.ui_window.comboBox_clan.currentIndex()
        worksheet = self.workbook[self.workbook.sheetnames[clan_index]]
        row_index = self.ui_window.comboBox_addEdit.currentIndex()

        if self.is_input_valid(family_member):
            if row_index == 0:  # If "Add" is selected.
                if not worksheet[worksheet.max_row][1].value:
                    row_index = worksheet.max_row
                else:
                    row_index = worksheet.max_row + 1

            del family_member["family_name"]
            for column, value in enumerate(family_member.values()):
                worksheet.cell(row_index, column + 6, value)

            if not worksheet.cell(row_index, 2).value:
                # Assign unique ID to member.
                worksheet.cell(row_index, 2, str(uuid4()))
            self.close()
