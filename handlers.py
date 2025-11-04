#   handlers.py -->  #  all bot methods wrapped by @input_error

from objects import AddressBook, Record, Phone

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # show friendly, specific text when provided
            return str(e) if str(e) else "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."
    return inner


@input_error
def add_contact(args, book: AddressBook):
    # add [name] [phone]
    if len(args) != 2:                         # <-- validate BEFORE unpack
        raise ValueError("Give me name and phone please.")
    name, phone = args

    Phone(phone)                               # 10-digit validation

    record = book.find(name)
    msg = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        msg = "Contact added."
    if any(p.value == phone for p in record.phones):
        return "Phone already exists."
    record.add_phone(phone)
    return msg


@input_error
def change_contact(args, book: AddressBook):
    # change [name] [old_phone] [new_phone]
    if len(args) != 3:
        return "Give me name, old phone and new phone."
    name, old_phone, new_phone = args

    record = book.find(name)
    if record is None:
        raise KeyError

    old = record.find_phone(old_phone)
    if not old:
        return "Old phone not found for this contact."

    Phone(new_phone)                            # 10-digit validation

    if any(p.value == new_phone for p in record.phones):
        return "Phone already exists."

    old.value = new_phone                       # replace only first match
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    # phone [name]
    if not args:                                # <-- avoid unpack error
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    phones = ", ".join(p.value for p in record.phones) or "No phones"
    return f"{name}: {phones}"


@input_error
def show_all(args, book: AddressBook):
    # all
    if not book.data:
        return "No contacts found."
    return "\n".join(str(rec) for rec in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    # add-birthday [name] [DD.MM.YYYY]
    if len(args) != 2:                          # <-- validate BEFORE unpack
        raise ValueError("Give me name and birthday in format DD.MM.YYYY.")
    name, bday_str = args

    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)

    record.add_birthday(bday_str)               # raises ValueError on bad date
    return "Birthday set."


@input_error
def show_birthday(args, book: AddressBook):
    # show-birthday [name]
    if not args:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.birthday:
        return "Birthday not set."
    return f"{name}: {record.birthday}"


@input_error
def birthdays(args, book: AddressBook):
    # birthdays
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays within 7 days."
    grouped = {}
    for item in upcoming:
        grouped.setdefault(item["congratulation_date"], []).append(item["name"])
    lines = [f"{d}: {', '.join(names)}" for d, names in sorted(grouped.items())]
    return "\n".join(lines)

