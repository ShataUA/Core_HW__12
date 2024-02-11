from classes import Record, AddressBook
import os

"""CLI_Bot"""


def input_error(func):
    """Decorator returns input error"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Invalid user name or user name not found"
        except ValueError:
            return "Give me name and phone(phones) please"
        except IndexError:
            return "User name or phone is already exists"
    return inner


@input_error
def hello_func():
    """Returns greeting"""
    return "How can I help you?"


@input_error
def add_func(address_book, command):
    """Add a new contact"""
    _, name, phone = command.split()
    if name and phone:
        record = address_book.find(name)
        if record:
            record.add_phone(phone)
            return f"Contact {name.capitalize()} add phone {phone}"
        else:
            record = Record(name)
            record.add_phone(phone)
            address_book.add_record(record)
            return f"Contact {name.capitalize()}: phone {phone}"
    raise ValueError


@input_error
def change_func(address_book, command):
    """Change a current contact"""
    _, name, phone, new_phone = command.split()
    if name and phone and new_phone:
        record = address_book.find(name)
        if record:
            record.edit_phone(phone, new_phone)
            return f"Phone number {phone} for {name.capitalize()} changed to {new_phone}"
    raise ValueError if address_book.find(name) else KeyError


@input_error
def show_phone(address_book, command):
    """Show a current contact's phone number"""
    _, name = command.split()
    record = address_book.find(name)
    if record:
        return record
    raise KeyError


@input_error
def remove_phone(address_book, command):
    """Remove a current contact's phone number"""
    _, name, phone = command.split()
    if name and phone:
        record = address_book.find(name)
        if record:
            record.remove_phone(phone)
            return f"Phone number {phone} for {name.capitalize()} removed"
    raise KeyError


def show_all(address_book):
    """Show all contacts if it possible"""
    if not address_book.data:
        return "No users available"
    return "\n".join(str(record) for record in address_book.data.values())


@input_error
def delete_contact(address_book, command):
    """Delete a current contact"""
    _, name = command.split()
    record = address_book.find(name)
    if record:
        address_book.delete(name)
        return f"Contact {name.capitalize()} deleted"
    raise KeyError


@input_error
def search_by(address_book, command):
    """Search by string"""
    _, value = command.split()
    search_result = address_book.search(value)
    if search_result:
        return "\n".join(str(record) for record in search_result)
    raise ValueError


# @input_error
# def days_to_birthday(address_book, command):
#     """Days to birthday"""
#     _, name = command.split()
#     record = address_book.find(name)
#     if record:
#         # add_birthday =
#         return (f'Contact {name.capitalize()} birthday is {record.birthday}, '
#                 f'there are {record.days_to_birthday()} days to next birthday' if record.days_to_birthday() else
#                 f'Unknown birthday for contact {name.capitalize()}')
#     raise KeyError


def main():
    """Main function"""
    address_book = AddressBook()
    if os.path.exists('address_book.pkl'):
        address_book.loading('address_book.pkl')
    while True:
        command = input("Enter command: ").lower().strip()
        if command in ["good bye", "close", "exit", "stop", "."]:
            address_book.saving('address_book.pkl')
            print("Good bye!")
            break
        if command in ["hello", "hi"]:
            print(hello_func())
        elif command.startswith("add "):
            print(add_func(address_book, command))
        elif command.startswith("change "):
            print(change_func(address_book, command))
        elif command.startswith("phone "):
            print(show_phone(address_book, command))
        elif command == "show all":
            print(show_all(address_book))
        elif command.startswith('remove '):
            print(remove_phone(address_book, command))
        elif command.startswith('delete '):
            print(delete_contact(address_book, command))
        elif command.startswith('search '):
            print(search_by(address_book, command))
        # elif command.startswith('birthday '):
        #     print(days_to_birthday(address_book, command))
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
