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

    symbol = "RUB"

    # parameterized query
    sql = " ".join([
        "select ClosingDate, CurrencySymbol, ExchangeRate",
        "from Rates",
        "where CurrencySymbol = ?",
    ])

    rates = con.execute(sql,(symbol,))

    for rate in rates:
        print(rate)