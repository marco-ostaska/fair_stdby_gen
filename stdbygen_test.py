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
            "required_days": [2, 25],
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
            "required_days": [20],
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
            "restricted_weekdays": ["mon","sat"],
            "restricted_days": [],
            "required_days": [],
            "holidays": []
        }
    ]
}


def add_worked_hours_helper(func, days, hours_to_sum):
    [func() for _ in range(days)]
    return len(range(days)) * hours_to_sum


# class Test_PreDefinedHours(unittest.TestCase):
#     def setUp(self) -> None:
#         pre_defined_hours = stdbygen.PreDefinedHours(allowed=186,week=15,weekend=24,holiday=24)

#     def test_set_PreDefinedHours(self):
#         self.assertEqual(stdbygen.DefinedHours.allowed, 186)
#         self.assertEqual(stdbygen.DefinedHours.week, 15)




class Test_WorkDayCalculator(unittest.TestCase):
    def setUp(self) -> None:
        pd_hours = stdbygen.PreDefinedHours(allowed=186,week=15,weekend=24,holiday=24)
        self.holidays = stdbygen.Holidays(days=[25,30], calc=pd_hours)
        self.weekends = stdbygen.Weekends(first_weekend=YML_DICT["first_weekend"],  calc=pd_hours)
        self.calculator = stdbygen.WorkDayCalculator(15)


    def test_add_worked_hours(self):
        total = add_worked_hours_helper(self.calculator.add_worked_hours, 2, 15)
        self.assertEqual(self.calculator.worked_hours, total)

    def test_worked_days(self):
        self.assertEqual(self.calculator.worked_days, 0)
        add_worked_hours_helper(self.calculator.add_worked_hours, 20, 15)
        self.assertEqual(self.calculator.worked_days, 20)

class Test_holidays(unittest.TestCase):
    def setUp(self) -> None:
        calc = stdbygen.WorkDayCalculator(hours_to_compute=24)
        self.holidays = stdbygen.Holidays(days=[25,30], calc=calc)
        self.weekends = stdbygen.Weekends(first_weekend=YML_DICT["first_weekend"],  calc=calc)
        self.calculator = stdbygen.WorkDayCalculator(15)

    def test_add_worked_hours(self):
        total = add_worked_hours_helper(self.holidays.calc.add_worked_hours, 2, 24)
        self.assertEqual(self.holidays.calc.worked_hours, total)

    def test_worked_days_holiday(self):
        self.assertEqual(self.holidays.calc.worked_days, 0)
        add_worked_hours_helper(self.holidays.calc.add_worked_hours, 20, 24)
        self.assertEqual(self.holidays.calc.worked_days, 20)


class Test_WorkDayValidator(unittest.TestCase):
    def setUp(self) -> None:
        pd_hours = stdbygen.PreDefinedHours(allowed=186,week=15,weekend=24,holiday=24)
        holidays = stdbygen.Holidays(days=[25,30], calc=pd_hours)
        weekends = stdbygen.Weekends(first_weekend=YML_DICT["first_weekend"],  calc=pd_hours)
        self.validator = stdbygen.WorkdayValidator(restricted_days=[2,30],
                                                    required_days=[4,8], holidays=holidays,
                                                    weekends=weekends)
    def test_is_required(self):
        self.assertTrue(self.validator.is_required(4))
        self.assertFalse(self.validator.is_required(2))

    def test_is_restricted(self):
        self.assertTrue(self.validator.is_restricted(2))
        self.assertFalse(self.validator.is_restricted(4))

    def test_is_holiday(self):
        self.assertTrue(self.validator.is_holiday(25))
        self.assertFalse(self.validator.is_holiday(1))

    def test_is_on_first_weekend(self):
        self.assertTrue(self.validator.weekends.is_on_first(
            "saturday", "John Doe"))
        self.assertFalse(self.validator.weekends.is_on_first("saturday", "Joao"))



class Test_Person(unittest.TestCase):
    def setUp(self) -> None:
        self.person =stdbygen.new_person_list_from_yml(YML_DICT)

    def test_person_list_from_yml(self):

        self.assertEqual(self.person[0].name, "John Doe")

    def test_sort_list_index_by_hours(self):
        # Create a list of Person objects with different worked hours
        self.person[0].worked_hours=10
        self.person[1].worked_hours=20
        self.person[2].worked_hours=5
        self.person[3].worked_hours=15
        self.person[4].worked_hours=15

        # Check that the function returns the correct indices
        self.assertEqual(stdbygen.sort_list_index_by_hours(self.person), [2, 0, 3, 4, 1])

class Test_Agenda(unittest.TestCase):
    def setUp(self) -> None:
        self.person =stdbygen.new_person_list_from_yml(YML_DICT)
        self.agenda = stdbygen.new_agenda_from_yml(YML_DICT)
        self.agenda.set_first_weekend_day("saturday")
        self.agenda.set_first_weekend_day("sunday")
        self.agenda.set_required_days()

    def test_set_first_weekend(self):
        self.assertEqual(self.agenda.calendar[1][0], "John Doe")
        self.assertEqual(self.agenda.calendar[1][1], "Jane Doe")

    def test_set_required_days(self):
        self.agenda.set_required_days()
        self.assertEqual(self.agenda.calendar[0][4], "John Doe")

    def test_update_worked_hours(self):
        self.agenda.update_worked_hours()
        self.assertEqual(self.agenda.person[0].worked_hours, 63)

    def test_get_calendar_idx_for_person(self):
        idx =  self.agenda.get_calendar_idx_for_person("John Doe")
        self.assertEqual(idx, [(0, 4), (1, 0), (3, 6)])
        for i, j in idx:
            self.assertEqual(self.agenda.calendar[i][j], 'John Doe')

