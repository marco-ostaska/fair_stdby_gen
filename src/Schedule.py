from monthinfo.monthinfo import CurrentMonth


class Agenda(CurrentMonth):
    SATURDAY, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY = range(7)

    def __init__(self, year, month, allow_hours, first_weekend):
        super().__init__(month, year, 5)
        self.year = year
        self.month = month
        self.allow_hours = allow_hours
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

    def set_first_saturday(self, person):
        for d in self.list_of_days():
            if self.is_first_saturday(d) and person.has_to_work_on_first_saturday:
                i, j = self.get_calendar_indexes_for_this_day(d)
                self.month_assigned_days_by_id[i][j] = person.id
                self.month_assigned_days_by_name[i][j] = person.name


def init_agenda_obj(yml):
    return Agenda(yml["year"], yml["month"], yml["allow_hours"], yml["first_weekend"])
