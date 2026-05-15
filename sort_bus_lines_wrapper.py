import subprocess
import os
import sys

def sort_buses(bus_list: list[dict], sort_by: str) -> list[dict]:
    """
    Sorts a list of bus dictionaries by wrapping the compiled `sort_lines` executable.
    It feeds the data via stdin and parses the sorted data from stdout.
    
    Args:
        bus_list: List of dictionaries with keys 'name', 'distance', 'duration', 'frequency'.
        sort_by: One of 'name', 'distance', 'duration', 'frequency'.
        
    Returns:
        A new list of sorted bus dictionaries.
    """
    if not bus_list:
        return []

    # Map the python friendly 'sort_by' to the executable arguments
    sort_arg_map = {
        'name': 'by_name',
        'distance': 'by_distance',
        'duration': 'by_duration',
        'frequency': 'by_frequency',
        'insertion': 'by_insertion',
        'selection': 'by_selection'
    }
    
    if sort_by not in sort_arg_map:
        raise ValueError(f"Unknown sort_by type: {sort_by}")

    # Prepare the input string for the C program
    input_lines = []
    # 1. Number of lines
    input_lines.append(str(len(bus_list)))
    
    # 2. Each bus line info
    for bus in bus_list:
        name = str(bus['name'])
        if ',' in name or '\n' in name:
            raise ValueError(f"Invalid bus name '{name}': cannot contain commas or newlines.")
        input_lines.append(f"{name},{bus['distance']},{bus['duration']},{bus['frequency']}")
    
    # Join with newlines and add a trailing newline
    input_data = "\n".join(input_lines) + "\n"

    # Define the command to run the executable
    executable = './sort_lines'
    
    # If we are on Windows, we likely need to run the ELF binary via WSL
    if os.name == 'nt':
        cmd = ['wsl', '-e', executable, sort_arg_map[sort_by]]
    else:
        cmd = [executable, sort_arg_map[sort_by]]

    cwd = os.path.dirname(os.path.abspath(__file__))

    # Run the subprocess
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            cwd=cwd
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error running {executable}:\nStdout: {e.stdout}\nStderr: {e.stderr}")

    # Parse the output
    sorted_buses = []
    output_lines = result.stdout.strip().split('\n')
    
    for line in output_lines:
        line = line.strip()
        if not line:
            continue
            
        # Ignore the prompts printed by the C program
        if line.startswith("Enter number of lines") or line.startswith("Enter line info"):
            continue
            
        # Parse the comma-separated sorted output
        parts = line.split(',')
        if len(parts) == 4:
            try:
                sorted_buses.append({
                    'name': parts[0],
                    'distance': int(parts[1]),
                    'duration': int(parts[2]),
                    'frequency': int(parts[3])
                })
            except ValueError:
                # If conversion to int fails, it might be an unexpected line, so skip
                continue

    return sorted_buses
