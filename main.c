#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "sort_bus_lines.h"
#include "test_bus_lines.h"

typedef enum Action
{
    BY_DISTANCE,
    BY_DURATION,
    BY_FREQUENCY,
    BY_NAME,
    BY_INSERTION,
    BY_SELECTION,
    TEST,
    UNDEFINED
} Action;

typedef struct StatusOrAction
{
    Action action;
    int status;
} StatusOrAction;

#define USAGE_ERROR_MSG "Usage: ./sort_lines <by_duration/by_distance/by_frequency/by_name/test>.\n"
#define ENTER_NUM_OF_LINES_MSG "Enter number of lines. Then enter\n"
#define ENTER_LINE_INFO_MSG "Enter line info. Then enter\n"
#define NUM_OF_LINES_ERR_MGS "Error: number of lines must be whole number and greater than zero.\n"
#define LINE_NAME_ERROR_MSG "Error: bus name should contains only digit and small chars\n"
#define DISTANCE_ERROR_MSG "Error: distance should be an integer between 0 and 1000 (includes)\n"
#define DURATION_ERROR_MSG "Error: duration should be an integer between 10 and 100 (includes)\n"
#define FREQUENCY_ERROR_MSG "Error: frequency should be an integer between 1 and 50 (includes)\n"
#define TEST_I_PASSED "TEST %d PASSED: Succes\n"
#define TEST_FAILED_DISTANCE "TEST 1 FAILED: Not sorted by distance\n"
#define TEST_FAILED_DURATION "TEST 3 FAILED: Not sorted by duration\n"
#define TEST_FAILED_FREQUENCY "TEST 5 FAILED: Not sorted by frequncy\n"
#define TEST_FAILED_NAME "TEST 7 FAILED: Not sorted by name\n"
#define TEST_I_FAILED "Test %d FAILED: Arrays are not equal\n"
#define MAX_LINE_LENGTH 60
#define MAX_NAME_LENGTH 20
#define DISTANCE_MAX 1000
#define DURATION_MIN 10
#define DURATION_MAX 100
#define FREQUENCY_MAX 50
#define IS_EQUAL_1 2
#define IS_EQUAL_2 4
#define IS_EQUAL_3 6
#define IS_EQUAL_4 8
#define BASE 10

StatusOrAction get_requested_action(int argc, char *argv[])
{
    StatusOrAction action;
    if (argc != 2)
    {
        action.status = 1;
        action.action = UNDEFINED;
        return action;
    }

    if (strcmp(argv[1], "by_distance") == 0)
    {
        action.action = BY_DISTANCE;
        action.status = 0;
    } else if (strcmp(argv[1], "by_duration") == 0)
    {
        action.action = BY_DURATION;
        action.status = 0;
    } else if (strcmp(argv[1], "by_name") == 0)
    {
        action.action = BY_NAME;
        action.status = 0;
    } else if (strcmp(argv[1], "by_frequency") == 0)
    {
        action.action = BY_FREQUENCY;
        action.status = 0;
    } else if (strcmp(argv[1], "by_insertion") == 0)
    {
        action.action = BY_INSERTION;
        action.status = 0;
    } else if (strcmp(argv[1], "by_selection") == 0)
    {
        action.action = BY_SELECTION;
        action.status = 0;
    } else if (strcmp(argv[1], "test") == 0)
    {
        action.action = TEST;
        action.status = 0;
    } else
    {
        action.status = 1;
        action.action = UNDEFINED;
    }
    return action;
}

int get_number_of_lines()
{
    int number_of_lines = -1;
    char buffer[MAX_LINE_LENGTH];


    while (number_of_lines == -1) {
        printf(ENTER_NUM_OF_LINES_MSG);
        if (fgets(buffer, sizeof(buffer), stdin) == NULL)
        {
            break;
        }
        char *endptr;
        long temp_val = strtol(buffer, &endptr, BASE);

        if (endptr != buffer)
            {
            while (isspace((unsigned char)*endptr))
            {
                endptr++;
            }
            if (*endptr == '\0' && temp_val > 0)
            {
                number_of_lines = (int)temp_val;
            }
        }
        if (number_of_lines == -1) {
            printf(NUM_OF_LINES_ERR_MGS);
        }
    }
    return number_of_lines;
}

bool validate_line_name(const char* line_name)
{
    if (line_name == NULL || line_name[0] == '\0')
    {
        return false;
    }
    if (strlen(line_name) > MAX_NAME_LENGTH)
    {
        return false;
    }
    for (size_t i = 0; i < strlen(line_name); i++)
    {
        if (!islower(line_name[i]) && !isdigit(line_name[i]))
        {
            return false;
        }
    }
    return true;
}

bool is_within_range(int number, int min, int max)
{
    return (min <= number && number <= max) != 0;
}

bool validate_distance(const char* distance_str)
{
    if (distance_str == NULL) {return false;}
    char *endptr;
    long val = strtol(distance_str, &endptr, BASE);
    return is_within_range((int)val, 0, DISTANCE_MAX);
}

bool validate_duration(const char* duration_str)
{
    if (duration_str == NULL) {return false;}
    char *endptr;
    long val = strtol(duration_str, &endptr, BASE);
    return is_within_range((int)val, DURATION_MIN, DURATION_MAX);
}

bool validate_frequency(const char* frequency_str)
{
    if (frequency_str == NULL) {return false;}
    char *endptr;
    long val = strtol(frequency_str, &endptr, BASE);
    return is_within_range((int)val, 1, FREQUENCY_MAX);
}

int get_buses_info(BusLine *bus_array, int requested_number_of_lines)
{
    int number_of_buses = 0;
    char buffer[MAX_LINE_LENGTH];
    while (number_of_buses < requested_number_of_lines)
    {
        printf("%s", ENTER_LINE_INFO_MSG);
        if (fgets(buffer, sizeof(buffer), stdin) != NULL)
        {
            char * line_name = strtok(buffer, ",");
            if (!validate_line_name(line_name))
            {
                printf("%s", LINE_NAME_ERROR_MSG);
                continue;
            }
            char * distance_str = strtok(NULL, ",");
            if (!validate_distance(distance_str))
            {
                printf("%s", DISTANCE_ERROR_MSG);
                continue;
            }
            char * duration_str = strtok(NULL, ",");
            if (!validate_duration(duration_str))
            {
                printf("%s", DURATION_ERROR_MSG);
                continue;
            }
            char * frequency_str = strtok(NULL, "\n");
            if (!validate_frequency(frequency_str))
            {
                printf("%s", FREQUENCY_ERROR_MSG);
                continue;
            }
            char *endptr;
            long distance = strtol(distance_str, &endptr, BASE);
            long duration = strtol(duration_str, &endptr, BASE);
            long frequncy = strtol(frequency_str, &endptr, BASE);
            BusLine line = {.distance = (int)distance, .duration = (int)duration, .frequency = (int)frequncy};
            strcpy(line.name, line_name);
            bus_array[number_of_buses] = line;
            number_of_buses++;
        }
        else {
            break;
        }
    }
    return number_of_buses;
}

void print_sorted_array(BusLine* bus_array, int number_of_lines)
{
    for (int i=0; i<number_of_lines; i++)
    {
        printf("%s,%d,%d,%d\n", bus_array[i].name, bus_array[i].distance, bus_array[i].duration, bus_array[i].frequency);
    }
}

void print_is_equal_test_results(const BusLine* start1, const BusLine* end1, const BusLine* start2, const BusLine* end2, int test_num)
{
    if (is_equal(start1,end1,start2,end2))
    {
        printf(TEST_I_PASSED, test_num);
    } else
    {
        printf(TEST_I_FAILED, test_num);
    }
}

void run_tests(BusLine *bus_array, int number_of_lines)
{
    BusLine* copied_bus_array = malloc(sizeof(BusLine) * number_of_lines);
    if (copied_bus_array == NULL) {
        return;
    }
    for (int i=0; i<number_of_lines; i++) {
        copied_bus_array[i] = bus_array[i];
    }

    bus_quick_sort(bus_array, bus_array + number_of_lines, DISTANCE);
    if (is_sorted_by_distance(bus_array, bus_array + number_of_lines)) {
        printf("TEST 1 PASSED: Succes\n");
    } else {
        printf(TEST_FAILED_DISTANCE);
    }
    print_is_equal_test_results(bus_array, bus_array + number_of_lines, copied_bus_array, copied_bus_array + number_of_lines, IS_EQUAL_1);

    bus_quick_sort(bus_array, bus_array + number_of_lines, DURATION);
    if (is_sorted_by_duration(bus_array, bus_array + number_of_lines)) {
        printf("TEST 3 PASSED: Succes\n");
    } else {
        printf(TEST_FAILED_DURATION);
    }
    print_is_equal_test_results(bus_array, bus_array + number_of_lines, copied_bus_array, copied_bus_array + number_of_lines, IS_EQUAL_2);

    bus_quick_sort(bus_array, bus_array + number_of_lines, FREQUENCY);
    if (is_sorted_by_frequency(bus_array, bus_array + number_of_lines)) {
        printf("TEST 5 PASSED: Succes\n");
    } else {
        printf(TEST_FAILED_FREQUENCY);
    }
    print_is_equal_test_results(bus_array, bus_array + number_of_lines, copied_bus_array, copied_bus_array + number_of_lines, IS_EQUAL_3);

    bus_bubble_sort(bus_array, bus_array + number_of_lines);
    if (is_sorted_by_name(bus_array, bus_array + number_of_lines)) {
        printf("TEST 7 PASSED: Succes\n");
    } else {
        printf(TEST_FAILED_NAME);
    }
    print_is_equal_test_results(bus_array, bus_array + number_of_lines, copied_bus_array, copied_bus_array + number_of_lines, IS_EQUAL_4);

    free(copied_bus_array);
}

int main (int argc, char *argv[])
{
    StatusOrAction status_or_action = get_requested_action(argc, argv);
    if (status_or_action.status == 1) {
        printf("%s", USAGE_ERROR_MSG);
        return EXIT_FAILURE;
    }

    int number_of_lines = get_number_of_lines();


    BusLine* bus_array = malloc(sizeof(BusLine) * number_of_lines);
    if (bus_array == NULL) {
        return EXIT_FAILURE;
    }

    number_of_lines = get_buses_info(bus_array, number_of_lines);

    // perform requested action on lines.
    switch (status_or_action.action) {
        case BY_NAME:
            bus_bubble_sort(bus_array, bus_array + number_of_lines);
            print_sorted_array(bus_array, number_of_lines);
            break;
        case BY_DISTANCE:
            bus_quick_sort(bus_array, bus_array + number_of_lines, DISTANCE);
            print_sorted_array(bus_array, number_of_lines);
            break;
        case BY_FREQUENCY:
            bus_quick_sort(bus_array, bus_array + number_of_lines, FREQUENCY);
            print_sorted_array(bus_array, number_of_lines);
            break;
        case BY_DURATION:
            bus_quick_sort(bus_array, bus_array + number_of_lines, DURATION);
            print_sorted_array(bus_array, number_of_lines);
            break;
        case BY_INSERTION:
            bus_insertion_sort(bus_array, bus_array + number_of_lines, DISTANCE); // Default to distance for insertion
            print_sorted_array(bus_array, number_of_lines);
            break;
        case BY_SELECTION:
            bus_selection_sort(bus_array, bus_array + number_of_lines, DISTANCE); // Default to distance for selection
            print_sorted_array(bus_array, number_of_lines);
            break;
        case TEST:
            run_tests(bus_array, number_of_lines);
        default:
            break;
    }

    free(bus_array);
    return EXIT_SUCCESS;
}
