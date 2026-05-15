from sort_bus_lines_wrapper import sort_buses

def main():
    test_data = [
        {'name': 'a9', 'distance': 500, 'duration': 40, 'frequency': 10},
        {'name': 'z1', 'distance': 100, 'duration': 60, 'frequency': 5},
        {'name': 'b2', 'distance': 900, 'duration': 20, 'frequency': 20},
    ]

    print("Original data:")
    for b in test_data:
        print(b)

    print("\n--- Sorted by Name ---")
    res_name = sort_buses(test_data, 'name')
    for b in res_name:
        print(b)
        
    print("\n--- Sorted by Distance ---")
    res_dist = sort_buses(test_data, 'distance')
    for b in res_dist:
        print(b)
        
    print("\n--- Sorted by Duration ---")
    res_dur = sort_buses(test_data, 'duration')
    for b in res_dur:
        print(b)
        
    print("\n--- Sorted by Frequency ---")
    res_freq = sort_buses(test_data, 'frequency')
    for b in res_freq:
        print(b)

if __name__ == '__main__':
    main()
