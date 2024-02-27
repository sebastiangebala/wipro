## Solution Overview
This project provides a scalable solution for processing large-scale financial instrument data, capable of calculating various statistics such as mean, median, and sum of the newest N elements for each instrument. The solution is designed utilizing parallel processing and chunked file reading to manage memory usage effectively.

## Design Decisions
**Parallel Processing**: To enhance performance, the solution processes data in parallel using Python's concurrent.futures.ProcessPoolExecutor. This approach allows the utilization of multiple CPU cores, significantly speeding up the computation, especially on large datasets.

**Chunked File Reading**: To avoid memory overload with large files, the solution reads data in manageable chunks. This method ensures that the system's memory is not exhausted, making it possible to process files of any size.

**Database Interaction for Price Adjustment**: A lightweight SQLite database is used to store instrument price multipliers. The solution queries this database to adjust instrument prices dynamically, demonstrating how external factors can influence data processing.

**Caching Database Queries**: To reduce database access load, the solution caches database queries for instrument multipliers. This caching is sensitive to the potential frequent updates to the database, with an invalidation period set to ensure data freshness.

## Running the Solution
Set up the environment:
Ensure Python 3.6+ and SQLite are installed on your system.

## Initialize the database:
Run python database.py to set up the database schema.

## Place your input file:
Ensure your input file is in the project directory and follows the specified format.

## Run the main script:
Execute python main.py to start processing the data. The script expects the input file name and database file as arguments, which are set to sensible defaults.

## Testing the Solution
The solution includes a suite of unit tests that cover the key functionalities, including data processing, database interaction, and statistical calculations. To run the tests:

Navigate to the project directory.
Run pytest or your preferred testing tool configured to discover and execute the test suite.

## Profiling and Optimization
Profiling was conducted to identify bottlenecks in data processing, especially concerning memory usage and CPU time. The following tools and techniques were used:

**Memory Profiler**: Monitored the memory usage during the processing of large files, leading to the implementation of chunked file reading.
**cProfile**: Identified CPU-intensive sections, optimizing them by introducing parallel processing.
Optimizations made based on profiling results include:

Adjusting the chunk size for file reading to balance memory usage and processing speed.
Fine-tuning the number of worker processes in the process pool to match the system's CPU resources.

