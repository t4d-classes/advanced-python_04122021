# fully enumerated when completed
# double_nums = [x * 2 for x in range(10)] # list comprehension

# enumerated as it is iterated over
double_nums = (x * 2 for x in range(10)) # generator comprehension

print(double_nums)

for num in double_nums:
    print(num)
