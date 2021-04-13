"""Main Module"""
from datetime import date, timedelta
from typing import Generator
import holidays


def business_days(start_date: date,
                  end_date: date) -> Generator[date, None, None]:
    """ determines the business days for a given date range """

    us_holidays = holidays.UnitedStates()

    for num in range((end_date - start_date).days + 1):
        the_date = start_date + timedelta(days=num)
        if (the_date.weekday() < 5) and (the_date not in us_holidays):
            yield the_date


def main() -> None:
    """Main Function"""

    start_date = date(2019, 1, 1)
    end_date = date(2019, 2, 28)

    working_days = business_days(start_date, end_date)

    for working_day in working_days:
        print(working_day.strftime("%A, %d %B %Y"))


if __name__ == '__main__':
    main()
