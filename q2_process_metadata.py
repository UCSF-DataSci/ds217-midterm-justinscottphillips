#!/usr/bin/env python3

# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.
def parse_config(filepath: str) -> dict:
    """
    Parse config file (key=value format) into dictionary.

    Args:
        filepath: Path to q2_config.txt

    Returns:
        dict: Configuration as key-value pairs

    Example:
        >>> config = parse_config('q2_config.txt')
        >>> config['sample_data_rows']
        '100'
    """
    # Create dict
    config = {}
    # Open file
    with open(filepath, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            # Split each line by the =
            key, val = line.split('=')
            config[key.strip()] = val.strip()
    return config

"""
Check if the value can be converted to an integer.
"""
def is_int(val) -> bool:
    try:
        int(val)
        return True
    except ValueError:
        return False

def validate_config(config: dict) -> dict:
    """
    Validate configuration values using if/elif/else logic.

    Rules:
    - sample_data_rows must be an int and > 0
    - sample_data_min must be an int and >= 1
    - sample_data_max must be an int and > sample_data_min

    Args:
        config: Configuration dictionary

    Returns:
        dict: Validation results {key: True/False}

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> results = validate_config(config)
        >>> results['sample_data_rows']
        True
    """
    # Create results dict
    results = {}

    # sample_data_rows must be an int and > 0
    if is_int(config['sample_data_rows']) and int(config['sample_data_rows']) > 0:
        results['sample_data_rows'] = True
    else:
        results['sample_data_rows'] = False

    # sample_data_min must be an int and >= 1
    if is_int(config['sample_data_min']) and int(config['sample_data_min']) >= 1:
        results['sample_data_min'] = True
    else:
        results['sample_data_min'] = False

    # sample_data_max must be an int and > sample_data_min
    if is_int(config['sample_data_max']) and int(config['sample_data_max']) > int(config['sample_data_min']):
        results['sample_data_max'] = True
    else:
        results['sample_data_max'] = False

    return results

def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.

    Args:
        filename: Output filename (e.g., 'sample_data.csv')
        config: Configuration dictionary with sample_data_rows, sample_data_min, sample_data_max

    Returns:
        None: Creates file on disk

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    import random

    # Convert strings to int
    var_rows = int(config['sample_data_rows'])
    var_min = int(config['sample_data_min'])
    var_max = int(config['sample_data_max'])

    # Generate random numbers and save to file
    with open(filename, 'w') as file:
        for _ in range(var_rows):
            # Use random module with config-specified range
            file.write(f"{random.randint(var_min, var_max)}\n")

def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.

    Args:
        data: List of numbers

    Returns:
        dict: {mean, median, sum, count}

    Example:
        >>> stats = calculate_statistics([10, 20, 30, 40, 50])
        >>> stats['mean']
        30.0
    """
    import statistics

    count = len(data)
    total = sum(data)
    mean = statistics.mean(data)
    median = statistics.median(data)
    return {
        "mean": mean,
        "median": median,
        "sum": total,
        "count": count
    }

if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    config = parse_config('q2_config.txt')
    validation = validate_config(config)
    print('Validation results:', validation)
    generate_sample_data('data/sample_data.csv', config)    

    # TODO: Read the generated file and calculate statistics
    # Convert generated file to a list
    numbers = []
    with open('data/sample_data.csv', 'r') as sample_file:
        for line in sample_file:
            line = line.strip()
            numbers.append(int(line))
    stats = calculate_statistics(numbers)
    print('Calculated statistics:', stats)

    # TODO: Save statistics to output/statistics.txt
    with open('output/statistics.txt', 'w') as output_file:
        print(f"Mean: {stats['mean']:.1f}", file=output_file)
        print(f"Median: {stats['median']:.1f}", file=output_file)
        print(f"Sum: {stats['sum']:.1f}", file=output_file)
        print(f"Count: {stats['count']:.1f}", file=output_file)
    
    print('Finished writing statistics to output/statistics.txt')
