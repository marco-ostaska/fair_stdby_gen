from enum import Enum

class DefinedHours():
    allowed = 0
    week = 0
    weekend = 0
    holiday = 0


class WeekDays(Enum):
    SATURDAY = {"sat": 0, "saturday": 0}
    SUNDAY = {"sun": 1, "sunday": 1}
    MONDAY = {"mon": 2, "monday": 2}
    TUESDAY = {"tue": 3, "tuesday": 3}
    WEDNESDAY = {"wed": 4, "wednesday": 4}
    THURSDAY = {"thu": 5, "thursday": 5}
    FRIDAY = {"fri": 6, "friday": 6}

class WorkdayValidator:
    def __init__(self, required_days: list[int], restricted_days: list[int]):
        self.required_days = required_days
        self.restricted_days = restricted_days

    def is_required(self, day) -> bool:
        return day in self.required_days

    def is_restricted(self, day) -> bool:
        return day in self.restricted_days

class HoursCalculator():
    worked_hours = 0
    hours = 0

    def __init__(self, allowed):
        self.allowed = allowed

    def add_worked_hours(self):
        self.worked_hours += self.hours

class Workday(WorkdayValidator, HoursCalculator):

    def worked_days(self) -> int:
        return self.worked_hours / self.hours

class Holidays(Workday):
    def __init__(self, days):
        self.days = days
        self.hours = DefinedHours.holiday

    def is_on(self, day):
        return day in self.days

class Weeks(Workday):

    def __init__(self, restricted_weekdays):
        self.restricted_weekdays = restricted_weekdays
        self.hours = DefinedHours.week

    def is_restricted(self, week_day) -> bool:
        return week_day[:3].lower() in [day[:3].lower() for day in self.restricted_weekdays]

class Weekends(Workday):

    def __init__(self, first_weekend):
        self.first_weekend = first_weekend
        self.hours = DefinedHours.weekend

    def is_on_first(self, weekday, onduty_person):
        return self.first_weekend[weekday] == onduty_person

class Person(Workday):
    """
    attributes:
        name: str
        required_days: list[int]
        restricted_days: list[int]
        restricted_weekdays: list[str]
        holidays: list[int]
        fisrt_weekend: dict
    """

    def __init__(self, name: str, required_days: list[int],restricted_days: list[int],
                 restricted_weekdays: list[str], holidays: list[int], fisrt_weekend: dict):
        super().__init__(required_days, restricted_days)
        self.name = name
        self.holiday = Holidays(holidays)
        self.week = Weeks(restricted_weekdays)
        self.weekend = Weekends(fisrt_weekend)

    def worked_hours(self) -> int:
        return self.week.worked_hours + self.weekend.worked_hours + self.holiday.worked_hours

    def worked_days(self) -> int:
        return self.week.worked_days() + self.weekend.worked_days() + self.holiday.worked_days()


def set_defined_hours(yml_dict):
    DefinedHours.allowed = yml_dict["hours"]["allowed"]
    DefinedHours.holiday = yml_dict["hours"]["holiday"]
    DefinedHours.week = yml_dict["hours"]["week"]
    DefinedHours.weekend  = yml_dict["hours"]["weekend"]



