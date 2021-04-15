import pyodbc

# sql express connection
conn_options = [
    "DRIVER={ODBC Driver 17 for SQL Server}",
    r"SERVER=localhost\SQLExpress",
    "DATABASE=ratesapp",
    "Trusted_Connection=yes",
]

# docker connection
# conn_options = [
#     "DRIVER={ODBC Driver 17 for SQL Server}",
#     r"SERVER=localhost,11433",
#     "DATABASE=ratesapp",
#     "UID=sa",
#     "PWD=sqlDBp@ss!",
# ]

# azure connection
# conn_options = [
#     "DRIVER={ODBC Driver 17 for SQL Server}",
#     r"SERVER=pythonclass.database.windows.net",
#     "DATABASE=ratesapp",
#     "UID=pythonclassuser",
#     "PWD=sqlDBp@ss!",
# ]

conn_string = ";".join(conn_options)

with pyodbc.connect(conn_string) as con:

    # lots_of_rates = [
    #     ('2021-01-07', 'EUR', 0.9),
    #     ('2021-01-08', 'EUR', 0.8),
    #     ('2021-01-09', 'EUR', 0.7),
    #     ('2021-01-10', 'EUR', 0.9),
    #     ('2021-01-11', 'EUR', 0.85),
    # ]

    # sql = " ".join([
    #     "insert into rates (ClosingDate, CurrencySymbol, ExchangeRate)",
    #     "values (?, ?, ?)",
    # ])

    # for rate in lots_of_rates:
    #     con.execute(sql, rate)

    # with con.cursor() as cur:
    #     cur.executemany(sql, lots_of_rates)

    rates = con.execute("select CurrencySymbol as currency_symbol from rates")

    for rate in rates:
        # print(rate[2])
        print(rate.currency_symbol)