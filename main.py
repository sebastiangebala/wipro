from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
import os
from database import DatabaseManager 
from calculator import Calculator

def process_instrument_data(instrument_data):
    """
    Process data for a single instrument in a separate process.
    Each process creates its own database connection.
    """
    instrument_name, records, db_file = instrument_data
    db_manager = DatabaseManager(db_file)  # Instantiate DatabaseManager locally
    
    # Fetch the multiplier for the instrument, if it exists
    multiplier = db_manager.get_instrument_modifier(instrument_name)
    if multiplier is None:
        multiplier = 1  # Default to 1 if no multiplier is found
    
    # Apply the multiplier to the values
    adjusted_records = [(d, v * multiplier) for d, v in records]
    
    # Proceed with the original logic, using adjusted_records
    _, adjusted_values = zip(*adjusted_records)  # Extract just the adjusted values for calculations
    result = None
    if instrument_name == 'INSTRUMENT1':
        result = Calculator.calculate_mean(adjusted_values)
    elif instrument_name == 'INSTRUMENT2':
        nov_adjusted_values = [v for d, v in adjusted_records if d.month == 11 and d.year == 2014]
        result = Calculator.calculate_mean(nov_adjusted_values)
    elif instrument_name == 'INSTRUMENT3':
        result = Calculator.calculate_median(adjusted_values)
    else:
        newest_adjusted_values = [v for _, v in adjusted_records[:10]]
        result = Calculator.sum_newest(newest_adjusted_values)
    
    return instrument_name, result


def read_file_in_chunks(filename, chunk_size=10000):
    """
    Generator function to read a file in chunks of lines.
    """
    chunk = []
    with open(filename, 'r') as file:
        for line in file:
            chunk.append(line)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:  # Yield the last chunk if it's not empty
            yield chunk

def parallel_process_chunk(chunk, db_file, current_date):
    """
    Process a chunk of data in parallel.
    """
    data = {}
    for line in chunk:
        parts = line.strip().split(',')
        if len(parts) == 3:
            instrument, date_str, value_str = parts
            date = datetime.strptime(date_str, '%d-%b-%Y').date()
            
            if date <= current_date and date.weekday() < 5:
                value = float(value_str)
                if instrument not in data:
                    data[instrument] = []
                data[instrument].append((date, value))

    # Sort data by date in descending order for each instrument.
    for instrument in data:
        data[instrument] = sorted(data[instrument], key=lambda x: x[0], reverse=True)

    # Use ProcessPoolExecutor to process each instrument's data in parallel
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(process_instrument_data, (instrument, records, db_file)) for instrument, records in data.items()]
        results = [future.result() for future in futures]

    return results

def parallel_process_file(filename, db_file):
    """
    Process the given file in chunks in parallel, considering only business days 
    and dates up to a specified current date.
    """
    current_date = datetime.strptime("19-Dec-2014", "%d-%b-%Y").date()
    aggregated_results = {}

    for chunk in read_file_in_chunks(filename, chunk_size=10000):
        chunk_results = parallel_process_chunk(chunk, db_file, current_date)

        # Aggregate results from each chunk.
        for instrument, result in chunk_results:
            if instrument not in aggregated_results:
                aggregated_results[instrument] = []
            aggregated_results[instrument].append(result)

    # Output the aggregated results with calculation details
    for instrument, results in aggregated_results.items():
        calculation_type = ""  # Initialize the calculation type description
        if instrument == 'INSTRUMENT1':
            calculation_type = "Mean"
        elif instrument == 'INSTRUMENT2':
            calculation_type = "Mean for November 2014"
        elif instrument == 'INSTRUMENT3':
            calculation_type = "Median"
        else:
            calculation_type = "Sum of the newest 10 elements"

        # Format the results list to a string of results separated by commas, rounded to 2 decimal places
        results_str = ", ".join(f"{result:.2f}" for result in results)

        print(f"{instrument} ({calculation_type}): [{results_str}]")

if __name__ == "__main__":
    db_file = "instrument_data.db"
    input_file = "instrument_prices.txt"
    parallel_process_file(input_file, db_file)
