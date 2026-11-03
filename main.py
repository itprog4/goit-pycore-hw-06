import re
from collections import UserDict
from typing import Any


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        match = re.match(r'\d{10}', value)
        if not match:
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    def __eq__(self, other: Any):
        if isinstance(other, Phone):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return False

class Record:
    def __init__(self, _name: str):
        self.name = Name(_name)
        self.phones = list[Phone]()

    def add_phone(self, phone: str) -> None:
        if Phone(phone) in self.phones:
            return
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        counter: int = 0
        while counter < len(self.phones):
            if self.phones[counter].value == old_phone:
                self.phones[counter] = Phone(new_phone)
                return

    def find_phone(self, phone: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, _record: Record):
        self.data[_record.name.value] = _record

    def find(self, _name: str) -> Record | None:
        return self.data.get(_name)

    def delete(self, _name: str):
        if _name in self.data:
            del self.data[_name]

if __name__ == '__main__':
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333") # unsafe but keep it because this is the example code

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555") # unsafe but keep it because this is the example code
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
