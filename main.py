import json
from datetime import datetime

class PhoneBook:
    def __init__(self, file_path: str):
        """ Инициализация объекта PhoneBook."""
        self.file_path = file_path
        self.contacts = self.load_data()

    def load_data(self) -> list:
        """Загрузка данных из файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            self.save_data([])  # Если файл не найден, создаем его
            return []

    def save_data(self, data: list):
        """Сохранение данных в файл."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def display_contacts(self, page_size=5):
        """Вывод контактов на экран постранично."""
        for i, contact in enumerate(self.contacts, start=1):
            print(i)
            self.display_contact_details(contact)

            if i % page_size == 0 or i == len(self.contacts):
                input("Нажмите Enter для продолжения...")

    @staticmethod
    def display_contact_details(contact: dict):
        """Вывод подробной информации о контакте."""
        print(f"ФИО: {contact['Фамилия']} {contact['Имя']} {contact['Отчество']}")
        print(f"Организация: {contact['Организация']}")
        print(f"Рабочий телефон: {contact['Рабочий телефон']}")
        print(f"Личный телефон: {contact['Личный телефон']}")
        print(f"Обновление: {contact.get('Обновлен', 'Не обновлялся')}")
        print()

    def add_contact(self):
        """ Добавление нового контакта.
        - last_name (str): Фамилия.
        - first_name (str): Имя.
        - middle_name (str): Отчество.
        - organization (str): Организация.
        - work_phone (str): Рабочий телефон.
        - personal_phone (str): Личный телефон."""

        last_name = input("Введите фамилию: ")
        first_name = input("Введите имя: ")
        middle_name = input("Введите отчество: ")
        organization = input("Введите название организации: ")
        work_phone = input("Введите рабочий телефон: ")
        personal_phone = input("Введите личный телефон: ")
        contact = {'Фамилия': last_name, 'Имя': first_name, 'Отчество': middle_name,
                   'Организация': organization, 'Рабочий телефон': work_phone, 'Личный телефон': personal_phone}
        self.contacts.append(contact)
        self.save_data(self.contacts)
        print("Контакт успешно добавлен.")

    @staticmethod
    def get_list():
        print('Список полей справочника:')
        print('Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон', sep=', ')

    def edit_contact(self, index):
        """Редактирование информации о контакте."""

        self.get_list()
        field = input("Введите поле из списка для редактирования: ").capitalize()
        if index <= 0 or index > len(self.contacts) or field not in self.contacts[index - 1]:
            print("Неверный индекс или такого поля нет. Начните сначала.")
        elif 1 <= index <= len(self.contacts) and field in self.contacts[index - 1]:
            new_value = input(f"Введите новое значение для {field}: ")
            self.contacts[index - 1][field] = new_value
            data = datetime.now()
            self.contacts[index - 1]['Обновлен'] = data.strftime('%d/%m/%Y %H:%M')
            self.save_data(self.contacts)
            print("Контакт успешно обновлен.")

    def search_contacts(self):
        """Поиск контактов по заданным критериям."""
        self.get_list()
        field = input("Введите поле из списка для поиска: ").capitalize()
        value = input(f"Введите значение для поиска по полю {field}: ")
        results = []
        for contact in self.contacts:
            match = contact.get(field) == value
            if match:
                results.append(contact)
        print("\nРезультаты поиска:")
        if results:
            for i, contact in enumerate(results, start=1):
                self.display_contact_details(contact)
        else:
            print('Нет данных')
        input("Нажмите Enter для продолжения...")


def main():
    phone_book = PhoneBook("phone_book_data.json")

    while True:
        print("\nМеню телефонного справочника:")
        print("1. Показать контакты")
        print("2. Добавить контакт")
        print("3. Редактировать контакт")
        print("4. Поиск контактов")
        print("5. Выйти")

        choice = input("Введите ваш выбор (1-5): ")

        if choice == "1":
            phone_book.display_contacts()
        elif choice == "2":
            phone_book.add_contact()
        elif choice == "3":
            try:
                index = int(input(f"Введите номер контакта для редактирования : "))
                phone_book.edit_contact(index)
            except ValueError:
                print('Зрачение должно быть числом')

        elif choice == "4":
            phone_book.search_contacts()
        elif choice == "5":
            print("Выход из телефонного справочника. До свидания!")
            break
        else:
            print("Неверный выбор. Введите число от 1 до 5.")


if __name__ == "__main__":
    main()
