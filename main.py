from collections import UserDict


class Field:
    # Зберігаємо значення поля
    def __init__(self, value):
        self.value = value

    # Повертаємо текстове представлення поля
    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        # Ім’я не може бути порожнім або містити лише пробіли
        if not value.strip():
            raise ValueError("Ім’я не може бути порожнім")

        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        # Телефон має містити рівно 10 цифр
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Номер має містити рівно 10 цифр")

        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        # Створюємо перевірений телефон і додаємо до списку
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def find_phone(self, phone):
        # Шукаємо телефон за його значенням
        for saved_phone in self.phones:
            if saved_phone.value == phone:
                return saved_phone

        return None

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)

        if found_phone is not None:
            self.phones.remove(found_phone)

    def edit_phone(self, old_phone, new_phone):
        found_phone = self.find_phone(old_phone)

        if found_phone is None:
            raise ValueError("Старий номер не знайдено")

        # Спочатку перевіряємо новий номер
        checked_phone = Phone(new_phone)

        # Змінюємо старий номер лише після успішної перевірки
        found_phone.value = checked_phone.value

    def __str__(self):
        phone_numbers = []

        for phone in self.phones:
            phone_numbers.append(phone.value)

        phones_text = "; ".join(phone_numbers)
        return f"Contact name: {self.name.value}, phones: {phones_text}"


class AddressBook(UserDict):
    def add_record(self, record):
        # Ключ — ім’я, значення — весь об’єкт контакту
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        records_text = []

        for record in self.data.values():
            records_text.append(str(record))

        return "\n".join(records_text)


# Приклад використання запускається лише при запуску цього файлу
if __name__ == "__main__":
    book = AddressBook()

    # Створюємо перший контакт із двома телефонами
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    # Створюємо другий контакт
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print("Усі контакти:")
    print(book)

    # Знаходимо контакт і редагуємо його телефон
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print("\nПісля редагування:")
    print(john)

    # Шукаємо конкретний телефон
    found_phone = john.find_phone("5555555555")
    print(f"\nЗнайдений телефон: {john.name}: {found_phone}")

    # Видаляємо телефон із контакту
    john.remove_phone("5555555555")

    print("\nПісля видалення телефону:")
    print(john)

    # Видаляємо контакт із книги
    book.delete("Jane")

    print("\nПісля видалення Jane:")
    print(book)

    print("\nПеревірка неправильного номера:")

    try:
        john.edit_phone("1112223333", "123")
    except ValueError as error:
        print(f"Помилка: {error}")

    print("Контакт після спроби:")
    print(john)