from datetime import timedelta, date, datetime
from typing import Generator
from typing import TypedDict
import requests
import holidays
import json
import pathlib
import csv
import time


class Rate(TypedDict):
    date: date
    eur: float


raw_rate_responses: list[str] = []
processed_rates: list[Rate] = []


def business_days(start_date: date,
                  end_date: date) -> Generator[date, None, None]:
    us_holidays = holidays.UnitedStates()
    for n in range((end_date - start_date).days + 1):
        the_date = start_date + timedelta(n)
        if (the_date.weekday() < 5) and (the_date not in us_holidays):
            yield the_date


def get_rates() -> None:
    start_date = date(2019, 1, 1)
    end_date = date(2019, 6, 30)
    for single_date in business_days(start_date, end_date):
        single_date_str = single_date.strftime("%Y-%m-%d")
        url = f"https://api.ratesapi.io/api/{single_date_str}?base=USD&symbols=EUR"
        response = requests.request("GET", url)
        raw_rate_responses.append(response.text)


def process_rates() -> None:

    for rate_data in raw_rate_responses:
        rate = json.loads(rate_data)
        processed_rates.append({
            "date": datetime.strptime(rate["date"], "%Y-%m-%d").date(),
            "eur": rate["rates"]["EUR"],
        })


def save_rates() -> None:
    with open(pathlib.Path("output", "rates.csv"), "w", newline="\n") as rates_file:
        rates_csv = csv.writer(rates_file)
        for rate in processed_rates:
            rates_csv.writerow(rate.values())


def main() -> None:

    get_rates()
    process_rates()
    save_rates()


if __name__ == "__main__":
    start_time = time.time()
    main()
    total_time = time.time() - start_time

    print(total_time)
