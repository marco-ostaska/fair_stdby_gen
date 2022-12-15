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


class Test_WorkdayChecker(unittest.TestCase):
    def setUp(self):
        self.mock_person = stdbygen.Person("John Doe", [20, 30], [3, 2])

    def test_is_required(self):
        self.assertTrue(self.mock_person.is_required(20))
        self.assertFalse(self.mock_person.is_required(25))

    def test_is_restricted(self):
        self.assertTrue(self.mock_person.is_restricted(3))
        self.assertFalse(self.mock_person.is_restricted(4))
