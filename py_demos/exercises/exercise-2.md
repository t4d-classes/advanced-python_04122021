# Exercise 2

## Done in the rates client application

1. Install the "requests" package from PyPi.org.

2. Using the "requests" package API, call the following URL for each date returned from the "business_days" function.

https://api.ratesapi.io/api/2019-01-01?base=USD&symbols=EUR

Iterate over a range of business days, and run the above request for each day.

3. Create a list of text values from each response. The text value is formatted as JSON. Do not parse the JSON. Just put each JSON response in the list.

4. Display each list item in the console.

## Done in the rates app application

5. Compare the output from "api.ratesapi.io" and the API we built in class. What is different? Update the API we coded to output the response in the same structure as "api.ratesapi.io".

6. Test your rates client code with both APIs. Ensure both APIs work with no code changes.