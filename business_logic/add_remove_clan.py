from re import search
from tkinter import messagebox as msbox

from pyui import Ui_AddRemoveClan

from .constructor import WindowConstructor


class AddRemoveClan(WindowConstructor):
    def __init__(self) -> None:
        super().__init__(Ui_AddRemoveClan)

    def openEvent(self) -> None:
        super().openEvent()
        self.fill_clan_names()

    def fill_clan_names(self) -> None:
        self.ui_window.lineEdit_addClan.clear()
        self.ui_window.comboBox_RemoveClan.clear()
        self.ui_window.comboBox_RemoveClan.insertItem(0, "")
        self.ui_window.comboBox_RemoveClan.insertItems(1, self.workbook.sheetnames)

    def save(self) -> None:
        clan_name = self.ui_window.lineEdit_addClan.text()
        clan_to_remove = self.ui_window.comboBox_RemoveClan.currentText()

        if clan_name:
            if search(r"[:\/\*\?[\]<>|]", clan_name):
                msbox.showerror(
                    "Помилка!",
                    "Заборонено вводити такі символи: / \ * ? [ ] < > : |",
                )
                return
            else:
                self.workbook.create_sheet(clan_name)
        if clan_to_remove:
            if len(self.workbook.sheetnames) == 1:
                msbox.showerror("Помилка!", "Неможливо видалити єдиний рід!")
                return
            else:
                del self.workbook[clan_to_remove]
                msbox.showinfo(message=f'Рід "{clan_to_remove}" видалено!')
        self.close()
