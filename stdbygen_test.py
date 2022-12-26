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


# class Test_Agenda(MockTests):
#     def test_agenda_from_ym(self):
#         agenda = stdbygen.new_agenda_from_yml(YML_DICT)
#         self.assertEqual(agenda.current_month.month, 11)
#         self.assertEqual(agenda.current_month.calendar()[0][3], 1)
#         self.assertEqual(agenda.current_month.number_of_days(), 30)

