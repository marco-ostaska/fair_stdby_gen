import calendar
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from monthinfo import monthinfo


@dataclass()
class PreDefinedHours:
    allowed: int
    week: int
    weekend: int
    holiday: int


@dataclass()
class WorkDayCalculator(object):
    hours_to_compute: int
    worked_hours: int = 0

    def add_worked_hours(self) -> int:
        self.worked_hours += self.hours_to_compute

    @property
    def worked_days(self) -> int:
        return self.worked_hours / self.hours_to_compute

@dataclass()
class Holidays:
    days: int
    calc: WorkDayCalculator

# @dataclass()
# class WorkDaySetter:
#     pass

# @dataclass()
# class WorkDayGetter:
#     pass


@dataclass()
class Weekends:
    first_weekend: dict
    calc: WorkDayCalculator

    def is_on_first(self, weekday:str, onduty_person:str) -> bool:
        return self.first_weekend[weekday.lower()] == onduty_person

@dataclass()
class Weeks:
    calc: WorkDayCalculator
    restricted_days: list[str]

    def is_restricted(self, weekday: str) -> bool:
        return weekday.lower()[:3] in [str(day[:3]).lower() for day in self.restricted_days]


@dataclass()
class WorkdayValidator:
    required_days: list[int]
    restricted_days: list[int]
    holidays: Holidays
    weekends: Weekends


    def is_required(self, day: int) -> bool:
        return day in self.required_days

    def is_restricted(self, day: int) -> bool:
        return day in self.restricted_days

    def is_holiday(self, day: int) -> bool:
        return day in self.holidays.days


@dataclass()
class Person:
    name: str
    validator: WorkdayValidator
    week: Weeks
    weekend: Weekends
    holiday: Holidays
    defined_hours: PreDefinedHours
    worked_hours: int = 0

    def add_worked_hours(self) -> int:
       return self.week.calc.worked_hours + self.weekend.calc.worked_hours + self.holiday.calc.worked_hours

    @property
    def worked_days(self) -> int:
        return self.week.calc.worked_days + self.weekend.calc.worked_days + self.holiday.calc.worked_days


def process_name_and_weekend(name: str, first_weekend: dict) -> tuple:
    return name.title(), {"saturday": str(first_weekend["saturday"]).title(), "sunday": str(first_weekend["sunday"]).title()}


def create_person_from_data(data: dict, defined_hours: PreDefinedHours, first_weekend: dict) -> Person:
    """Create a Person object based on the given  data and defined hours."""
    name, first_weekend = process_name_and_weekend(data["name"], first_weekend)
    holidays = Holidays(days=data["holidays"],
                        calc=WorkDayCalculator(defined_hours.holiday))
    week = Weeks(restricted_days=data["restricted_weekdays"],
                 calc=WorkDayCalculator(defined_hours.week))
    weekend = Weekends(first_weekend=first_weekend,
                       calc=WorkDayCalculator(defined_hours.weekend))
    validator = WorkdayValidator(
        required_days=data["required_days"], restricted_days=data["restricted_days"], holidays=holidays, weekends=weekend)
    return Person(name=name, validator=validator, week=week, weekend=weekend, holiday=holidays, defined_hours=defined_hours)


def new_person_list_from_yml(yml_dict: dict) -> list[Person]:
    """Create a list of Person objects based on the given YAML dictionary."""
    h = yml_dict["hours"]
    defined_hours = PreDefinedHours(
        allowed=h["allowed"], week=h["week"], weekend=h["weekend"], holiday=h["holiday"])
    people_list = []
    for person_data in yml_dict["person"]:
        person = create_person_from_data(
            person_data, defined_hours, yml_dict["first_weekend"])
        people_list.append(person)
    return people_list


@dataclass()
class AgendaSetter:
    person: list[Person]
    current_month: monthinfo.CurrentMonth
    calendar: Optional[list[list[str]]] = None

    def __post_init__(self) -> None:
        self.calendar = [
            [""]*7 for _ in range(self.current_month.get.number_of_days)]

    def set_first_weekend_day(self, weekday: str):
        for p in self.person:
            if p.weekend.is_on_first(weekday, p.name):
                first_saturday = self.current_month.get.list_of_weekday(weekday)[
                    0]
                week, day = self.current_month.get_calendar_indexes_for_this_day(
                    first_saturday)
                self.calendar[week][day] = p.name

    def set_required_days(self):
        for p in self.person:
            for day in p.validator.required_days:
                print(day, p.name)
                week, day = self.current_month.get_calendar_indexes_for_this_day(day)
                self.calendar[week][day] = p.name


def sort_list_index_by_hours(people: list[Person]):
    sp = sorted(people, key=lambda person: person.worked_hours)
    return [people.index(p) for p in sp]

@dataclass()
class Agenda:
    setter: AgendaSetter
    calendar: Optional[list[list[str]]] = None

    def update_calendar(self):
        self.calendar = self.setter.calendar


def new_agenda_from_yml(yml_dict) -> Agenda:
    month_info = monthinfo.new(year=yml_dict["year"], month=yml_dict["month"], first_week_day="Saturday")
    person =  new_person_list_from_yml(yml_dict)
    agendaSetter = AgendaSetter(person=person, current_month=month_info)
    return Agenda(setter=agendaSetter)
