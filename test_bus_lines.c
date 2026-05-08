#include "test_bus_lines.h"
#include <string.h>

#define MAX_NAME_LENGTH 21

int is_sorted_by_distance (const BusLine *start, const BusLine *end)
{
    for (const BusLine *current = start; current < end -1; current++) {
        if (current->distance > (current+1)->distance) {
            return 0;
        }
    }

    return 1;
}

int is_sorted_by_duration (const BusLine *start, const BusLine *end)
{
    for (const BusLine *current = start; current < end -1; current++) {
        if (current->duration > (current+1)->duration) {
            return 0;
        }
    }

    return 1;
}

int is_sorted_by_frequency (const BusLine *start, const BusLine *end)
{
    for (const BusLine *current = start; current < end -1; current++) {
        if (current->frequency > (current+1)->frequency) {
            return 0;
        }
    }

    return 1;
}

int is_sorted_by_name (const BusLine *start, const BusLine *end)
{
    for (const BusLine *current = start; current < end -1; current++) {
        if (strcmp(current->name, (current+1)->name) >0) {
            return 0;
        }
    }
    return 1;
}

int is_equal (const BusLine *start_sorted,
              const BusLine *end_sorted,
              const BusLine *start_original,
              const BusLine *end_original)
{
    if (end_sorted - start_sorted != end_original - start_original) {
        return 0;
    }

    for (int i = 0; i < end_sorted - start_sorted; i++) {
        int found = 0;
        for (int j = 0; j < end_original - start_original; j++) {
            if (strcmp(start_sorted[i].name, start_original[j].name) == 0) {
                found = 1;
            }
        }
        if (!found) {
            return 0;
        }
    }
    return 1;
}