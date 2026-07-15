from tkinter import messagebox as msbox
from typing import Any

from PyQt5 import QtCore, QtWidgets

from pyui import Ui_FamilyTies

from .constructor import WindowConstructor


class FamilyTies(WindowConstructor):
    def __init__(self) -> None:
        """
        All actions take place from the point of view of the person for whom
        the connections are made.
        """
        super().__init__(Ui_FamilyTies)

    def openEvent(self) -> None:
        super().openEvent()
        self.ui_window.comboBox_clan.addItems(self.workbook.sheetnames)
        self._reset_window()
        self.ui_window.comboBox_clan.currentIndexChanged.connect(self.reset_window)
        self.ui_window.comboBox_person.currentIndexChanged.connect(self.fill_window)

    def closeEvent(self, *args: Any) -> None:
        self.ui_window.comboBox_clan.disconnect()
        self.ui_window.comboBox_person.disconnect()
        self.ui_window.comboBox_clan.clear()
        self._clean_window()
        super().closeEvent(*args)

    def add_sibling_to_table(self, sibling: str | None = None) -> None:
        item = QtWidgets.QTableWidgetItem()
        rowCount = self.ui_window.tableWidget_siblings.rowCount()
        if not sibling:
            sibling = self.ui_window.comboBox_siblings.currentText()
        if sibling and not self.ui_window.tableWidget_siblings.findItems(
            sibling, QtCore.Qt.MatchFlag.MatchExactly
        ):
            self.ui_window.tableWidget_siblings.setRowCount(rowCount + 1)
            self.ui_window.tableWidget_siblings.setItem(rowCount, 0, item)
            item.setText(sibling)

    def _clean_window(self, *, with_person_box: bool = False) -> None:
        self.ui_window.comboBox_father.clear()
        self.ui_window.comboBox_mother.clear()
        self.ui_window.comboBox_partner.clear()
        self.ui_window.comboBox_siblings.clear()
        self.ui_window.tableWidget_siblings.clear()
        self.ui_window.tableWidget_siblings.setRowCount(0)
        if with_person_box:
            self.ui_window.comboBox_person.clear()

    def fill_window(self) -> None:
        clan_name = self.ui_window.comboBox_clan.currentText()
        worksheet = self.workbook[clan_name]
        person = self.ui_window.comboBox_person.currentText()

        if not person:
            self.reset_window()
        else:
            self._clean_window()
            name_by_id, data_of = {"": ""}, {}
            for row in worksheet.iter_rows(values_only=True):
                member = f"{row[7]} {row[6]}, {row[9]} р.н."
                name_by_id[row[1]] = member
                data_of[member] = row
            self.ui_window.comboBox_siblings.addItems(name_by_id.values())
            if partner_id := data_of[person][2]:
                self.ui_window.comboBox_partner.addItems(
                    {
                        partner_id: name_by_id[partner_id],
                        **name_by_id,
                    }.values()
                )
            else:
                self.ui_window.comboBox_partner.addItems(name_by_id.values())
            if father_id := data_of[person][3]:
                self.ui_window.comboBox_father.addItems(
                    {
                        father_id: name_by_id[father_id],
                        **name_by_id,
                    }.values()
                )
                for member, member_info in data_of.items():
                    if member != person and member_info[3] == father_id:
                        self.add_sibling_to_table(member)
            else:
                self.ui_window.comboBox_father.addItems(name_by_id.values())
            if mother_id := data_of[person][4]:
                self.ui_window.comboBox_mother.addItems(
                    {
                        mother_id: name_by_id[mother_id],
                        **name_by_id,
                    }.values()
                )
                for member, member_info in data_of.items():
                    if member != person and member_info[4] == mother_id:
                        self.add_sibling_to_table(member)
            else:
                self.ui_window.comboBox_mother.addItems(name_by_id.values())

    def _reset_window(self) -> None:
        clan_name = self.ui_window.comboBox_clan.currentText()
        worksheet = self.workbook[clan_name]
        self._clean_window(with_person_box=True)
        if worksheet.max_row == 1 and worksheet.max_column == 1:
            return None
        self.ui_window.comboBox_father.insertItem(0, "")
        self.ui_window.comboBox_mother.insertItem(0, "")
        self.ui_window.comboBox_person.insertItem(0, "")
        self.ui_window.comboBox_partner.insertItem(0, "")
        for row in range(1, worksheet.max_row + 1):
            args = (
                row,
                f"{worksheet[row][7].value} {worksheet[row][6].value}, "
                f"{worksheet[row][9].value} р.н.",
            )
            self.ui_window.comboBox_father.insertItem(*args)
            self.ui_window.comboBox_mother.insertItem(*args)
            self.ui_window.comboBox_person.insertItem(*args)
            self.ui_window.comboBox_partner.insertItem(*args)
            self.ui_window.comboBox_siblings.insertItem(*args)

    def reset_window(self) -> None:
        self.ui_window.comboBox_person.disconnect()
        self._reset_window()
        self.ui_window.comboBox_person.currentIndexChanged.connect(self.fill_window)

    def is_input_valid(self, family: dict[str, list[str]]) -> bool:
        members = [member for group in family.values() for member in group if member]
        if not family["person"][0]:
            msbox.showerror("Помилка!", "Оберіть, для кого створити зв'язки.")
            return False
        if len(members) != len(set(members)):
            msbox.showerror("Помилка!", "Деякі члени сім'ї повторюються.")
            return False
        father, mother = family["father"][0], family["mother"][0]
        for parent in (father, mother):
            if not parent:
                continue
            for member in members:
                if member in {father, mother}:
                    continue
                age_of_parent = int(parent.split(", ")[1].split()[0])
                age_of_member = int(member.split(", ")[1].split()[0])
                if age_of_parent > age_of_member:
                    msbox.showwarning(
                        "Увага!", "Батьки повинні бути старші за нащадків."
                    )
                    return False
        return True

    def save(self) -> None:
        person = self.ui_window.comboBox_person.currentText()
        father = self.ui_window.comboBox_father.currentText()
        mother = self.ui_window.comboBox_mother.currentText()
        partner = self.ui_window.comboBox_partner.currentText()
        siblings_rowCount = self.ui_window.tableWidget_siblings.rowCount()
        siblings = (
            [
                self.ui_window.tableWidget_siblings.item(row, 0).text()
                for row in range(siblings_rowCount)
            ]
            if siblings_rowCount > 0
            else []
        )
        if not self.is_input_valid(
            {
                "person": [person],
                "father": [father],
                "mother": [mother],
                "partner": [partner],
                "siblings": siblings,
            }
        ):
            return None

        # Generate mapping of "member - row number".
        clan_name = self.ui_window.comboBox_clan.currentText()
        ws, row_of = self.workbook[clan_name], {}
        for row_number, row in enumerate(ws.iter_rows(values_only=True)):
            for member in [person, father, mother, partner, *siblings]:
                if member == f"{row[7]} {row[6]}, {row[9]} р.н.":
                    row_of[member] = row_number + 1

        if father:
            if mother:  # Cross-assignment of partner IDs for parents.
                ws.cell(row_of[father], 3, ws[row_of[mother]][1].value)
                ws.cell(row_of[mother], 3, ws[row_of[father]][1].value)
            # Assign father's ID to person.
            ws.cell(row_of[person], 4, ws[row_of[father]][1].value)
            for sibling in siblings:  # Assign father's ID to siblings.
                ws.cell(row_of[sibling], 4, ws[row_of[father]][1].value)
        if mother:  # Assign mother's ID to person.
            ws.cell(row_of[person], 5, ws[row_of[mother]][1].value)
            for sibling in siblings:  # Assign mother's ID to siblings.
                ws.cell(row_of[sibling], 5, ws[row_of[mother]][1].value)
        if partner:  # Cross-assignment of partner IDs.
            ws.cell(row_of[person], 3, ws[row_of[partner]][1].value)
            ws.cell(row_of[partner], 3, ws[row_of[person]][1].value)
        self.close()
