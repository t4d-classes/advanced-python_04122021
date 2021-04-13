Exercise 3

# rate client application

1. Add profiling code to the previous lab exercise. Run the code and record the total time to execute the code.

2. Copy the current `__main__.py` file, and rename it to `__main__single.py`. Upgrade the `__main__.py` file implementation to use threads for the I/O bound part of the program. Remember, append operations on the list object are thread-safe.

3. Run the threaded version. Record the time to complete using the time diff profile technique that was demonstrated. Was there a difference? Why did the difference occur?

4. Run the rates client against the official internet version and your local rates app version.