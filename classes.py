from collections import UserDict
from datetime import datetime
import pickle


class Field:
    """Field class"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)




class Name(Field):
    """Name class"""
    @property
    def value(self):
        """Return the value"""
        return self.__value

    @value.setter
    def value(self, value):
        if not value:
            raise ValueError("Give me a name")
        self.__value = value


class Phone(Field):
    """Phone class"""
    @property
    def value(self):
        """Return the value"""
        return self.__value

    @value.setter
    def value(self, value):
        if value and not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain 10 digits.")
        self.__value = value


class Birthday(Field):
    """Birthday class"""

    @property
    def value(self):
        """Return the value"""
        return self.__value

    @value.setter
    def value(self, value):
        try:
            if isinstance(value, str):
                self.__value = datetime.strptime(value, '%d-%m-%Y')
            else:
                self.__value = value
        except ValueError:
            raise ValueError('Invalid birthday format. Try "dd-mm-yyyy"')



class Record:
    """Record class"""
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        """Days to birthday"""
        if self.birthday is None:
            return None
        today = datetime.now()
        birthday_this_year = self.birthday.value.replace(today.year)
        if today < birthday_this_year:
            return (birthday_this_year - today).days
        return (birthday_this_year.replace(today.year + 1) - today).days

    def add_phone(self, phone):
        """Add phone"""
        phones_list = [p.value for p in self.phones]
        if phone not in phones_list:
            self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Remove phone"""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """Edit phone"""
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = Phone(new_phone)
                return
        raise ValueError

    def find_phone(self, phone):
        """Find phone"""
        for i in self.phones:
            if i.value == phone:
                return i
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)


class AddressBook(UserDict):
    """Address Book"""

    def add_record(self, record):
        """New record in Address Book"""
        self.data[record.name.value] = record

    def find(self, name):
        """Find record data in Address Book"""
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        """Delete record from Address Book"""
        if name in self.data:
            del self.data[name]

    def iterator(self, value):
        count = 0

        while count < len(self.data):
            yield list(self.data.values())[count: count + value]
            count += value

    def saving(self, filename):
        """Save Address Book"""
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def loading(self, filename):
        """Load Address Book"""
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)

    def search(self, value):
        """Search value in Address Book"""
        result = []
        for record in self.data.values():
            if value.lower() in record.name.value.lower():
                result.append(record)
            else:
                for phone in record.phones:
                    if value in phone.value:
                        result.append(record)
        return result

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)
