class Person():

    hours_worked_on_weekends_holidays = 0
    regular_worked_hours = 0

    def __init__(self, name, id, week_restriction, day_restriction, days_to_work, holidays, regular):
        self.name = name
        self.id = id
        self.week_restriction = week_restriction
        self.day_restriction = day_restriction
        self.days_to_work = days_to_work
        self.holidays = holidays
        self.regular = regular

    def has_to_work_today(self, current_month_day) -> bool:
        return current_month_day in self.days_to_work

    def has_to_work_on_first_saturday(self, agenda) -> bool:
        return agenda.first_weekend["saturday"] == self.name

    def has_to_work_on_first_sunday(self, agenda) -> bool:
        return agenda.first_weekend["sunday"] == self.name

    def is_holiday(self, day):
        return day in self.holidays

    def sum_weekends_holidays_worked_hours(self, agenda, current_day):
        if self.is_holiday(current_day) or agenda.is_weekend(current_day):
            self.hours_worked_on_weekends_holidays += 24

    def sum_regular_worked_hours(self, agenda, current_day):
        if not self.is_holiday(current_day) and not agenda.is_weekend(current_day):
            self.regular_worked_hours += 15

    def sum_worked_days(self, agenda):
        for d in agenda.list_of_days():
            i, j = agenda.get_calendar_indexes_for_this_day(d)

            if agenda.month_assigned_days_by_name[i][j] == self.name:
                self.sum_weekends_holidays_worked_hours(
                    agenda, agenda.month_calendar[i][j])
                self.sum_regular_worked_hours(
                    agenda, agenda.month_calendar[i][j])

    def total_of_worked_hours(self) -> int:
        return self.regular_worked_hours + self.hours_worked_on_weekends_holidays

    def number_of_weekends_holidays_worked(self) -> int:
        return self.hours_worked_on_weekends_holidays / 24

    def number_of_regular_days_worked(self) -> int:
        return self.regular_worked_hours / 15

    def number_of_worked_days(self) -> int:
        return self.number_of_regular_days_worked() + self.number_of_weekends_holidays_worked()


def init_person_obj(yml):
    return [Person(p["name"], p["id"], p["week_restriction"],
                   p["day_restriction"], p["days_to_work"],
                   p["holidays"], p["regular"]) for p in yml["person"]]
