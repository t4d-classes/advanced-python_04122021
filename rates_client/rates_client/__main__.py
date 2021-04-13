"""Main Module"""
from datetime import date, timedelta
from typing import Generator
import threading
import holidays
import requests


def business_days(start_date: date,
                  end_date: date) -> Generator[date, None, None]:
    """ determines the business days for a given date range """

    us_holidays = holidays.UnitedStates()

    for num in range((end_date - start_date).days + 1):
        the_date = start_date + timedelta(days=num)
        if (the_date.weekday() < 5) and (the_date not in us_holidays):
            yield the_date


def get_rates_by_day(business_day: date, rates: list[str]) -> None:
    """ get rates from api for a given day """
    day_fmt = business_day.strftime("%Y-%m-%d")

    rate_url = "".join([
        "https://api.ratesapi.io/api/",
        # "http://127.0.0.1:5000/api/",
        day_fmt,
        "?base=USD&symbols=EUR",
    ])

    response = requests.request("GET", rate_url)
    rates.append(response.text)


def main() -> None:
    """Main Function"""

    rates: list[str] = []
    get_rate_threads: list[threading.Thread] = []

    start_date = date(2019, 1, 1)
    end_date = date(2019, 2, 28)

    for business_day in business_days(start_date, end_date):
        get_rate_thread = threading.Thread(
            target=get_rates_by_day, args=(
                business_day, rates))
        get_rate_thread.start()
        get_rate_threads.append(get_rate_thread)

    for get_rate_thread in get_rate_threads:
        get_rate_thread.join()

    for rate in rates:
        print(rate)

    print(len(rates))


if __name__ == '__main__':
    main()
