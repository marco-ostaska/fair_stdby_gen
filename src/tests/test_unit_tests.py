import unittest

from .. import configFile
from .. import People
from .. import Schedule


CONFIG_FILE = './src/tests/config_5_people.yml'
YML = configFile.read_yaml_file(CONFIG_FILE)


class TestConfigFile(unittest.TestCase):

    def test_can_read_file(self):
        self.assertEqual(configFile.read_yaml_file(CONFIG_FILE)["year"], 2022)


class TestSchedule(unittest.TestCase):

    AGENDA = Schedule.init_agenda_obj(YML)

    def test_can_init_agenda_obj(self):
        self.assertEqual(TestSchedule.AGENDA.year, 2022)

    def test_monthinfo(self):
        self.assertEqual(TestSchedule.AGENDA.month_calendar[0][3], 1)

    def test_set_days_person_must_work(self):
        agenda = TestSchedule.AGENDA
        person = People.init_person_obj(YML)
        agenda.set_days_person_must_work(person[1])
        self.assertEqual(agenda.month_assigned_days_by_name[3][3], "Person_2")

    def test_set_first_weekend(self):
        person, _ = People.init_person_obj(YML), Schedule.init_agenda_obj(YML)
        agenda = TestSchedule.AGENDA
        agenda.first_weekend["sunday"] = "Person_3"
        agenda.first_weekend["saturday"] = "Person_2"
        agenda.set_first_weekend(person[2])
        agenda.set_first_weekend(person[1])
        self.assertEqual(agenda.first_weekend["sunday"], "Person_3")
        i, j = agenda.current_month.get_calendar_indexes_for_this_day(6)
        self.assertEqual(agenda.month_assigned_days_by_name[i][j], "Person_3")
        i, j = agenda.current_month.get_calendar_indexes_for_this_day(5)
        self.assertEqual(agenda.month_calendar[i][j], 5)
        self.assertEqual(agenda.month_assigned_days_by_name[i][j], "Person_2")

    # def test_has_worked_on_saturdays_ago(self):
    #     person, _ = TestPeople().reset_data_for_tests(YML)
    #     agenda = TestSchedule.AGENDA
    #     agenda.set_first_saturday(person)
    #     self.assertFalse(agenda.has_worked_on_saturdays_ago(
    #         person, 5, agenda.ONE_WEEK_AGO))
    #     self.assertTrue(agenda.has_worked_on_saturdays_ago(
    #         person, 12, agenda.ONE_WEEK_AGO))
    #     self.assertFalse(agenda.has_worked_on_saturdays_ago(
    #         person, 12, agenda.TWO_WEEKS_AGO))

    def test_has_worked_on_sundays_ago(self):
        person, _ = People.init_person_obj(
            YML)[2], Schedule.init_agenda_obj(YML)
        agenda = TestSchedule.AGENDA
        agenda.first_weekend["sunday"] = "Person_3"
        agenda.set_first_weekend(person)
        self.assertFalse(agenda.has_worked_on_sundays_ago(
            person, 6, agenda.ONE_WEEK))
        self.assertTrue(agenda.has_worked_on_sundays_ago(
            person, 13, agenda.ONE_WEEK))
        self.assertFalse(agenda.has_worked_on_sundays_ago(
            person, 13, agenda.TWO_WEEKS))


class TestPeople(unittest.TestCase):

    def reset_data_for_tests(self, YML):
        return People.init_person_obj(YML)[1], Schedule.init_agenda_obj(YML)

    def test_can_init_person_obj(self):
        person = People.init_person_obj(YML)
        self.assertEqual(person[0].name, "Person_1")

    def test_person_has_to_work_today(self):
        person, _ = self.reset_data_for_tests(YML)
        person.days_to_work = [2, 3, 4, 15, 10, 20]
        self.assertTrue(person.has_to_work_today(10))

    def test_has_to_work_on_first_saturday(self):
        person, agenda = self.reset_data_for_tests(YML)
        agenda.first_weekend["saturday"] = "Person_2"
        self.assertTrue(person.has_to_work_on_first_saturday(agenda.first_weekend["saturday"]))
        agenda.first_weekend["saturday"] = "Person_1"
        self.assertFalse(person.has_to_work_on_first_saturday(agenda.first_weekend["saturday"]))

    def test_has_reached_number_of_hours(self):
        person, agenda = self.reset_data_for_tests(YML)
        person.regular_worked_hours = 200
        self.assertTrue(person.has_reached_number_of_hours(agenda.hours["allowed"]))

    def test_has_to_work_on_first_sunday(self):
        person, agenda = self.reset_data_for_tests(YML)
        agenda.first_weekend["sunday"] = "Person_2"
        self.assertTrue(person.has_to_work_on_first_sunday(agenda.first_weekend["sunday"]))
        agenda.first_weekend["sunday"] = "Person_1"
        self.assertFalse(person.has_to_work_on_first_sunday(agenda.first_weekend["sunday"]))

    def test_is_holiday(self):
        person, _ = self.reset_data_for_tests(YML)
        person.holidays = [2, 20, 15]
        self.assertTrue(person.is_holiday(15))

    def compute_worked_days(self):
        person, agenda = self.reset_data_for_tests(YML)
        person.holidays = [2, 20, 15]
        person.days_to_work = [2, 15, 20, 1, 3, 6]
        agenda.set_days_person_must_work(person)
        person.sum_worked_days(agenda)
        return person

    def test_sum_weekends_holidays_worked_hours(self):
        person = self.compute_worked_days()
        self.assertEqual(person.hours_worked_on_weekends_holidays, (24*4))

    def test_regular_worked_hours(self):
        person = self.compute_worked_days()
        self.assertEqual(person.regular_worked_hours, (15*2))

    def test_total_of_worked_hours(self):
        person = self.compute_worked_days()
        self.assertEqual(person.total_of_worked_hours(), (15*2)+(24*4))

    def test_number_of_weekends_holidays_worked(self):
        person = self.compute_worked_days()
        self.assertEqual(person.number_of_weekends_holidays_worked(), 4)

    def test_number_of_regular_days_worked(self):
        person = self.compute_worked_days()
        self.assertEqual(person.number_of_regular_days_worked(), 2)

    def test_number_of_worked_days(self):
        person = self.compute_worked_days()
        self.assertEqual(person.number_of_worked_days(), 2 + 4)

    def test_sum_worked_days(self):
        self.test_sum_weekends_holidays_worked_hours()
        self.test_regular_worked_hours()
        self.test_number_of_weekends_holidays_worked()
        self.test_number_of_regular_days_worked()
        self.test_number_of_worked_days()

    def test_sort_list_index_by_hours_for_regular_person(self):
        person = People.init_person_obj(YML)
        person[1].regular_worked_hours = 15
        person[0].hours_worked_on_weekends_holidays = 24
        person[2].hours_worked_on_weekends_holidays = 24
        person[3].hours_worked_on_weekends_holidays = 48
        person[4].hours_worked_on_weekends_holidays = 24

        self.assertEqual(
            People.sort_list_index_by_hours(person), [1, 0, 2, 4, 3])

if __name__ == '__main__':
    unittest.main()
