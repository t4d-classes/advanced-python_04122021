from datetime import datetime, timedelta, date
from timedelta_demos.business_days import business_days, business_days_list

# nums = [1,2,3,4,5]

# for num in nums:
#     print(num)

# for index in range(10):
#     print(index)

def main():

    start_date = date(2019, 1, 1)
    end_date = date(2019, 2, 28)

    # for working_day in business_days(start_date, end_date):
    #     print(working_day.strftime("%A, %d %B %Y"))

    business_days_iterator = business_days(start_date, end_date)

    print(next(business_days_iterator))
    print(next(business_days_iterator))
    print(next(business_days_iterator))


    # start = datetime.now()
    # end = start + timedelta(days=4)
    # print(start)
    # print(end)
    # print(end - start)
    # print(end.weekday())


if __name__ == "__main__":
    main()