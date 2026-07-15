from typing import Any

from PyQt5 import QtWidgets

from pyui import Ui_Review

from .constructor import WindowConstructor


class Review(WindowConstructor):
    def __init__(self) -> None:
        super().__init__(Ui_Review)

    def openEvent(self) -> None:
        super().openEvent()
        self.ui_window.comboBox_clan.addItems(self.workbook.sheetnames)
        self.fill_table()
        self.ui_window.comboBox_clan.currentIndexChanged.connect(self.fill_table)

    def closeEvent(self, *args: Any) -> None:
        self.ui_window.comboBox_clan.disconnect()
        self.ui_window.comboBox_clan.clear()
        super().closeEvent(*args)

    def fill_table(self) -> None:
        clan_name = self.ui_window.comboBox_clan.currentText()
        worksheet = self.workbook[clan_name]
        self.ui_window.tableWidget.clearContents()
        self.ui_window.tableWidget.setRowCount(0)
        self.ui_window.tableWidget.setRowCount(worksheet.max_row)
        self.ui_window.tableWidget.setColumnCount(9)  # Sex - Additional info.

        for row_n, row in enumerate(
            worksheet.iter_rows(min_col=6, max_col=14, values_only=True)
        ):
            for column_n, cell in enumerate(row):
                item = QtWidgets.QTableWidgetItem()
                item.setText(cell)
                self.ui_window.tableWidget.setItem(row_n, column_n, item)
