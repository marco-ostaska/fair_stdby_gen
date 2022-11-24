from monthinfo.monthinfo import CurrentMonth


class Agenda(CurrentMonth):
    SATURDAY, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY = range(7)

    ONE_WEEK = 7
    TWO_WEEKS = ONE_WEEK*2
    THREE_WEEKS = ONE_WEEK*3

    def __init__(self, year, month, hours, first_weekend):
        super().__init__(month, year, 5)
        self.year = year
        self.month = month
        self.hours = hours
        self.first_weekend = first_weekend
        self.month_calendar = self.calendar()
        self.month_assigned_days_by_id = self.blank_month_calendar()
        self.month_assigned_days_by_name = self.blank_month_calendar()

    def blank_month_calendar(self):
        return [
            [None]*7 for _ in range(len(self.month_calendar))]

    def set_month_assigned_days(self, day, person):
        i, j = self.get_calendar_indexes_for_this_day(day)
        self.month_assigned_days_by_id[i][j] = person.id
        self.month_assigned_days_by_name[i][j] = person.name

    def set_days_person_must_work(self, person):
        for day in self.list_of_days():
            if person.has_to_work_today(day):
                self.set_month_assigned_days(day, person)

    #saturdays
    def set_first_saturday(self, person):
        if person.has_to_work_on_first_saturday(self):
            self.set_month_assigned_days(
                person=person, day=self.list_of_saturdays()[0])

    def has_worked_on_saturdays_ago(self, person, current_day, days_ago):
        if not self.is_first_saturday(current_day) and (current_day - days_ago) >= 0:
            week, day = self.get_calendar_indexes_for_this_day(
                current_day - days_ago)
            return self.month_assigned_days_by_id[week][day] == person.id
        return False

    # sundays
    def set_first_sunday(self, person):
        if person.has_to_work_on_first_sunday(self):
            self.set_month_assigned_days(
                person=person, day=self.list_of_sundays()[0])

    def has_worked_on_sundays_ago(self, person, current_day, days_ago):
        if not self.is_first_saturday(current_day) and (current_day - days_ago) >= 0:
            week, day = self.get_calendar_indexes_for_this_day(
                current_day - days_ago)
            return self.month_assigned_days_by_id[week][day] == person.id
        return False

    #weekends
    def set_first_weekend(self, person):
        self.set_first_saturday(person)
        self.set_first_sunday(person)



def init_agenda_obj(yml):
    return Agenda(yml["year"], yml["month"], yml["hours"], yml["first_weekend"])
