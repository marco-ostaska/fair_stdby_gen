import yaml
import calendar
from tabulate import tabulate
from yaml.loader import SafeLoader


class Agenda:
    Sat = 0
    Sun = 1
    Mon = 2
    Tue = 3
    Wed = 4
    Thu = 5
    Fri = 6

    def __init__(self, data):
        self.year = data["year"]
        self.month = data["month"]
        self.holidays = data["Holidays"]
        calendar.setfirstweekday(calendar.SATURDAY)
        self.month_calendar = calendar.monthcalendar(self.year, self.month)
        self.month_schedule = [[""]*7 for i in range(len(self.month_calendar))]
        self.init_saturday = data["last_saturday"]
        self.init_sunday = data["last_sunday"]

    def fill_month_schedule_wanted_days(self, people_list):
        for week in range(len(self.month_calendar)):
            for day in range(len(self.month_calendar[week])):
                for person in people_list:
                    if person.has_to_work(self.month_calendar[week][day]):
                        self.month_schedule[week][day] = person.name
                        break

    def saturday_block(self, person, week) -> bool:
        # is it the first saturday of month and person match the existing init saturday:
        if (self.month_calendar[week][self.Sat] <= 7) and (self.init_saturday == person.name):
            return True

        # Person cant work on saturday if already worked on last one
        if (self.month_schedule[week-1][self.Sat] == person.name):
            return True

        # Person has worked on last Friday
        if (self.month_schedule[week-1][self.Fri] == person.name):
            return True

        # Person has worked on last Sunday
        if person.total > 3 and (self.month_schedule[week-1][self.Sun] == person.name):
            return True

        return False

    def sunday_block(self, person, week) -> bool:
        # is it the first saturday of month and person match the existing init saturday:
        if (self.month_calendar[week][self.Sun] <= 7) and (self.init_sunday == person.name):
            return True

        # Person cant work on sunday if already worked on last one
        if (self.month_schedule[week-1][self.Sun] == person.name):
            return True

        # Person has worked on Saturday
        if (self.month_schedule[week][self.Sat] == person.name):
            return True

        if person.total > 3:
            # Person has worked on last Saturday
            if self.month_schedule[week-1][self.Sat] == person.name:
                return True

        return False

    def monday_block(self, person, week) -> bool:
        # Has worked on Sunday
        if (self.month_schedule[week][self.Sun] == person.name):
            return True

        # Has worked on Saturday
        if (self.month_schedule[week][self.Sat] == person.name) and person.total > 2:
            return True


class Person:

    def __init__(self, idx, name, week_restriction, day_restriction, wanted_days, total):
        self.name = name
        self.week_restriction = week_restriction
        self.day_restriction = day_restriction
        self.wanted_days = wanted_days
        self.idx = idx
        self.total = total

    def has_week_restriction(self, week_day) -> bool:
        if week_day in self.week_restriction:
            return True

    def has_day_restriction(self, month_day) -> bool:
        if month_day in self.day_restriction:
            return True

    def has_to_work(self, month_day) -> bool:
        if month_day in self.wanted_days:
            return True

    def available(self, month_day, week_day) -> bool:
        if self.has_day_restriction(month_day):
            return False

        if self.has_week_restriction(week_day):
            return False
        return True


def read_yaml(file_name):
    with open(file_name, 'r') as stream:
        try:
            return yaml.load(stream, Loader=SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)

# Function to initialize objects


def init_objects(data):
    people_list = []
    for people in data["People"]:
        people_list.append(Person(people["idx"], people["Name"], people["week_restriction"],
                                  people["day_restriction"], people["wanted_days"], len(data["People"])))

    return people_list, Agenda(data)

# function to get the next person from person list based on the last one used


def get_next_person(people_list, current_person_idx, month_day, week_day) -> int:
    for person in people_list:
        if person.idx > current_person_idx:
            if not person.available(month_day, week_day):
                return get_next_person(people_list, person.idx,
                                       month_day, week_day)

            return person.idx
    return people_list[0].idx


def fill_schedule(agenda, person):

    # Already fill the days a person need to work
    agenda.fill_month_schedule_wanted_days(person)
    person_idx = 0

    for week in range(len(agenda.month_calendar)):
        for day in range(len(agenda.month_calendar[week])):
            if agenda.month_calendar[week][day] > 0 and agenda.month_schedule[week][day] == "":
                # saturday
                if day == agenda.Sat and agenda.month_schedule[week][day] == "":
                    while agenda.saturday_block(person[person_idx], week):
                        person_idx = get_next_person(
                            person, person_idx, agenda.month_calendar[week][day], day)
                    agenda.month_schedule[week][day] = person[person_idx].name
                # Sunday
                elif day == agenda.Sun and agenda.month_schedule[week][day] == "":
                    while agenda.sunday_block(person[person_idx], week):
                        person_idx = get_next_person(
                            person, person_idx, agenda.month_calendar[week][day], day)
                    agenda.month_schedule[week][day] = person[person_idx].name
                # Monday
                elif day == agenda.Mon and agenda.month_schedule[week][day] == "":
                    while agenda.monday_block(person[person_idx], week):
                        person_idx = get_next_person(
                            person, person_idx, agenda.month_calendar[week][day], day)
                    agenda.month_schedule[week][day] = person[person_idx].name
                # other_days
                elif day in range(3, 7) and agenda.month_schedule[week][day] == "":
                    while agenda.month_schedule[week][day-1] == person[person_idx].name:
                        person_idx = get_next_person(
                            person, person_idx, agenda.month_calendar[week][day], day)
                    agenda.month_schedule[week][day] = person[person_idx].name


def print_summary(person, agenda):
    for p in person:
        sum_hours = 0
        work_days = 0
        day_24 = 0
        day_15 = 0

        for week in range(len(agenda.month_calendar)):
            for day in range(0, 7):
                if agenda.month_calendar[week][day] != 0 and agenda.month_schedule[week][day] == p.name:
                    work_days += 1
                    if agenda.month_calendar[week][day] in agenda.holidays or day == 0 or day == 1:
                        sum_hours += 24
                        day_24 += 1
                    else:
                        sum_hours += 15
                        day_15 += 1

        print(tabulate([['', sum_hours, work_days, day_15, day_24]],
                       headers=[p.name, "Hours", 'Days', '15h day', '24h day'], tablefmt='psql'))
        print()


def print_schedule(agenda):
    for week in range(len(agenda.month_calendar)):
        for day in range(0, 7):
            if agenda.month_calendar[week][day] != 0:
                agenda.month_schedule[week][day] = "{}. {}".format(
                    agenda.month_calendar[week][day], agenda.month_schedule[week][day])
            if agenda.month_calendar[week][day] in agenda.holidays:
                agenda.month_schedule[week][day] = "{} (holiday)".format(
                    agenda.month_schedule[week][day])
                print()
    print(tabulate(agenda.month_schedule, headers=['Saturday', 'Sunday',
                                                   'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], tablefmt='psql'))


def main():
    data = read_yaml("./config/config.yaml")
    person, agenda = init_objects(data)

    # exit program if person.total < 3
    if person[0].total < 3:
        print("Not enough people to work")
        exit(1)

    fill_schedule(agenda, person)
    print_summary(person, agenda)
    print_schedule(agenda)


if __name__ == "__main__":
    main()
