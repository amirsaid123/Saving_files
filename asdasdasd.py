import os

import openpyxl
from datetime import datetime


class Test1Results:
    # Class attribute for the deadline
    deadline = "2024-10-28 23:59:59"

    def __init__(self, student_id, file_path="test_1.xlsx"):
        """
        Initialize with the Excel file and student ID (ИСУ).

        :param file_path: path to the .xlsx file
        :param student_id: student ID (номер ИСУ)
        """
        try:
            self.file_path = file_path
            self.student_id = student_id
            self.data = self._load_data()  # метод для загрузки данных из файла

            student_data = next((item for item in self.data if item["ИСУ"] == self.student_id), None)
            if not student_data:
                raise ValueError(f"Student ID {self.student_id} not found in the file")
            # your code here
            # оценка студента с номером ИСУ student_id; это сумма баллов за все 20 вопросов
            # время сдачи теста студента с номером ИСУ student_id
            self.grade = student_data["grade"]
            self.timestamp = student_data["timestamp"]
        except FileNotFoundError:
            raise FileNotFoundError('Something wrong with a file(')
    def _load_data(self):
        """
        Load data from the Excel file using openpyxl.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found")

        data = []
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            fio, isu, timestamp_str, *grades = row
            total_grade = sum(grade for grade in grades if grade != None)
            # if timestamp_str is None:
            #     raise ValueError(f"Missing timestamp for student {isu}")
            if isu != None:
                data.append({
                    "ФИО": fio,
                    "ИСУ": isu,
                    "timestamp": self.str_to_timestamp(timestamp_str),
                    "grade": total_grade
                })
        # your code here
        # дока в помощь! https://openpyxl.readthedocs.io/en/stable/tutorial.html#loading-from-a-file
        # и ещё можно посмотреть вот на это https://www.geeksforgeeks.org/python-reading-excel-file-using-openpyxl-module/

        # data - это список словарей, каждый из которых выглядит следующим образом:
        # {"ФИО": str, "ИСУ": int,"timestamp": datetime.datetime, "grade": int}
        # для удобства метод конвертации строки в объект типа datetime.datetime реализован за вас как статический метод класса

        return data

    @staticmethod
    def str_to_timestamp(str_):
        if isinstance(str_, datetime):  # Проверяем, не является ли входное значение уже объектом datetime
            return str_
        return datetime.strptime(str_, "%Y-%m-%d %H:%M:%S")

    def is_late(self):
        deadline_datetime = self.str_to_timestamp(self.deadline)
        submission_datetime = self.timestamp

        return submission_datetime > deadline_datetime


# Пример использования
if __name__ == "__main__":
    test_results = Test1Results(465833, 'test_1.xlsx')  # попробуйте любой номер ИСУ из доступных в таблице

    print(f"Grade for student {test_results.student_id}: {test_results.grade}")

    is_late = test_results.is_late()
    print(f"Was the submission late? {'Yes' if is_late else 'No'}")


