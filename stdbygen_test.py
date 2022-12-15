import unittest
import stdbygen


YML_DICT = {
    "year": 2022,
    "month": 11,
    "hours": {
        "allowed": 186,
        "week": 15,
        "weekend": 24,
        "holiday": 24

    },
    "first_weekend": {
        "saturday": "John Doe",
        "sunday": "Jane Doe"
    },
    "person": [
        {
            "name": "John Doe",
            "restricted_weekdays": ["Mon", "Wed", "Fri"],
            "restricted_days": [5, 17],
            "required_days": [2],
            "holidays": [25, 1]
        },
        {
            "name": "Jane Doe",
            "restricted_weekdays": ["Tue", "Thu"],
            "restricted_days": [],
            "required_days": [1, 10],
            "holidays": [25]
        },
        {
            "name": "Mark Doe",
            "restricted_weekdays": [],
            "restricted_days": [],
            "required_days": [2],
            "holidays": []
        },
        {
            "name": "Hugo Doe",
            "restricted_weekdays": [],
            "restricted_days": [],
            "required_days": [],
            "holidays": []
        },
        {
            "name": "Ana Doe",
            "restricted_weekdays": [2,4],
            "restricted_days": [],
            "required_days": [],
            "holidays": []
        }
    ]
}


def add_worked_hours_helper(func, days, hours_to_sum):
    total = 0
    for _ in range(days):
        func()
        total += hours_to_sum
    return total


class MockTests(unittest.TestCase):

    def setUp(self):
        holiday = stdbygen.new_holiday([25, 26], 24)
        week = stdbygen.new_week(["Mon", "Fri"], 15)
        weekend = stdbygen.new_weekend(
            {"saturday": "John Doe", "sunday": "Jane Doe"}, 24)
        self.mock_person = stdbygen.Person(
            "John Doe", [20, 30], [3, 2], holiday, week, weekend)

class Test_WorkdayValidator(MockTests):
    def test_is_required(self):
        self.assertTrue(self.mock_person.is_required(20))
        self.assertFalse(self.mock_person.is_required(25))

    def test_is_restricted(self):
        self.assertTrue(self.mock_person.is_restricted(3))
        self.assertFalse(self.mock_person.is_restricted(4))

class TEST_HoursCalculator(unittest.TestCase):

    def test_add_worked_hours(self):
        hour_calc = stdbygen.HoursCalculator(186)
        hour_calc.hours = 24
        total = add_worked_hours_helper(hour_calc.add_worked_hours, 2, 24)
        self.assertEqual(hour_calc.worked_hours, total)


class TEST_Holidays(MockTests):

    def test_is_on(self):
        self.assertTrue(self.mock_person.holiday.is_on(25))
        self.assertFalse(self.mock_person.holiday.is_on(27))

    def add_worked_hours_holiday(self):
        self.worked_hours += self.hours

    def test_add_worked_hours_holiday(self):
        self.mock_person.holiday.worked_hours = 0
        total = add_worked_hours_helper(self.mock_person.holiday.add_worked_hours, 2, 24)
        self.assertEqual(self.mock_person.holiday.worked_hours, total)

    def test_worked_days_holiday(self):
        self.mock_person.holiday.worked_hours = 0
        self.assertEqual(self.mock_person.holiday.worked_days(), 0)
        add_worked_hours_helper(self.mock_person.holiday.add_worked_hours, 20, 24)
        self.assertEqual(self.mock_person.holiday.worked_days(), 20)

class TEST_Weeks(MockTests):

    def test_is_restricted(self):
        self.assertTrue(self.mock_person.week.is_restricted("Fri"))
        self.assertFalse(self.mock_person.week.is_restricted("Thu"))

    def test_add_worked_hours_week(self):
        self.mock_person.week.worked_hours = 0
        total = add_worked_hours_helper(self.mock_person.week.add_worked_hours, 2, 15)
        self.assertEqual(self.mock_person.week.worked_hours, total)

    def test_worked_days_week(self):
        self.mock_person.week.worked_hours = 0
        self.assertEqual(self.mock_person.week.worked_days(), 0)
        add_worked_hours_helper(self.mock_person.week.add_worked_hours, 20, 15)
        self.assertEqual(self.mock_person.week.worked_days(), 20)

class TEST_Weekends(unittest.TestCase):
    def setUp(self):
        holiday = stdbygen.new_holiday([25, 26], 24)
        weekend = stdbygen.new_weekend({"saturday": "John Doe", "sunday": "Jane Doe"}, 24)
        week = stdbygen.new_week(["Mon", "Fri"], 15)
        self.mock_person = [stdbygen.Person("John Doe", [20, 30], [3, 2], holiday, week, weekend),
                            stdbygen.Person("Jane Doe", [20, 30], [3, 2], holiday, week, weekend)]

    def test_add_worked_hours_weekend(self):
        self.mock_person[0].weekend.worked_hours = 0
        total = add_worked_hours_helper(self.mock_person[0].weekend.add_worked_hours, 2, 24)
        self.assertEqual(self.mock_person[0].weekend.worked_hours, total)

    def test_worked_days_weekend(self):
        self.mock_person[0].weekend.worked_hours = 0
        self.assertEqual(self.mock_person[0].weekend.worked_days(), 0)
        add_worked_hours_helper(self.mock_person[0].weekend.add_worked_hours, 20, 15)
        self.assertEqual(self.mock_person[0].weekend.worked_days(), 20)

class Test_Person(MockTests):

    def test_total_worked_days(self):
        self.mock_person.holiday.worked_hours = 0
        self.mock_person.week.worked_hours = 0
        self.mock_person.weekend.worked_hours = 0
        self.assertEqual(self.mock_person.worked_days(), 0)
        add_worked_hours_helper(self.mock_person.holiday.add_worked_hours, 2, 24)
        add_worked_hours_helper(
            self.mock_person.week.add_worked_hours, 14, 15)
        add_worked_hours_helper(self.mock_person.weekend.add_worked_hours, 4, 24)
        self.assertEqual(self.mock_person.worked_days(), 20)

    def test_total_worked_hours(self):
        self.mock_person.holiday.worked_hours = 0
        self.mock_person.week.worked_hours = 0
        self.mock_person.weekend.worked_hours = 0
        self.assertEqual(self.mock_person.worked_hours(), 0)
        add_worked_hours_helper(self.mock_person.holiday.add_worked_hours, 2, 24)
        add_worked_hours_helper(
            self.mock_person.week.add_worked_hours, 14, 15)
        add_worked_hours_helper(self.mock_person.weekend.add_worked_hours, 4, 24)
        self.assertEqual(self.mock_person.worked_hours(), 354)
