import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QComboBox
from PyQt6.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optica Shop")
        self.resize(800, 600)

        # Создание главного виджета и разметки
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Виджет для отображения чеков
        self.checks_widget = QWidget()
        self.checks_layout = QVBoxLayout(self.checks_widget)
        self.layout.addWidget(self.checks_widget)

        # Загрузка данных о чеках и их товарах
        self.load_data()

    def load_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="optica"
        )
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT id_cheque FROM cheque")
            checks = cursor.fetchall()

            for check_id, in checks:
                # Получение информации о товарах в чеке
                cursor.execute(f"SELECT o.name, pc.quantity, o.price, o.img_opt FROM optica o INNER JOIN position_cheque pc ON o.id_optica = pc.id_optica WHERE pc.id_cheque = {check_id}")
                products = cursor.fetchall()

                # Получение общего количества товаров и даты покупки для текущего чека
                cursor.execute(
                    f"SELECT COUNT(*), date_p FROM position_cheque WHERE id_cheque = {check_id} GROUP BY date_p")
                total_quantity, purchase_date = cursor.fetchone()

                # Вычисление общей суммы для текущего чека
                total_price = sum(product[2] * product[1] for product in products)

                # Виджет для отображения чека и его товаров
                check_widget = QWidget()
                check_layout = QVBoxLayout(check_widget)

                # Добавление заголовка с номером чека, общей суммой, общим количеством товаров и датой покупки
                check_info_label = QLabel(f"Номер чека: {check_id}, Общая сумма: {total_price}, Общее количество товаров: {total_quantity}, Дата покупки: {purchase_date}")
                check_layout.addWidget(check_info_label)

                # Перебор товаров в чеке
                for product_name, quantity, price, image in products:
                    # Виджет для отображения товара
                    product_widget = QWidget()
                    product_layout = QHBoxLayout(product_widget)

                    # Добавление информации о товаре
                    product_info_label = QLabel(f"{product_name}, Количество: {quantity}, Цена: {price}")
                    product_layout.addWidget(product_info_label)

                    # Добавление изображения товара
                    pixmap = QPixmap()
                    pixmap.loadFromData(image)
                    image_label = QLabel()
                    image_label.setPixmap(pixmap.scaledToWidth(100))
                    product_layout.addWidget(image_label)

                    check_layout.addWidget(product_widget)

                # Добавление виджета чека в главный виджет
                self.checks_layout.addWidget(check_widget)
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
