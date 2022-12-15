from typing import List, Set


class WorkdayChecker:
    def __init__(self, required_days: Set[int], restricted_days: Set[int]):
        self.required_days = required_days
        self.restricted_days = restricted_days

    def is_required(self, day: int) -> bool:
        return day in self.required_days

    def is_restricted(self, day: int) -> bool:
        return day in self.restricted_days


class Workday:
    def __init__(self, name: str, hours: int):
        self.name = name
        self.hours = hours


class Weekday(Workday):
    pass


class Weekend(Workday):
    pass


class Holiday(Workday):
    pass


class Person:
    def __init__(self, name: str, required_days: Set[int], restricted_days: Set[int]):
        self.name = name
        self.workday_checker = WorkdayChecker(required_days, restricted_days)


class WorkdayCalculator:
    def __init__(self, allowed_hours: int, weekdays: List[Weekday], weekends: List[Weekend], holidays: List[Holiday]):
        self.allowed_hours = allowed_hours
        self.weekdays = weekdays
        self.weekends = weekends
        self.holidays = holidays

    def calculate_total_hours(self) -> int:
        total_hours = 0
        for workday in self.weekdays + self.weekends + self.holidays:
            total_hours += workday.hours
        return total_hours
