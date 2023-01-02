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

    def add_worked_hours(self) -> None:
        self.worked_hours += self.hours_to_compute

    @property
    def worked_days(self) -> int:
        return self.worked_hours / self.hours_to_compute

@dataclass()
class Holidays:
    days: int
    calc: WorkDayCalculator

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


    def add_worked_hours(self) -> None:
       self.worked_hours += self.week.calc.worked_hours + self.weekend.calc.worked_hours + self.holiday.calc.worked_hours

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
class Agenda:
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
                week, day = self.current_month.get_calendar_indexes_for_this_day(day)
                self.calendar[week][day] = p.name

    def get_calendar_idx_for_person(self, name: str):
        indexes = []
        for i in range(len(self.calendar)):
            indexes.extend((i, j) for j in range(len(self.calendar[i])) if self.calendar[i][j] == name)
        return indexes

    def get_list_of_worked_holiday_days(self, person: Person) -> list[int]:
        idx = self.get_calendar_idx_for_person(person.name)
        return [self.current_month.calendar[i][j] for i, j in idx if person.validator.is_holiday(self.current_month.calendar[i][j])]

    def get_list_of_worked_weekend_days(self, person: Person) -> list[int]:
        idx = self.get_calendar_idx_for_person(person.name)
        return [self.current_month.calendar[i][j] for i, j in idx if self.current_month.validate.is_weekend(self.current_month.calendar[i][j])]

    def get_list_of_worked_week_days(self, person: Person) -> list[int]:
        idx = self.get_calendar_idx_for_person(person.name)
        return [
            self.current_month.calendar[i][j]
            for i, j in idx
            if not self.current_month.validate.is_weekend(self.current_month.calendar[i][j])
            and not person.validator.is_holiday(self.current_month.calendar[i][j])
        ]

    def update_worked_hours(self):
        for p in self.person:
            p.holiday.calc.worked_hours =0
            p.week.calc.worked_hours =0
            p.weekend.calc.worked_hours = 0
            p.worked_hours = 0

            for _ in self.get_list_of_worked_holiday_days(p):
                p.holiday.calc.add_worked_hours()

            for _ in self.get_list_of_worked_weekend_days(p):
                p.weekend.calc.add_worked_hours()

            for _ in self.get_list_of_worked_week_days(p):
                p.week.calc.add_worked_hours()

            p.add_worked_hours()

    def assign_person(self, week:int, day:int, person:str) -> None:
        self.calendar[week][day] = person
        self.update_worked_hours()



@dataclass()
class WeekRules:
    agenda: Agenda
    sat: int = 0
    sun: int = 0

    # def last_worked(self, weekday: str, person: str) -> int:
    #     last = self.agenda.current_month.get.list_of_weekday(weekday)
    #     for l in reversed(last):
    #         i,j = self.agenda.current_month.get_calendar_indexes_for_this_day(l)
    #         if self.agenda.calendar[i][j] == person:
    #             return l

    def has_worked_last_weekend(self, day: int, person:str) -> bool:
        if self.agenda.current_month.validate.is_day_in_weekday(day, "saturday"):
            self.sat = day

        if self.agenda.current_month.validate.is_day_in_weekday(day, "sunday"):
            self.sat = day-1

        self.sat -= 7
        i, j = self.agenda.current_month.get_calendar_indexes_for_this_day(self.sat)

        return (self.agenda.calendar[i][j] == person or  self.agenda.calendar[i+1][j+1] == person)

    # def will_work_next_weekend(self, day: int, person:str) -> bool:


@dataclass()
class SaturdayRules:
    week: WeekRules

    def is_blocked(self, day: int, person: str) -> bool:
        return self.week.has_worked_last_weekend(day, person)




def new_agenda_from_yml(yml_dict) -> Agenda:
    month_info = monthinfo.new(year=yml_dict["year"], month=yml_dict["month"], first_week_day="Saturday")
    person =  new_person_list_from_yml(yml_dict)
    return Agenda(person=person, current_month=month_info)


def sort_list_index_by_hours(people: list[Person]):
    sp = sorted(people, key=lambda person: person.worked_hours)
    return [people.index(p) for p in sp]


def process(yml):
    agenda = new_agenda_from_yml(yml)

    agenda.set_first_weekend_day("saturday")
    agenda.set_first_weekend_day("sunday")
    agenda.set_required_days()
    agenda.update_worked_hours()

    for day in agenda.current_month.get.list_of_days:
        i, j = agenda.current_month.get_calendar_indexes_for_this_day(day)
        weekday = calendar.day_name[calendar.weekday(agenda.current_month.year, agenda.current_month.month, day)]
        if agenda.calendar[i][j] != "":
            for p in agenda.person:
                if agenda.calendar[i][j] == p.name:
                    print(day, weekday, p.name, p.worked_hours)

        if agenda.calendar[i][j] == "":

            ###########################################################
            # saturday
            ###########################################################
            if weekday == "Saturday":
                for ix in sort_list_index_by_hours(agenda.person):
                    week_rule = WeekRules(agenda)
                    sat_rule = SaturdayRules(week_rule)
                    if not sat_rule.is_blocked(day, agenda.person[ix].name):
                        agenda.assign_person(i,j,agenda.person[ix].name)
                        print(day, weekday, agenda.person[ix].name, agenda.person[ix].worked_hours, week_rule.has_worked_last_weekend(day, agenda.person[ix].name))
                        break
            ###########################################################
            # sunday
            ###########################################################


            # if weekday == "Sunday":
            #     for ix in sort_list_index_by_hours(agenda.person):
            #         lsi, lsj = agenda.current_month.get_calendar_indexes_for_this_day(
            #             day - 8)
            #         lsd, lss = agenda.current_month.get_calendar_indexes_for_this_day(
            #             day - 7)
            #         lsy, lzt  = agenda.current_month.get_calendar_indexes_for_this_day(
            #             day - 1)

            #         # check if has worked on last weekend
            #         if agenda.calendar[lsi][lsj] != agenda.person[ix].name and agenda.calendar[lsd][lss] != agenda.person[ix].name and agenda.calendar[lsy][lzt] != agenda.person[ix].name:
            #             agenda.calendar[i][j] = agenda.person[ix].name
            #             agenda.update_worked_hours()
            #             print(
            #                 day, weekday, agenda.person[ix].name, agenda.person[ix].worked_hours, agenda.person[ix].worked_days)
            #             break


def main():
    pass

if __name__ == "__main__":
    main()
