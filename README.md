# Fair StandBy On-Call Scheduler

The Fair Standby On-Call Scheduler is a Python script that generates a fair on-call schedule based on a set of rules. The schedule takes into account holidays, weekends, and the preferences of each person on the schedule.

## How to Install

Before using the script, you will need to have [python 3](https://www.python.org/downloads/) installed on your computer. Alternatively, you can install [miniconda](https://docs.conda.io/en/latest/miniconda.html), which includes Python and a suite of tools for working with data and scientific computing.

To download and install the script, follow these steps:

1. Open a terminal or command prompt.
2. Use git to clone the repository:

```
git clone https://github.com/marco-ostaska/fair_stdby_gen
cd fair_stdby_gen
```
3. Install the required python modules

```
pip install -r requirements.txt
```

or
```
pip3 install -r requirements.txt
```

## How to configure

Before running the script, you will need to configure the config/config.ymal file. This file contains information about the year and month for which the schedule will be generated, as well as a list of holidays and the people who will be on the schedule.

To configure the script, open config/config.ymal in a text editor and follow the instructions in the file. **Important: Do not rename this file.**

Here is an example of the config.ymal file:


```yaml
# Settings file in YAML
# DO NOT RENAME THIS FILE

# Year in YYYY format
year: 2022

# Month in mm format
month: 11

# List of holidays in this month
# Enter an empty list in case of none
Holidays:
    - 2
    - 15
    - 20

# List of people that will be on the standby schedule
# Should be at leat two
People:
    - { Name: "Person 1",            # Person Name
       idx: 0,                       # Person index, must be unique and sequential
       week_restriction: [],         # Week restrictions (Days of the week a person can´t work). (0=Monday, 6=Sunday)
       day_restriction: [],          # List of days a person cant work, useful for vacation
       wanted_days: [] }             # A list of days a person wants to work


    - { Name: "Person 2",
       idx: 1,
       week_restriction: [],
       day_restriction: [],
       wanted_days: [] }

    - { Name: "Person 3",
       idx: 2,
       week_restriction: [],
       day_restriction: [],
       wanted_days: [] }


    - { Name: "Person 4",
       idx: 3,
       week_restriction: [2, 3],
       day_restriction: [],
       wanted_days: [] }

    - { Name: "Person 5",
       idx: 4,
       week_restriction: [],
       day_restriction: [15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
       wanted_days: [] }


# If someone worked last Saturday use this parameter with the person name
last_saturday: "Person 1"
# If someone worked last Saturday use this parameter with the person name
last_sunday: "Person 4"
```

## How to use

To generate the on-call schedule, open a terminal or command prompt and navigate to the directory where the script was installed. Then, run the following command:

```
python fair_stdby_gen.py
```

# The Output

The output of the script is a summary table showing the following information for each person on the schedule:

- **Hours:** The total number of hours that the person will be on call. Regular weekdays are 15 hours and weekends and holidays are 24 hours.
- **Days:** The total number of days that the person will be on call.
- **15h day:** The number of regular weekdays that the person will be on call.
- **24h day:** The number of 24-hour days (weekends and holidays) that the person will be on call.

Here is an example of the output:

```
+------------+---------+--------+-----------+-----------+
| Person 1   |   Hours |   Days |   15h day |   24h day |
|------------+---------+--------+-----------+-----------|
|            |     132 |      7 |         4 |         3 |
+------------+---------+--------+-----------+-----------+

+------------+---------+--------+-----------+-----------+
| Person 2   |   Hours |   Days |   15h day |   24h day |
|------------+---------+--------+-----------+-----------|
|            |     147 |      8 |         5 |         3 |
+------------+---------+--------+-----------+-----------+

+------------+---------+--------+-----------+-----------+
| Person 3   |   Hours |   Days |   15h day |   24h day |
|------------+---------+--------+-----------+-----------|
|            |     123 |      7 |         5 |         2 |
+------------+---------+--------+-----------+-----------+

+------------+---------+--------+-----------+-----------+
| Person 4   |   Hours |   Days |   15h day |   24h day |
|------------+---------+--------+-----------+-----------|
|            |      84 |      5 |         4 |         1 |
+------------+---------+--------+-----------+-----------+

+------------+---------+--------+-----------+-----------+
| Person 5   |   Hours |   Days |   15h day |   24h day |
|------------+---------+--------+-----------+-----------|
|            |      54 |      3 |         2 |         1 |
+------------+---------+--------+-----------+-----------+

```

### The schedule

```
+--------------+------------------------+--------------+------------------------+-----------------------+--------------+--------------+
| Saturday     | Sunday                 | Monday       | Tuesday                | Wednesday             | Thursday     | Friday       |
|--------------+------------------------+--------------+------------------------+-----------------------+--------------+--------------|
|              |                        |              | 1. Person 1            | 2. Person 2 (holiday) | 3. Person 3  | 4. Person 4  |
| 5. Person 5  | 6. Person 1            | 7. Person 2  | 8. Person 3            | 9. Person 4           | 10. Person 5 | 11. Person 1 |
| 12. Person 2 | 13. Person 3           | 14. Person 5 | 15. Person 1 (holiday) | 16. Person 2          | 17. Person 3 | 18. Person 4 |
| 19. Person 1 | 20. Person 4 (holiday) | 21. Person 2 | 22. Person 3           | 23. Person 4          | 24. Person 1 | 25. Person 2 |
| 26. Person 3 | 27. Person 2           | 28. Person 1 | 29. Person 2           | 30. Person 3          |              |              |
+--------------+------------------------+--------------+------------------------+-----------------------+--------------+--------------+

```

## Rules 

The script follows these rules when generating the on-call schedule:

- Try to alternate as possible the days between the list
- Try to avoid a person to work two weekends in a row
- Try to avoid whoever worked on the weekend to work on Monday

## Troubleshooting

If you have any issues with the script, check the following:

- Make sure you have Python 3 and the required modules installed.
- Make sure you are using the correct syntax when running the script.
- Make sure the `config/config.ymal` file is properly formatted and that all required fields are filled out.

## Limitations

- Need to have at least 3 people on the list.
- Depending on how many restrictions configured you may fall in a infinite loop, because the conditions could not be met. In case this happens hit `ctrl + c` to kill the script.
- The script can only generate schedules for one month at a time. If you need a schedule for multiple months, you will need to run the script multiple times.
- The script relies on the config/config.ymal file for configuration. If the file is not properly formatted or required fields are missing, the script may not work as intended.
- The script does not check for conflicts between the schedules of different people. For example, if two people have the same day off on their wanted days list, the script will not be able to resolve this conflict and the resulting schedule may not be fair.
- The script does not take into account the workload or availability of each person. If one person is unable to work on certain days due to other commitments, this will not be reflected in the generated schedule.
- The script does not account for holidays or other days off that are not listed in the config/config.ymal file. If you need to exclude these days from the schedule, you will need to manually adjust the wanted days lists for each person.
- The script does not account for any additional constraints or preferences that may be relevant to generating the schedule. For example, if you want to ensure that certain people work together on the same days, the script will not be able to take this into account.
- The script does not allow for different shift lengths or schedules for different people. It assumes that everyone works the same number of hours per day and follows the same schedule.
- The script does not automatically update the on-call schedule if changes are made to the configuration file. If you need to update the schedule, you will need to re-run the script.


