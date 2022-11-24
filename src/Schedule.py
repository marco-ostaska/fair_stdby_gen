from monthinfo.monthinfo import CurrentMonth


class Agenda(object):
    SATURDAY, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY = range(7)

    ONE_WEEK = 7
    TWO_WEEKS = ONE_WEEK*2
    THREE_WEEKS = ONE_WEEK*3

    def __init__(self, year, month, hours, first_weekend):
        self.current_month = CurrentMonth(month, year, 5)
        self.year = year
        self.month = month
        self.hours = hours
        self.first_weekend = first_weekend
        self.month_calendar = self.current_month.calendar()
        self.month_assigned_days_by_id = self.blank_calendar()
        self.month_assigned_days_by_name = self.blank_calendar()

    def blank_calendar(self):
        return [
            [None]*7 for _ in range(len(self.month_calendar))]

    def set_month_assigned_days(self, day, person):
        i, j = self.current_month.get_calendar_indexes_for_this_day(day)
        self.month_assigned_days_by_id[i][j] = person.id
        self.month_assigned_days_by_name[i][j] = person.name

    def set_days_person_must_work(self, person):
        for day in self.current_month.list_of_days():
            if person.has_to_work_today(day):
                self.set_month_assigned_days(day, person)

    def has_worked_on_saturdays_ago(self, person, current_day, weeks_ago):
        return Saturday.has_worked_on_weeks_ago(self, person, current_day, weeks_ago)

    def has_worked_on_sundays_ago(self, person, current_day, weeks_ago):
        return Sunday.has_worked_on_weeks_ago(self, person, current_day, weeks_ago)

    #weekends
    def set_first_weekend(self, person):
        Weekends.set_first(self, person)

class Saturday(Agenda):
    def set_first(self, person):
        if person.has_to_work_on_first_saturday(self.first_weekend["saturday"]):
            self.set_month_assigned_days(
                person=person, day=self.current_month.list_of_saturdays()[0])

    def has_worked_on_weeks_ago(self, person, current_day, weeks_ago):
        if not self.current_month.is_first_saturday(current_day) and (current_day - weeks_ago) >= 0:
            week, day = self.current_month.get_calendar_indexes_for_this_day(
                current_day - weeks_ago)
            return self.month_assigned_days_by_id[week][day] == person.id
        return False

class Sunday(Agenda):
    def set_first(self,person):
        if person.has_to_work_on_first_sunday(self.first_weekend["sunday"]):
            self.set_month_assigned_days(
                person=person, day=self.current_month.list_of_sundays()[0])

    def has_worked_on_weeks_ago(self, person, current_day, weeks_ago):
        if not self.current_month.is_first_sunday(current_day) and (current_day - weeks_ago) >= 0:
            week, day = self.current_month.get_calendar_indexes_for_this_day(
                current_day - weeks_ago)
            return self.month_assigned_days_by_id[week][day] == person.id
        return False

class Weekends(Sunday):
    def set_first(self, person):
        Saturday.set_first(self, person)
        Sunday.set_first(self, person)




def init_agenda_obj(yml):
    return Agenda(yml["year"], yml["month"], yml["hours"], yml["first_weekend"])
