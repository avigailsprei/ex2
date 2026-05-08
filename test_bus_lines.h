#ifndef EX2_REPO_TESTBUSLINES_H
#define EX2_REPO_TESTBUSLINES_H
// write only between #define EX2_REPO_TESTBUSLINES_H and #endif //EX2_REPO_TESTBUSLINES_H
#include "sort_bus_lines.h"

/**
 *  Checks that the array is sorted by bus distance.
 */
int is_sorted_by_distance (const BusLine *start, const BusLine *end);

/**
 * Checks that the array is sorted by bus duration.
 */
int is_sorted_by_duration (const BusLine *start, const BusLine *end);

/**
 * Checks that the array is sorted by bus frequency.
 */
int is_sorted_by_frequency (const BusLine *start, const BusLine *end);

/**
 * Checks that the array is sorted by names, lexicographically.
 */
int is_sorted_by_name (const BusLine *start, const BusLine *end);

/**
 * Checks that both arrays have the same length and all names are equal.
 */
int is_equal (const BusLine *start_sorted,
              const BusLine *end_sorted,
              const BusLine *start_original,
              const BusLine *end_original);
// write only between #define EX2_REPO_TESTBUSLINES_H and #endif //EX2_REPO_TESTBUSLINES_H
#endif //EX2_REPO_TESTBUSLINES_H
