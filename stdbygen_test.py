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


    # @property
    # def worked_days(self) -> int:
    #     return self.worked_hours / self.hours

# class MockTests(unittest.TestCase):

#     def setUp(self):
#         stdbygen.set_defined_hours(YML_DICT)
#         self.mock_person = stdbygen.new_person(
#             name="John Doe",
#             required_days=[20, 30],
#             restricted_days=[3, 2],
#             restricted_weekdays=["Mon", "Fri"],
#             holidays=[25, 26],
#             first_weekend={"saturday": "John Doe", "sunday": "Jane Doe"})





# class TEST_Holidays(MockTests):

#     def test_is_on(self):
#         self.assertTrue(self.mock_person.holiday.is_on(25))
#         self.assertFalse(self.mock_person.holiday.is_on(27))

#     def test_add_worked_hours_holiday(self):
#         self.mock_person.holiday.worked_hours = 0
#         total = add_worked_hours_helper(self.mock_person.holiday.add_worked_hours, 2, 24)
#         self.assertEqual(self.mock_person.holiday.worked_hours, total)

#     def test_worked_days_holiday(self):
#         self.mock_person.holiday.worked_hours = 0
#         self.assertEqual(self.mock_person.holiday.worked_days(), 0)
#         add_worked_hours_helper(self.mock_person.holiday.add_worked_hours, 20, 24)
#         self.assertEqual(self.mock_person.holiday.worked_days(), 20)

# class TEST_Weeks(MockTests):

#     def test_is_restricted(self):
#         self.assertTrue(self.mock_person.week.is_restricted("mon"))
#         self.assertFalse(self.mock_person.week.is_restricted("Thu"))

#     def test_add_worked_hours_week(self):
#         self.mock_person.week.worked_hours = 0
#         total = add_worked_hours_helper(self.mock_person.week.add_worked_hours, 2, 15)
#         self.assertEqual(self.mock_person.week.worked_hours, total)

#     def test_worked_days_week(self):
#         self.mock_person.week.worked_hours = 0
#         self.assertEqual(self.mock_person.week.worked_days(), 0)
#         add_worked_hours_helper(self.mock_person.week.add_worked_hours, 20, 15)
#         self.assertEqual(self.mock_person.week.worked_days(), 20)

# class TEST_Weekends(MockTests):
#     def test_add_worked_hours_weekend(self):
#         self.mock_person.weekend.worked_hours = 0
#         total = add_worked_hours_helper(self.mock_person.weekend.add_worked_hours, 2, 24)
#         self.assertEqual(self.mock_person.weekend.worked_hours, total)

#     def test_worked_days_weekend(self):
#         self.mock_person.weekend.worked_hours = 0
#         self.assertEqual(self.mock_person.weekend.worked_days(), 0)
#         add_worked_hours_helper(self.mock_person.weekend.add_worked_hours, 20, 15)
#         self.assertEqual(self.mock_person.weekend.worked_days(), 20)

#     def test_is_on_first(self):

#         self.assertTrue(self.mock_person.weekend.is_on_first("saturday", self.mock_person.name))
#         self.assertFalse(self.mock_person.weekend.is_on_first("sunday", self.mock_person.name))

# class Test_Person(MockTests):
#     def test_total_worked_days(self):
#         self.mock_person.holiday.worked_hours = 0
#         self.mock_person.week.worked_hours = 0
#         self.mock_person.weekend.worked_hours = 0
#         self.assertEqual(self.mock_person.worked_days(), 0)
#         add_worked_hours_helper(self.mock_person.holiday.add_worked_hours, 2, 24)
#         add_worked_hours_helper(
#             self.mock_person.week.add_worked_hours, 14, 15)
#         add_worked_hours_helper(self.mock_person.weekend.add_worked_hours, 4, 24)
#         self.assertEqual(self.mock_person.worked_days(), 20)

#     def test_total_worked_hours(self):
#         self.mock_person.holiday.worked_hours = 0
#         self.mock_person.week.worked_hours = 0
#         self.mock_person.weekend.worked_hours = 0
#         self.assertEqual(self.mock_person.worked_hours(), 0)
#         add_worked_hours_helper(self.mock_person.holiday.add_worked_hours, 2, 24)
#         add_worked_hours_helper(
#             self.mock_person.week.add_worked_hours, 14, 15)
#         add_worked_hours_helper(self.mock_person.weekend.add_worked_hours, 4, 24)
#         self.assertEqual(self.mock_person.worked_hours(), 354)

# class Test_person_list_from_yml(unittest.TestCase):
#     def test_person_list_from_yml(self):
#         person = stdbygen.person_list_from_yml(YML_DICT)
#         self.assertEqual(person[3].name, "Hugo Doe")


# class Test_Agenda(MockTests):
#     def test_agenda_from_ym(self):
#         agenda = stdbygen.new_agenda_from_yml(YML_DICT)
#         self.assertEqual(agenda.current_month.month, 11)
#         self.assertEqual(agenda.current_month.calendar()[0][3], 1)
#         self.assertEqual(agenda.current_month.number_of_days(), 30)

