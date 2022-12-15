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


class Test_WorkdayChecker(unittest.TestCase):
    def setUp(self):
        holiday = stdbygen.Holidays([25,26], 24)
        self.mock_person = stdbygen.Person(
            "John Doe", [20, 30], [3, 2], holiday)

    def test_is_required(self):
        self.assertTrue(self.mock_person.is_required(20))
        self.assertFalse(self.mock_person.is_required(25))

    def test_is_restricted(self):
        self.assertTrue(self.mock_person.is_restricted(3))
        self.assertFalse(self.mock_person.is_restricted(4))


class TEST_Holidays(unittest.TestCase):
    def setUp(self):
        holiday = stdbygen.Holidays([25,26], 24)
        self.mock_person = stdbygen.Person(
            "John Doe", [20, 30], [3, 2], holiday)

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
