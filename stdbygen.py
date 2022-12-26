import calendar
from dataclasses import dataclass
from enum import Enum
from monthinfo import monthinfo
from typing import Optional

@dataclass()
class PreDefinedHours:
    allowed: int
    week: int
    weekend: int
    holiday: int

@dataclass()
class Holidays:
    days: int

@dataclass()
class WorkDaySetter:
    pass

@dataclass()
class WorkDayGetter:
    pass

@dataclass()
class WorkDayCalculator(object):
    hours_to_compute: int
    worked_hours: int = 0
    hours: int = 0

    def add_worked_hours(self):
        self.worked_hours += self.hours_to_compute

    @property
    def worked_days(self) -> int:
        return self.worked_hours / self.hours_to_compute


@dataclass()
class WorkdayValidator:
    required_days: list[int]
    restricted_days: list[int]
    holidays: Holidays

    def is_required(self, day) -> bool:
        return day in self.required_days

    def is_restricted(self, day) -> bool:
        return day in self.restricted_days

    def is_holiday(self, day) -> bool:
        return day in self.holidays.days





# class Weeks(Workday):

#     def __init__(self, restricted_weekdays):
#         self.restricted_weekdays = restricted_weekdays
#         self.hours = DefinedHours.week

#     def is_restricted(self, week_day) -> bool:
#         return week_day[:3].lower() in [day[:3].lower() for day in self.restricted_weekdays]

# class Weekends(Workday):

#     def __init__(self, first_weekend):
#         self.first_weekend = first_weekend
#         self.hours = DefinedHours.weekend

#     def is_on_first(self, weekday, onduty_person) -> bool:
#         return self.first_weekend[weekday[:3]] == onduty_person

# class Person(Workday):
#     def __init__(self, name: str, required_days: list[int],restricted_days: list[int],
#                                      week: Weeks, weekend: Weekends, holiday: Holidays):
#         super().__init__(required_days, restricted_days)
#         self.name = name
#         self.holiday = holiday
#         self.week = week
#         self.weekend = weekend

#     def worked_hours(self) -> int:
#         return self.week.worked_hours + self.weekend.worked_hours + self.holiday.worked_hours

#     def worked_days(self) -> int:
#         return self.week.worked_days() + self.weekend.worked_days() + self.holiday.worked_days()



# def set_defined_hours(yml_dict):
#     DefinedHours.allowed = yml_dict["hours"]["allowed"]
#     DefinedHours.holiday = yml_dict["hours"]["holiday"]
#     DefinedHours.week = yml_dict["hours"]["week"]
#     DefinedHours.weekend  = yml_dict["hours"]["weekend"]


# def new_person(name: str, required_days: list[int], restricted_days: list[int],
#                       restricted_weekdays: list[str],holidays: list[int], first_weekend: dict) -> Person:

#     name = name.title()
#     week = Weeks([str(day[:3]).lower() for day in restricted_weekdays])
#     first_sat = str(first_weekend["saturday"]).title()
#     first_sun = str(first_weekend["sunday"]).title()
#     first_weekend = {"sat": first_sat, "sun": first_sun}
#     weekend = Weekends(first_weekend)
#     holiday = Holidays(holidays)

#     return Person(name=name, required_days=required_days,restricted_days=restricted_days,
#                  week=week, holiday=holiday, weekend=weekend)


# def person_list_from_yml(yml_dict) -> list[Person]:
#     set_defined_hours(yml_dict)
#     return [new_person(p["name"], p["required_days"],
#                       p["restricted_days"],
#                       p["restricted_weekdays"], p["holidays"],
#                       yml_dict["first_weekend"]) for p in yml_dict["person"]]


# class DayOfWeek(monthinfo.CurrentMonth):
#     def __init__(self, month, year, first_week_day):
#         super().__init__(month, year, first_week_day)

#     def get_first_day(self, weekday):
#         for


# class Saturday(DayOfWeek):
#     def __init__(self):
#         super().__init__("Saturday", 6)


# class Agenda():
#     def __init__(self,  current_month: monthinfo.CurrentMonth,  people: list[Person]):
#         self.current_month = current_month
#         self.people = people
#         self.calendar = [[""]*7 for _ in range(self.current_month.number_of_days())]



# def new_agenda_from_yml(yml_dict) -> Agenda:
#     month_info = monthinfo.CurrentMonth(yml_dict['month'], yml_dict['year'], calendar.SATURDAY)
#     people =  person_list_from_yml(yml_dict)
#     return Agenda(month_info, people)
