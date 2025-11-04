#   Field, Name, Phone, Birthday, Record, AddressBook Classes

from collections import UserDict
from datetime import datetime, date, timedelta

# Base field
class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

# Required name field
class Name(Field):
    pass

# Phone with 10-digit validation
class Phone(Field):
    def __init__(self, value: str):
        value = str(value)
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone must be 10 digits")
        super().__init__(value)

# Birthday stored as date, input format DD.MM.YYYY
class Birthday(Field):
    def __init__(self, value: str):
        try:
            d = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(d)
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

# Contact record with phones and optional birthday
class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def find_phone(self, value: str):
        return next((p for p in self.phones if p.value == value), None)

    def remove_phone(self, value: str) -> bool:
        p = self.find_phone(value)
        if p:
            self.phones.remove(p)
            return True
        return False

    def edit_phone(self, old: str, new: str) -> bool:
        p = self.find_phone(old)
        if not p:
            return False
        p.value = Phone(new).value
        return True

    def add_birthday(self, bday_str: str):
        self.birthday = Birthday(bday_str)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) or "—"
        bday = str(self.birthday) if self.birthday else "—"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {bday}"

# Addressbook class added
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        return self.data.pop(name, None) is not None

    # Return upcoming birthdays for next 7 days
    def get_upcoming_birthdays(self) -> list[dict]:
        today = date.today()
        end = today + timedelta(days=7)
        result = []

        for rec in self.data.values():
            if not rec.birthday:
                continue
            dob: date = rec.birthday.value

            # Align birthday to this/next year; handle Feb 29
            def mk(y: int) -> date:
                try:
                    return dob.replace(year=y)
                except ValueError:
                    return date(y, 3, 1)

            bday = mk(today.year)
            if bday < today:
                bday = mk(today.year + 1)

            if today <= bday <= end:
                wd = bday.weekday()  # 0=Mon..6=Sun
                if wd >= 5:          # shift weekend to Monday
                    bday += timedelta(days=7 - wd)
                result.append({
                    "name": rec.name.value,
                    "congratulation_date": bday.strftime("%d.%m.%Y"),
                })

        return result
