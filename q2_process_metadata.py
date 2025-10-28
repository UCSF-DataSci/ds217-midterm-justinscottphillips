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
    # Read file, split on '=', create dict
    config = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, val = line.split('=', 1)
            config[key.strip()] = val.strip()
    return config

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
    # Implement with if/elif/else
    results = {
        'sample_data_rows': False,
        'sample_data_min': False,
        'sample_data_max': False,
    }

    # sample_data_rows: int and > 0
    try:
        rows = int(config.get('sample_data_rows', 0))
        results['sample_data_rows'] = rows > 0
    except Exception:
        results['sample_data_rows'] = False

    # sample_data_min: int and >= 1
    try:
        var_min = int(config.get('sample_data_min', 0))
        results['sample_data_min'] = var_min >= 1
    except Exception:
        results['sample_data_min'] = False

    # sample_data_max: int and > sample_data_min
    try:
        var_max = int(config.get('sample_data_max', 0))
        if results['sample_data_min']:
            var_min = int(config.get('sample_data_min'))
            results['sample_data_max'] = var_max > var_min
        else:
            results['sample_data_max'] = False
    except Exception:
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
    from pathlib import Path

    # Parse config values (convert strings to int)
    var_rows = int(config.get('sample_data_rows', 100))
    var_min = int(config.get('sample_data_min', 1))
    var_max = int(config.get('sample_data_max', 100))

    if var_max < var_min:
        raise ValueError("sample_data_max must be >= sample_data_min")

    outp = Path(filename)
    outp.parent.mkdir(parents=True, exist_ok=True)

    # Generate random numbers and save to file
    # Use random module with config-specified range
    with outp.open('w', encoding='utf-8') as f:
        for _ in range(var_rows):
            f.write(f"{random.randint(var_min, var_max)}\n")

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
    # Calculate stats
    import statistics

    if not data:
        return {"mean": None, "median": None, "sum": 0, "count": 0}

    cnt = len(data)
    total = sum(data)
    try:
        mean = statistics.mean(data)
    except Exception:
        mean = total / cnt if cnt else None
    try:
        median = statistics.median(data)
    except Exception:
        median = None
    return {"mean": mean, "median": median, "sum": total, "count": cnt}

if __name__ == '__main__':
    # Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    # 
    # Read the generated file and calculate statistics
    # Save statistics to output/statistics.txt
    # Keep TODOs visible above; implement runner below
    import os
    import sys

    cfg_path = 'q2_config.txt'
    if not os.path.exists(cfg_path):
        print(f"Config file '{cfg_path}' not found.", file=sys.stderr)
        sys.exit(1)

    cfg = parse_config(cfg_path)
    validation = validate_config(cfg)
    bad = [k for k, v in validation.items() if not v]
    if bad:
        print('Warning: validation failed for keys:', ', '.join(bad))

    try:
        generate_sample_data('data/sample_data.csv', cfg)
    except Exception as e:
        print('Error generating sample data:', e, file=sys.stderr)
        sys.exit(1)

    # Read generated file and compute statistics
    numbers = []
    data_file = 'data/sample_data.csv'
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as fh:
            for line in fh:
                s = line.strip()
                if not s:
                    continue
                try:
                    numbers.append(int(s))
                except ValueError:
                    try:
                        numbers.append(float(s))
                    except ValueError:
                        continue

    stats = calculate_statistics(numbers)

    os.makedirs('output', exist_ok=True)
    outpath = os.path.join('output', 'statistics.txt')
    with open(outpath, 'w', encoding='utf-8') as outf:
        for k, v in stats.items():
            outf.write(f"{k}: {v}\n")

    print('Wrote', outpath)
