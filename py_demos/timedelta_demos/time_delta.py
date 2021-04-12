from datetime import datetime, timedelta

# nums = [1,2,3,4,5]

# for num in nums:
#     print(num)

# for index in range(10):
#     print(index)

def main():

    start = datetime.now()

    end = start + timedelta(days=4)

    print(start)
    print(end)

    print(end - start)

    print(end.weekday())


if __name__ == "__main__":
    main()