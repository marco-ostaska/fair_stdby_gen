# Fair StandBy On-Call Scheduler

[![test](https://github.com/marco-ostaska/fair_stdby_gen/actions/workflows/test.yml/badge.svg)](https://github.com/marco-ostaska/fair_stdby_gen/actions/workflows/test.yml)

Fair StandBy on-Call Scheduler is a python script that aims to create a fair on-call table using a set of rules:

## Rules
- Try to alternate as possible the days between the list
- Try to avoid a person to work two weekend in a row
- Try to avoid whoever worked on weekend to work on monday


## How to Install

In order to use this script, you will need to download and install [python 3](https://www.python.org/downloads/), alternately you can install [miniconda](https://docs.conda.io/en/latest/miniconda.html)

#### Download and install the code

```
git clone https://github.com/marco-ostaska/fair_stdby_gen
cd fair_stdby_gen
```

#### Install the required python modules

```
pip install -r requirements.txt
```

or
```
pip3 install -r requirements.txt
```

## How to configure

Edit the file `config/config.ymal` *(DO NOT RENAME THIS FILE)* and follow comments instructions as the example below:
 - A lot can be accomplished tunning this file.

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

```
python fair_stdby_gen.py
```

# The Output

### Summary

- **Hours:** the sum of the hours a person would be on-call, where regular weekdays = 15 hors. Weekends and holidays = 24 hours
- **Days:** number of days a person would be on call
- **15h day:** number of regular week days a person would be on call
- **24h day:** number of 24h week days (weekends and holidays) a person would be on call

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

## Limitations

- Need to have at least 3 people on the list.
- Depending on how many restrictions configured you may fall in a infinite loop, because the conditions could not be met. In case this happens hit `ctrl + c` to kill the script.


