import calendar
from enum import Enum
from monthinfo import monthinfo

class DefinedHours:
    allowed = 0
    week = 0
    weekend = 0
    holiday = 0

class WeekDays(Enum):
    SATURDAY = {0:0, "sat": 0, "saturday": 0}
    SUNDAY = {1:1, "sun": 1, "sunday": 1}
    MONDAY = {2:2, "mon": 2, "monday": 2}
    TUESDAY = {3:3, "tue": 3, "tuesday": 3}
    WEDNESDAY = {4:4, "wed": 4, "wednesday": 4}
    THURSDAY = {5:5, "thu": 5, "thursday": 5}
    FRIDAY = {6:6, "fri": 6, "friday": 6}


class Workday:
    def __init__(self, hours):
        self.hours_calculator = HoursCalculator(hours)
        self.days_calculator = DaysCalculator()

    def add_worked_hours(self, hours):
        self.hours_calculator.add_worked_hours(hours)
        self.days_calculator.add_worked_days(
            hours / self.hours_calculator.hours_per_day)

    def is_on(self, day):
        raise NotImplementedError


class Weekday(Workday):
    def __init__(self):
        super().__init__(DefinedHours.week)

    def is_on(self, day):
        return True


class Weekend(Workday):
    def __init__(self):
        super().__init__(DefinedHours.weekend)

    def is_on(self, day):
        return day in (WeekDays.SATURDAY, WeekDays.SUNDAY)


class Holiday(Workday):
    def __init__(self, days):
        super().__init__(DefinedHours.holiday)
        self.days = days

    def is_on(self, day):
        return day in self.days


class WorkdayValidator:
    def __init__(self, required_days: list[int], restricted_days: list[int]):
        self.required_days = required_days
        self.restricted_days = restricted_days

    def is_required(self, day) -> bool:
        return day in self.required_days

    def is_restricted(self, day) -> bool:
        return day in self.restricted_days


class Person:
    def __init__(self, name: str, required_days: list[int], restricted_days: list[int],
                 restricted_weekdays: list[str], holidays: list[int], first_weekend: dict):
        self.name = name
        self.workday_validator = WorkdayValidator(
            required_days, restricted_days)
        self.weekday = Weekday()
        self.weekend = Weekend()
        self.holiday = Holiday(holidays)
        self.first_weekend = first_weekend

    def add_worked_hours(self, month: str, year: int, hours: int):
        calendar_retriever = CalendarRetriever()
        calendar_month = calendar_retriever.get_calendar(month, year)
        workday_decider = WorkdayDecider(
            self.workday_validator, self.weekday, self.weekend, self.holiday, self.first_weekend)
        for week in calendar_month:
            for day in week:
                workday = workday_decider.decide(day)
                workday.add_worked_hours(hours)

    def worked_hours(self) -> int:
        return self.weekday.hours_calculator.worked_hours + self.weekend.hours_calculator.worked_hours + self.holiday.hours_calculator.worked_hours

    def worked_days(self) -> int:
        return self.weekday.days_calculator.worked_days + self.weekend.days_calculator.worked_days + self.holiday.days_calculator.worked_days


class CalendarRetriever:
    def get_calendar(self, month: str, year: int):
        return calendar.monthcalendar(year, monthinfo.index(month)+1)


class WorkdayDecider:
    def __init__(self, workday_validator, weekday, weekend, holiday, first_weekend):
        self.workday_validator = workday_validator
        self.weekday = weekday
        self.weekend = weekend
        self.holiday = holiday
        self.first_weekend = first_weekend

    def decide(self, day):
        day_str = calendar.day_name[day-1][:3].lower()
        if self.workday_validator.is_required(day):
            if self.weekday.is_on(day_str):
                return self.weekday
            elif self.week
