"""Main Module"""
from datetime import date, timedelta, datetime
from typing import Generator, TypedDict
import threading
import queue
import json
import pathlib
import csv
import holidays
import requests


class Rate(TypedDict):
    """ rate typed dict type """
    date: date
    eur: float


raw_rate_responses_done = threading.Event()
process_rates_done = threading.Event()


def business_days(start_date: date,
                  end_date: date) -> Generator[date, None, None]:
    """ determines the business days for a given date range """

    us_holidays = holidays.UnitedStates()

    for num in range((end_date - start_date).days + 1):
        the_date = start_date + timedelta(days=num)
        if (the_date.weekday() < 5) and (the_date not in us_holidays):
            yield the_date


def get_rates_by_day(business_day: date, rates: queue.Queue[str]) -> None:
    """ get rates from api for a given day """
    day_fmt = business_day.strftime("%Y-%m-%d")

    rate_url = "".join([
        "https://api.ratesapi.io/api/",
        # "http://127.0.0.1:5000/api/",
        day_fmt,
        "?base=USD&symbols=EUR",
    ])

    response = requests.request("GET", rate_url)
    rates.put(response.text)


def process_rates(raw_rates: queue.Queue[str],
                  processed_rates: queue.Queue[Rate]) -> None:
    """ process rates """
    while True:

        try:
            raw_rate_data = raw_rates.get(timeout=1)
            rate = json.loads(raw_rate_data)
            processed_rates.put({
                "date": datetime.strptime(rate["date"], "%Y-%m-%d").date(),
                "eur": rate["rates"]["EUR"]
            })
            raw_rates.task_done()
        except queue.Empty:
            if raw_rate_responses_done.is_set():
                break
            else:
                continue


def save_rates(processed_rates: queue.Queue[Rate]) -> None:
    """ saves rates to a csv file """

    with open(pathlib.Path("output", "euro-rates.csv"),
              "w", newline="\n") as rates_file:

        rates_csv = csv.writer(rates_file)
        while True:
            try:
                rate = processed_rates.get(timeout=1)
                rates_csv.writerow(rate.values())
                processed_rates.task_done()
            except queue.Empty:
                if process_rates_done.is_set():
                    break
                else:
                    continue


def main() -> None:
    """Main Function"""

    raw_rate_responses: queue.Queue[str] = queue.Queue()
    processed_rates: queue.Queue[Rate] = queue.Queue()

    get_rate_threads: list[threading.Thread] = []

    start_date = date(2019, 1, 1)
    end_date = date(2019, 2, 28)

    for business_day in business_days(start_date, end_date):
        get_rate_thread = threading.Thread(
            target=get_rates_by_day, args=(
                business_day, raw_rate_responses))
        get_rate_thread.start()
        get_rate_threads.append(get_rate_thread)

    process_rates_thread = threading.Thread(
        target=process_rates,
        args=(
            raw_rate_responses,
            processed_rates))
    process_rates_thread.start()

    save_rates_thread = threading.Thread(
        target=save_rates,
        args=(processed_rates,))
    save_rates_thread.start()

    for get_rate_thread in get_rate_threads:
        get_rate_thread.join()

    raw_rate_responses_done.set()

    process_rates_thread.join()

    process_rates_done.set()

    save_rates_thread.join()


if __name__ == '__main__':
    main()
