# Person
# bools:
# - has_to_work_today?
# - has_to_work_first_saturday?
# - has_to_work_first_sunday?
# - has_reached_number_of_hours?
# - has_holiday_today?
# - has_worked_on_last_saturday
# - has_worked_on_last_sunday
# - can_work_this_saturday
# - can_work_this_sunday
# - can_work_this_monday

# get
# number_of_worked_days
# number_of_regular_days_worked
# number_of_non_regular_days_worked
# saturdays_worked
# mondays_worked ....



# set
# sum_non_regular_hours
# sum_regular_hours
# sum_worked_days
# sort_list_index_by_hours


# Rules

# saturday
# Person can not work two saturdays in a row
# person can not work on saturday if already worked on friday


# sunday
# Person can not work two sundays in a row
# person can not work on sunday if already worked on saturday

# monday
# person can not work on monday if already worked on weekend


class Person(object):

    hours_worked_on_weekends_holidays = 0
    regular_worked_hours = 0

    def __init__(self, name, id, week_restriction, day_restriction, days_to_work, holidays):
        self.name = name
        self.id = id
        self.week_restriction = week_restriction
        self.day_restriction = day_restriction
        self.days_to_work = days_to_work
        self.holidays = holidays

    def has_to_work_today(self, current_month_day) -> bool:
        return current_month_day in self.days_to_work

    def has_to_work_on_first_saturday(self, designated_name) -> bool:
        return designated_name == self.name

    def has_to_work_on_first_sunday(self, designated_name) -> bool:
        return designated_name== self.name

    def has_reached_number_of_hours(self, hours_allowed) -> bool:
        return self.total_of_worked_hours() >= hours_allowed

    def is_holiday(self, day):
        return day in self.holidays

    def sum_weekends_holidays_worked_hours(self, agenda, current_day):
        if self.is_holiday(current_day) or agenda.current_month.is_weekend(current_day):
            self.hours_worked_on_weekends_holidays += agenda.hours["weekend_holidays"]

    def sum_regular_worked_hours(self, agenda, current_day):
        if not self.is_holiday(current_day) and not agenda.current_month.is_weekend(current_day):
            self.regular_worked_hours += agenda.hours["regular"]

    def sum_worked_days(self, agenda):
        for d in agenda.current_month.list_of_days():
            i, j = agenda.current_month.get_calendar_indexes_for_this_day(d)

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


def sort_list_index_by_hours(people):
    sp = sorted(people, key=lambda person: person.total_of_worked_hours())
    return [people.index(p) for p in sp]



def init_person_obj(yml):
    return [Person(p["name"], p["id"], p["week_restriction"],
                   p["day_restriction"], p["days_to_work"],
                   p["holidays"]) for p in yml["person"]]
