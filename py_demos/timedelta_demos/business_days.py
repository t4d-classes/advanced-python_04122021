from datetime import datetime, timedelta, date
import holidays

def business_days_list(start_date, end_date):

    working_days = []

    us_holidays = holidays.UnitedStates()

    for num in range((end_date - start_date).days + 1):
        the_date = start_date + timedelta(days=num)
        if (the_date.weekday() < 5) and (the_date not in us_holidays):
            print("appending")
            working_days.append(the_date)

    return working_days

def business_days(start_date, end_date):

    us_holidays = holidays.UnitedStates()

    for num in range((end_date - start_date).days + 1):
        the_date = start_date + timedelta(days=num)
        if (the_date.weekday() < 5) and (the_date not in us_holidays):
            print("yielding")
            yield the_date


def main():

    start_date = date(2019, 1, 1)
    end_date = date(2019, 2, 28)

    working_days = business_days(start_date, end_date)

    for working_day in working_days:
        print(working_day.strftime("%A, %d %B %Y"))

print(__name__)
if __name__ == "__main__":
    main()