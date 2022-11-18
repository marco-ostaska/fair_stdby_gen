from monthinfo.monthinfo import CurrentMonth


class Monday(CurrentMonth):
    pass


class Tuesday(CurrentMonth):
    pass


class Wednesday(CurrentMonth):
    pass


class Thursday(CurrentMonth):
    pass


class Friday(CurrentMonth):
    pass


class WeekRules(Monday, Tuesday, Wednesday, Thursday, Friday):
    pass


class Saturday(CurrentMonth):
    def set_first_saturday(self, person):
        week, day = self.get_calendar_indexes_for_this_day(
            self.list_of_saturdays()[0])
        if person.has_to_work_on_first_saturday(self):
            self.month_assigned_days_by_id[week][day] = person.id
            self.month_assigned_days_by_name[week][day] = person.name

    def has_worked_on_saturdays_ago(self, person, current_day, days_ago):
        if not self.is_first_saturday(current_day) and (current_day - days_ago) >= 0:
            week, day = self.get_calendar_indexes_for_this_day(
                current_day - days_ago)
            return self.month_assigned_days_by_id[week][day] == person.id
        return False


class Sunday(CurrentMonth):
    def set_first_sunday(self, person):
        week, day = self.get_calendar_indexes_for_this_day(
            self.list_of_sundays()[0])
        if person.has_to_work_on_first_sunday(self):
            self.month_assigned_days_by_id[week][day] = person.id
            self.month_assigned_days_by_name[week][day] = person.name

    def has_worked_on_sundays_ago(self, person, current_day, days_ago):
        if not self.is_first_saturday(current_day) and (current_day - days_ago) >= 0:
            week, day = self.get_calendar_indexes_for_this_day(
                current_day - days_ago)
            return self.month_assigned_days_by_id[week][day] == person.id
        return False


class WeekendRules(Saturday, Sunday):
    def set_first_weekend(self, person):
        self.set_first_saturday(person)
        self.set_first_sunday(person)


class Agenda(WeekRules, WeekendRules):
    SATURDAY, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY = range(7)

    ONE_WEEK_AGO = 7
    TWO_WEEKS_AGO = ONE_WEEK_AGO*2
    THREE_WEEKS_AGO = ONE_WEEK_AGO*3

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


def init_agenda_obj(yml):
    return Agenda(yml["year"], yml["month"], yml["allow_hours"], yml["first_weekend"])
