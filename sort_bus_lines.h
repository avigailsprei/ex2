#ifndef EX2_REPO_SORTBUSLINES_H
#define EX2_REPO_SORTBUSLINES_H
// write only between #define EX2_REPO_SORTBUSLINES_H and #endif //EX2_REPO_SORTBUSLINES_H

#define NAME_LEN 21
/**
 * Struct to describe bus line info.
 */
typedef struct BusLine
{
    char name[NAME_LEN];
    int distance, duration, frequency;
} BusLine;

typedef enum SortType
{
    DISTANCE,
    DURATION,
    FREQUENCY
} SortType;

/**
 * Sort buses by line name.
 */
void bus_bubble_sort (BusLine *start, BusLine *end);

/**
 * Use quick sort to sort buses by distance, duration or frequency.
 */
void bus_quick_sort (BusLine *start, BusLine *end, SortType sort_type);

/**
 * TODO add documentation
 */
BusLine *partition (BusLine *start, BusLine *end, SortType sort_type);

/**
 * Sort buses by distance, duration or frequency using Insertion Sort.
 */
void bus_insertion_sort (BusLine *start, BusLine *end, SortType sort_type);

/**
 * Sort buses by distance, duration or frequency using Selection Sort.
 */
void bus_selection_sort (BusLine *start, BusLine *end, SortType sort_type);
// write only between #define EX2_REPO_SORTBUSLINES_H and #endif //EX2_REPO_SORTBUSLINES_H
#endif //EX2_REPO_SORTBUSLINES_H
