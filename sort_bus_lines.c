#include "sort_bus_lines.h"

#include <stdbool.h>
#include <string.h>

void bus_quick_sort (BusLine *start, BusLine *end, SortType sort_type)
{
   if (start >= end) {
       return;
   }
    BusLine *pivot = partition(start, end, sort_type);

    bus_quick_sort(start, pivot, sort_type);
    bus_quick_sort(pivot+1, end, sort_type);
}

void bus_bubble_sort (BusLine *start, BusLine *end)
{
    int len = end - start;
    for (int i = 0; i < len; i++) {
        for (int j = 0; j < len - i -1; j++) {
            if (strcmp ((start + j)->name, (start + j +1)->name) > 0) {
                BusLine tmp = *(start + j);
                *(start + j) = *(start + j +1);
                *(start + j + 1) = tmp;
            }
        }
    }
}

BusLine *partition (BusLine *start, BusLine *end, SortType sort_type)
{
    if (start >= end) {
        return start;
    }
    BusLine *smaller_or_equal_limit = start-1;

    for (BusLine *moving_ptr =start; moving_ptr < end-1; moving_ptr++) {
        bool is_smaller_or_equal = false;
        switch (sort_type) {
            case DURATION:
                is_smaller_or_equal = (moving_ptr->duration <= (end-1)->duration);
                break;
            case DISTANCE:
                is_smaller_or_equal = (moving_ptr->distance <= (end-1)->distance);
                break;
            case FREQUENCY:
                is_smaller_or_equal = (moving_ptr->frequency <= (end-1)->frequency);
                break;
        }
        if (is_smaller_or_equal) {
            smaller_or_equal_limit++;
            BusLine tmp = *smaller_or_equal_limit;
            *smaller_or_equal_limit = *moving_ptr;
            *moving_ptr = tmp;
        }
    }
    smaller_or_equal_limit++;
    BusLine tmp = *smaller_or_equal_limit;
    *smaller_or_equal_limit = *(end-1);
    *(end-1) = tmp;

    return smaller_or_equal_limit;
}

static bool is_smaller(BusLine a, BusLine b, SortType sort_type) {
    switch (sort_type) {
        case DURATION: return a.duration < b.duration;
        case DISTANCE: return a.distance < b.distance;
        case FREQUENCY: return a.frequency < b.frequency;
    }
    return false;
}

void bus_insertion_sort (BusLine *start, BusLine *end, SortType sort_type) {
    int len = end - start;
    for (int i = 1; i < len; i++) {
        BusLine key = *(start + i);
        int j = i - 1;
        while (j >= 0 && is_smaller(key, *(start + j), sort_type)) {
            *(start + j + 1) = *(start + j);
            j--;
        }
        *(start + j + 1) = key;
    }
}

void bus_selection_sort (BusLine *start, BusLine *end, SortType sort_type) {
    int len = end - start;
    for (int i = 0; i < len - 1; i++) {
        BusLine *min_ptr = start + i;
        for (int j = i + 1; j < len; j++) {
            if (is_smaller(*(start + j), *min_ptr, sort_type)) {
                min_ptr = start + j;
            }
        }
        if (min_ptr != (start + i)) {
            BusLine tmp = *(start + i);
            *(start + i) = *min_ptr;
            *min_ptr = tmp;
        }
    }
}