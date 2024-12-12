import sys
import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGroupBox, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QIcon


class New_Window(QWidget):  # Новое окно с информацией
    def __init__(self, name_place):
        self.place = name_place
        super().__init__()
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        useful_cards = cursor.execute(f"""SELECT cards.place, new_windows.UI_File, new_windows.html_linkText FROM new_windows
                                        LEFT JOIN cards
                                            ON cards.window_id = new_windows.id
                                        WHERE cards.place = '{self.place}'""")
        for place, UI_File, html_link in useful_cards:
            uic.loadUi(UI_File, self)
            self.setWindowTitle(self.place)
            self.setMinimumSize(604, 457)
            self.setMaximumSize(604, 457)
            self.link.setText(f"<a href=\"{html_link}\">Яндекс Карта: {place}</a>")
            self.link.setOpenExternalLinks(True)
            self.textEdit.setReadOnly(True)
        connection.close()
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/main.ui', self)

        # Словарь для стран
        self.countries = {1: "Россия",
                     2: "Германия",
                     3: "Франция",
                     4: "Италия",
                     5: "Испания",
                     6: "Греция",
                     7: "Норвегия",
                     8: "Швейцария",
                     9: "Япония"}

        # Имя базы данных
        self.database = "my_database.db"

        # Пополняю выбор в ComboBox
        self.choose_country.addItem(QIcon('Иконки/travel.png'), 'Все')
        self.choose_country.addItem(QIcon('Иконки/russia.png'), 'Россия')
        self.choose_country.addItem(QIcon('Иконки/germany.png'), 'Германия')
        self.choose_country.addItem(QIcon('Иконки/france.png'), 'Франция')
        self.choose_country.addItem(QIcon('Иконки/italy.png'), 'Италия')
        self.choose_country.addItem(QIcon('Иконки/spanish.png'), 'Испания')
        self.choose_country.addItem(QIcon('Иконки/greece.png'), 'Греция')
        self.choose_country.addItem(QIcon('Иконки/norway.png'), 'Норвегия')
        self.choose_country.addItem(QIcon('Иконки/switzerland.png'), 'Швейцария')
        self.choose_country.addItem(QIcon('Иконки/japan.png'), 'Япония')

        # Подключаем ComboBox
        self.choose_country.activated.connect(self.change_country)

        # Подключение кнопок переключения
        self.next.clicked.connect(self.next_page)
        self.back.clicked.connect(self.back_page)

        # Layout для каждой страницы
        i = 0
        while i <= 8:
            i += 1
            exec("self.for_page{} = QGridLayout()".format(i))

        # Цикл создание карточек
        widgets = 0
        pages = 1
        row = 0
        column = 0
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        useful_cards = cursor.execute("""SELECT countries.country, cards.place, cards.picture
                                                FROM cards
                                                INNER JOIN countries
                                                ON countries.id = cards.country_id;""")
        self.layout_for_page = QGridLayout()
        self.layout_for_page.setColumnStretch(1, 0)
        for country, place, picture in useful_cards:
            self.key = QGroupBox(country)
            layout = QVBoxLayout()
            self.btn_pic = QPushButton('', self)
            self.btn_pic.setStyleSheet("width : 200;"
                                        "height : 200;"
                                        "border-image : url({});".format(str(picture)))
            layout.addWidget(self.btn_pic)
            self.btn_click = QPushButton(str(place), self)
            self.btn_click.clicked.connect(self.open_window)
            layout.addWidget(self.btn_click)
            self.key.setLayout(layout)
            if column <= 2:
                self.layout_for_page.addWidget(self.key, row, column)
                column += 1
                widgets += 1
            else:
                row += 1
                column = 0
                self.layout_for_page.addWidget(self.key, row, column)
                column += 1
                widgets += 1
            if widgets == 6 and pages == 1:  # Заполнение 1 страницы
                row = 0
                column = 0
                for i in range(0, self.layout_for_page.count()):
                    gb = self.layout_for_page.itemAt(i).widget()
                    if column <= 2:
                        self.for_page1.addWidget(gb, row, column)
                        column += 1
                    else:
                        row += 1
                        column = 0
                        self.for_page1.addWidget(gb, row, column)
                        column += 1
                self.page.setLayout(self.for_page1)
                self.layout_for_page = QGridLayout()
                pages += 1
                widgets = 0
            elif widgets == 6 and pages == 2:  # Заполнение 2 страницы
                row = 0
                column = 0
                for i in range(0, self.layout_for_page.count()):
                    gb = self.layout_for_page.itemAt(i).widget()
                    if column <= 2:
                        self.for_page2.addWidget(gb, row, column)
                        column += 1
                    else:
                        row += 1
                        column = 0
                        self.for_page2.addWidget(gb, row, column)
                        column += 1
                self.page_2.setLayout(self.for_page2)
                self.layout_for_page = QGridLayout()
                pages += 1
                widgets = 0
            elif widgets == 6 and pages == 3:  # Заполнение 3 страницы
                row = 0
                column = 0
                for i in range(0, self.layout_for_page.count()):
                    gb = self.layout_for_page.itemAt(i).widget()
                    if column <= 2:
                        self.for_page3.addWidget(gb, row, column)
                        column += 1
                    else:
                        row += 1
                        column = 0
                        self.for_page3.addWidget(gb, row, column)
                        column += 1
                self.page_3.setLayout(self.for_page3)
                self.layout_for_page = QGridLayout()
                pages += 1
                widgets = 0
            elif widgets == 6 and pages == 4:  # Заполнение 4 страницы
                row = 0
                column = 0
                for i in range(0, self.layout_for_page.count()):
                    gb = self.layout_for_page.itemAt(i).widget()
                    if column <= 2:
                        self.for_page4.addWidget(gb, row, column)
                        column += 1
                    else:
                        row += 1
                        column = 0
                        self.for_page4.addWidget(gb, row, column)
                        column += 1
                self.page_4.setLayout(self.for_page4)
                self.layout_for_page = QGridLayout()
                pages += 1
                widgets = 0
            elif widgets == 6 and pages == 5:  # Заполнение 5 страницы
                row = 0
                column = 0
                for i in range(0, self.layout_for_page.count()):
                    gb = self.layout_for_page.itemAt(i).widget()
                    if column <= 2:
                        self.for_page5.addWidget(gb, row, column)
                        column += 1
                    else:
                        row += 1
                        column = 0
                        self.for_page5.addWidget(gb, row, column)
                        column += 1
                self.page_5.setLayout(self.for_page5)
                self.layout_for_page = QGridLayout()
                pages += 1
                widgets = 0
            elif widgets == 6 and pages == 6:   # Заполнение 6 страницы
                row = 0
                column = 0
                for i in range(0, self.layout_for_page.count()):
                    gb = self.layout_for_page.itemAt(i).widget()
                    if column <= 2:
                        self.for_page6.addWidget(gb, row, column)
                        column += 1
                    else:
                        row += 1
                        column = 0
                        self.for_page6.addWidget(gb, row, column)
                        column += 1
                self.page_6.setLayout(self.for_page6)
                self.layout_for_page = QGridLayout()
                pages += 1
                widgets = 0
            elif widgets == 6 and pages == 7:   # Заполнение 7 страницы
                row = 0
                column = 0
                for i in range(0, self.layout_for_page.count()):
                    gb = self.layout_for_page.itemAt(i).widget()
                    if column <= 2:
                        self.for_page7.addWidget(gb, row, column)
                        column += 1
                    else:
                        row += 1
                        column = 0
                        self.for_page7.addWidget(gb, row, column)
                        column += 1
                self.page_7.setLayout(self.for_page7)
                self.layout_for_page = QGridLayout()
                pages += 1
                widgets = 0
            elif widgets <= 6 and pages == 8:   # Заполнение 8 страницы
                self.page_8.setLayout(self.layout_for_page)
                pages += 1
                widgets = 0

        connection.close()

    # Функционал кнопки переключения вперёд
    def next_page(self):
        if self.choose_country.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)
        else:
            self.stackedWidget.setCurrentIndex(0)

    # Функционал кнопки переключения назад
    def back_page(self):
        if self.choose_country.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() - 1)
        else:
            self.stackedWidget.setCurrentIndex(0)

    # Настройка фильтра
    def change_country(self):
        index = self.choose_country.currentIndex()
        if index == 0:
            self.stackedWidget.setCurrentIndex(0)
            for i in range(self.for_page1.count()):
                gb = self.for_page1.itemAt(i).widget()
                gb.deleteLater()
            for i in range(self.for_page2.count()):
                gb = self.for_page2.itemAt(i).widget()
                gb.deleteLater()
            for i in range(self.for_page3.count()):
                gb = self.for_page3.itemAt(i).widget()
                gb.deleteLater()
            for i in range(self.for_page4.count()):
                gb = self.for_page4.itemAt(i).widget()
                gb.deleteLater()
            for i in range(self.for_page5.count()):
                gb = self.for_page5.itemAt(i).widget()
                gb.deleteLater()
            for i in range(self.for_page6.count()):
                gb = self.for_page6.itemAt(i).widget()
                gb.deleteLater()
            for i in range(self.for_page7.count()):
                gb = self.for_page7.itemAt(i).widget()
                gb.deleteLater()
            for i in range(self.for_page8.count()):
                gb = self.for_page8.itemAt(i).widget()
                gb.deleteLater()
            # Цикл создание Боксов
            widgets = 0
            pages = 1
            row = 0
            column = 0
            connection = sqlite3.connect('my_database.db')
            cursor = connection.cursor()
            useful_cards = cursor.execute("""SELECT countries.country, cards.place, cards.picture
                                                            FROM cards
                                                            INNER JOIN countries
                                                            ON countries.id = cards.country_id;""")
            self.layout_for_page = QGridLayout()
            self.layout_for_page.setColumnStretch(1, 0)
            for country, place, picture in useful_cards:
                self.key = QGroupBox(country)
                layout = QVBoxLayout()
                self.btn_pic = QPushButton('', self)
                self.btn_pic.setStyleSheet("width : 200;"
                                           "height : 200;"
                                           "border-image : url({});".format(str(picture)))
                layout.addWidget(self.btn_pic)
                self.btn_click = QPushButton(str(place), self)
                self.btn_click.clicked.connect(self.open_window)
                layout.addWidget(self.btn_click)
                self.key.setLayout(layout)
                if column <= 2:
                    self.layout_for_page.addWidget(self.key, row, column)
                    column += 1
                    widgets += 1
                else:
                    row += 1
                    column = 0
                    self.layout_for_page.addWidget(self.key, row, column)
                    column += 1
                    widgets += 1
                if widgets == 6 and pages == 1:  # Заполнение 1 страницы
                    row = 0
                    column = 0
                    for i in range(0, self.layout_for_page.count()):
                        gb = self.layout_for_page.itemAt(i).widget()
                        if column <= 2:
                            self.for_page1.addWidget(gb, row, column)
                            column += 1
                        else:
                            row += 1
                            column = 0
                            self.for_page1.addWidget(gb, row, column)
                            column += 1
                    self.page.setLayout(self.for_page1)
                    self.layout_for_page = QGridLayout()
                    pages += 1
                    widgets = 0
                elif widgets == 6 and pages == 2:  # Заполнение 2 страницы
                    row = 0
                    column = 0
                    for i in range(0, self.layout_for_page.count()):
                        gb = self.layout_for_page.itemAt(i).widget()
                        if column <= 2:
                            self.for_page2.addWidget(gb, row, column)
                            column += 1
                        else:
                            row += 1
                            column = 0
                            self.for_page2.addWidget(gb, row, column)
                            column += 1
                    self.page_2.setLayout(self.for_page2)
                    self.layout_for_page = QGridLayout()
                    pages += 1
                    widgets = 0
                elif widgets == 6 and pages == 3:  # Заполнение 3 страницы
                    row = 0
                    column = 0
                    for i in range(0, self.layout_for_page.count()):
                        gb = self.layout_for_page.itemAt(i).widget()
                        if column <= 2:
                            self.for_page3.addWidget(gb, row, column)
                            column += 1
                        else:
                            row += 1
                            column = 0
                            self.for_page3.addWidget(gb, row, column)
                            column += 1
                    self.page_3.setLayout(self.for_page3)
                    self.layout_for_page = QGridLayout()
                    pages += 1
                    widgets = 0
                elif widgets == 6 and pages == 4:  # Заполнение 4 страницы
                    row = 0
                    column = 0
                    for i in range(0, self.layout_for_page.count()):
                        gb = self.layout_for_page.itemAt(i).widget()
                        if column <= 2:
                            self.for_page4.addWidget(gb, row, column)
                            column += 1
                        else:
                            row += 1
                            column = 0
                            self.for_page4.addWidget(gb, row, column)
                            column += 1
                    self.page_4.setLayout(self.for_page4)
                    self.layout_for_page = QGridLayout()
                    pages += 1
                    widgets = 0
                elif widgets == 6 and pages == 5:  # Заполнение 5 страницы
                    row = 0
                    column = 0
                    for i in range(0, self.layout_for_page.count()):
                        gb = self.layout_for_page.itemAt(i).widget()
                        if column <= 2:
                            self.for_page5.addWidget(gb, row, column)
                            column += 1
                        else:
                            row += 1
                            column = 0
                            self.for_page5.addWidget(gb, row, column)
                            column += 1
                    self.page_5.setLayout(self.for_page5)
                    self.layout_for_page = QGridLayout()
                    pages += 1
                    widgets = 0
                elif widgets == 6 and pages == 6:  # Заполнение 6 страницы
                    row = 0
                    column = 0
                    for i in range(0, self.layout_for_page.count()):
                        gb = self.layout_for_page.itemAt(i).widget()
                        if column <= 2:
                            self.for_page6.addWidget(gb, row, column)
                            column += 1
                        else:
                            row += 1
                            column = 0
                            self.for_page6.addWidget(gb, row, column)
                            column += 1
                    self.page_6.setLayout(self.for_page6)
                    self.layout_for_page = QGridLayout()
                    pages += 1
                    widgets = 0
                elif widgets == 6 and pages == 7:  # Заполнение 7 страницы
                    row = 0
                    column = 0
                    for i in range(0, self.layout_for_page.count()):
                        gb = self.layout_for_page.itemAt(i).widget()
                        if column <= 2:
                            self.for_page7.addWidget(gb, row, column)
                            column += 1
                        else:
                            row += 1
                            column = 0
                            self.for_page7.addWidget(gb, row, column)
                            column += 1
                    self.page_7.setLayout(self.for_page7)
                    self.layout_for_page = QGridLayout()
                    pages += 1
                    widgets = 0
                elif widgets <= 6 and pages == 8:  # Заполнение 8 страницы
                    self.page_8.setLayout(self.layout_for_page)
                    pages += 1
                    widgets = 0

            connection.close()
        else:
            self.stackedWidget.setCurrentIndex(0)
            for i in range(self.for_page1.count()):
                gb = self.for_page1.itemAt(i).widget()
                gb.deleteLater()
            row = 0
            column = 0
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()
            useful_cards = cursor.execute(f"""SELECT countries.country, cards.place, cards.picture
                                                FROM cards
                                                INNER JOIN countries
                                                ON countries.id = cards.country_id
                                                WHERE countries.country='{self.countries[index]}';""")
            self.layout_for_page = QGridLayout()
            self.layout_for_page.setColumnStretch(1, 0)
            for country, place, picture in useful_cards:
                self.key = QGroupBox(country)
                layout = QVBoxLayout()
                self.btn_pic = QPushButton('', self)
                self.btn_pic.setStyleSheet("width : 200;"
                                           "height : 200;"
                                           "border-image : url({});".format(str(picture)))
                layout.addWidget(self.btn_pic)
                self.btn_click = QPushButton(str(place), self)
                self.btn_click.clicked.connect(self.open_window)
                layout.addWidget(self.btn_click)
                self.key.setLayout(layout)
                if column <= 2:
                    self.for_page1.addWidget(self.key, row, column)
                    column += 1
                else:
                    row += 1
                    column = 0
                    self.for_page1.addWidget(self.key, row, column)
                    column += 1
                self.page.setLayout(self.for_page1)

    # Функция открытия окон
    def open_window(self):
        self.btn_clickName = self.sender().text()
        self.win = New_Window(self.btn_clickName)
        self.win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())