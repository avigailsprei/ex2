import re
import os

with open("visualizer/index.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update initial state
text = text.replace(
    '{ name: "Dan", distance: 300, duration: 45, frequency: 10 }',
    '{ name: "Dan", distance: 300, duration: 60, frequency: 10 }'
)
text = text.replace(
    '{ name: "Alice", distance: 100, duration: 20, frequency: 30 }',
    '{ name: "Alice", distance: 100, duration: 40, frequency: 30 }'
)
text = text.replace(
    '{ name: "Charlie", distance: 500, duration: 60, frequency: 5 }',
    '{ name: "Charlie", distance: 500, duration: 20, frequency: 5 }'
)
text = text.replace(
    '{ name: "Bob", distance: 200, duration: 30, frequency: 20 }',
    '{ name: "Bob", distance: 200, duration: 50, frequency: 20 }'
)

# 2. Update CSS for pointers container
text = text.replace(
'''/* Pointers */
.pointers-container {
    position: absolute;
    top: -60px;
    left: 0;
    width: 100%;
    height: 60px;
    pointer-events: none;
}''',
'''/* Pointers */
.pointers-container {
    position: absolute;
    top: -120px;
    left: 0;
    width: 100%;
    height: 120px;
    pointer-events: none;
    z-index: 10;
}'''
)

text = text.replace(
'''    margin-top: 60px;''',
'''    margin-top: 120px;'''
)

# 3. Update CSS for pointer arrows and labels
text = text.replace(
'''.pointer .label {
    background: currentColor;
    color: #fff;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
    white-space: nowrap;
}''',
'''.pointer .label {
    background: currentColor;
    color: #fff;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    white-space: nowrap;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}'''
)

# 4. Update the pointer top offset in JS
text = text.replace(
'''        let offset = p.level * 25; 
        el.style.top = `${offset}px`;''',
'''        let offset = 90 - (p.level * 30); 
        el.style.top = `${offset}px`;'''
)

# 5. Quick Sort narrative and partition logic visualization
qs_old = """    function partition(start, end) {
        if (start >= end) return start;

        let pivotIndex = end - 1;
        let limitIndex = start - 1;

        frames.push({
            arr: cloneArray(arr),
            pointers: [
                { id: 'start', label: 'start', index: start, class: 'ptr-start', level: 0 },
                { id: 'end', label: 'end', index: end, class: 'ptr-end', level: 0 },
                { id: 'limit', label: 'limit', index: limitIndex, class: 'ptr-limit', level: 1 },
                { id: 'pivot', label: 'pivot (end-1)', index: pivotIndex, class: 'ptr-end', level: 2 }
            ],
            highlights: [ {index: pivotIndex, type: 'pivot'} ],
            action: `Partitioning range [${formatAddr(start)}, ${formatAddr(end)}]. Pivot is ${arr[pivotIndex].name}`
        });

        for (let moving = start; moving < end - 1; moving++) {
            frames.push({
                arr: cloneArray(arr),
                pointers: [
                    { id: 'limit', label: 'limit', index: limitIndex, class: 'ptr-limit', level: 1 },
                    { id: 'moving', label: 'moving_ptr', index: moving, class: 'ptr-moving', level: 2 },
                    { id: 'pivot', label: 'pivot', index: pivotIndex, class: 'ptr-end', level: 3 }
                ],
                highlights: [ {index: moving, type: 'comparing'}, {index: pivotIndex, type: 'pivot'} ],
                action: `Comparing ${arr[moving].name} with pivot ${arr[pivotIndex].name}`
            });

            let isSmaller = false;
            let cmpVal = compare(arr[moving], arr[pivotIndex], metric);
            if (metric === 'name') isSmaller = cmpVal <= 0; 
            else isSmaller = arr[moving][metric] <= arr[pivotIndex][metric];

            if (isSmaller) {
                limitIndex++;
                
                frames.push({
                    arr: cloneArray(arr),
                    pointers: [
                        { id: 'limit', label: 'limit', index: limitIndex, class: 'ptr-limit', level: 1 },
                        { id: 'moving', label: 'moving_ptr', index: moving, class: 'ptr-moving', level: 2 },
                        { id: 'pivot', label: 'pivot', index: pivotIndex, class: 'ptr-end', level: 3 }
                    ],
                    highlights: [ {index: limitIndex, type: 'swapping'}, {index: moving, type: 'swapping'} ],
                    action: `Element is <= pivot. Incrementing limit and Swapping ${arr[limitIndex].name} with ${arr[moving].name}`
                });

                let tmp = arr[limitIndex];
                arr[limitIndex] = arr[moving];
                arr[moving] = tmp;

                 frames.push({
                    arr: cloneArray(arr),
                    pointers: [
                        { id: 'limit', label: 'limit', index: limitIndex, class: 'ptr-limit', level: 1 },
                        { id: 'moving', label: 'moving', index: moving, class: 'ptr-moving', level: 2 }
                    ],
                    highlights: [ {index: pivotIndex, type: 'pivot'} ],
                    action: `Swap complete`
                });
            }
        }

        limitIndex++;
        frames.push({
            arr: cloneArray(arr),
            pointers: [
                { id: 'limit', label: 'limit', index: limitIndex, class: 'ptr-limit', level: 1 },
                { id: 'pivot', label: 'pivot', index: pivotIndex, class: 'ptr-end', level: 2 }
            ],
            highlights: [ {index: limitIndex, type: 'swapping'}, {index: pivotIndex, type: 'swapping'} ],
            action: `Loop done. Placing pivot by swapping ${arr[limitIndex].name} with ${arr[pivotIndex].name}`
        });

        let tmp = arr[limitIndex];
        arr[limitIndex] = arr[pivotIndex];
        arr[pivotIndex] = tmp;

        frames.push({
            arr: cloneArray(arr),
            pointers: [
                { id: 'pivot_placed', label: 'pivot_final', index: limitIndex, class: 'ptr-start', level: 0 }
            ],
            highlights: [ {index: limitIndex, type: 'sorted'} ],
            action: `Pivot placed at final position ${formatAddr(limitIndex)}`
        });

        return limitIndex;
    }"""

qs_new = """    function partition(start, end) {
        if (start >= end) return start;

        let pivotIndex = end - 1;
        let limitIndex = start - 1;

        frames.push({
            arr: cloneArray(arr),
            pointers: [
                { id: 'start', label: 'start', index: start, class: 'ptr-start', level: 0 },
                { id: 'end', label: 'end', index: end, class: 'ptr-end', level: 0 },
                { id: 'limit', label: 'limit (smaller <=)', index: limitIndex, class: 'ptr-limit', level: 1 },
                { id: 'pivot', label: 'pivot', index: pivotIndex, class: 'ptr-end', level: 2 }
            ],
            highlights: [ {index: pivotIndex, type: 'pivot'} ],
            action: `Partitioning. Pivot is ${arr[pivotIndex].name}. 'limit' tracks the boundary of smaller elements.`
        });

        for (let moving = start; moving < end - 1; moving++) {
            frames.push({
                arr: cloneArray(arr),
                pointers: [
                    { id: 'limit', label: 'limit', index: limitIndex, class: 'ptr-limit', level: 1 },
                    { id: 'moving', label: 'moving', index: moving, class: 'ptr-moving', level: 2 },
                    { id: 'pivot', label: 'pivot', index: pivotIndex, class: 'ptr-end', level: 3 }
                ],
                highlights: [ {index: moving, type: 'comparing'}, {index: pivotIndex, type: 'pivot'} ],
                action: `Comparing ${arr[moving].name} with pivot ${arr[pivotIndex].name}.`
            });

            let isSmaller = false;
            let cmpVal = compare(arr[moving], arr[pivotIndex], metric);
            if (metric === 'name') isSmaller = cmpVal <= 0; 
            else isSmaller = arr[moving][metric] <= arr[pivotIndex][metric];

            if (isSmaller) {
                limitIndex++;
                
                frames.push({
                    arr: cloneArray(arr),
                    pointers: [
                        { id: 'limit', label: 'limit++ (expand)', index: limitIndex, class: 'ptr-limit', level: 1 },
                        { id: 'moving', label: 'moving', index: moving, class: 'ptr-moving', level: 2 },
                        { id: 'pivot', label: 'pivot', index: pivotIndex, class: 'ptr-end', level: 3 }
                    ],
                    highlights: [ {index: limitIndex, type: 'swapping'}, {index: moving, type: 'swapping'} ],
                    action: `It is smaller! Expanding the 'smaller region' (limit++) and swapping to include it.`
                });

                let tmp = arr[limitIndex];
                arr[limitIndex] = arr[moving];
                arr[moving] = tmp;

                 frames.push({
                    arr: cloneArray(arr),
                    pointers: [
                        { id: 'limit', label: 'limit', index: limitIndex, class: 'ptr-limit', level: 1 },
                        { id: 'moving', label: 'moving', index: moving, class: 'ptr-moving', level: 2 }
                    ],
                    highlights: [ {index: pivotIndex, type: 'pivot'} ],
                    action: `Swap complete. ${arr[limitIndex].name} is now safely inside the smaller region.`
                });
            } else {
                frames.push({
                    arr: cloneArray(arr),
                    pointers: [
                        { id: 'limit', label: 'limit', index: limitIndex, class: 'ptr-limit', level: 1 },
                        { id: 'moving', label: 'moving', index: moving, class: 'ptr-moving', level: 2 },
                        { id: 'pivot', label: 'pivot', index: pivotIndex, class: 'ptr-end', level: 3 }
                    ],
                    highlights: [ {index: pivotIndex, type: 'pivot'} ],
                    action: `It is larger. Doing nothing, so it naturally becomes part of the larger region.`
                });
            }
        }

        limitIndex++;
        frames.push({
            arr: cloneArray(arr),
            pointers: [
                { id: 'limit', label: 'limit+1', index: limitIndex, class: 'ptr-limit', level: 1 },
                { id: 'pivot', label: 'pivot', index: pivotIndex, class: 'ptr-end', level: 2 }
            ],
            highlights: [ {index: limitIndex, type: 'swapping'}, {index: pivotIndex, type: 'swapping'} ],
            action: `Loop done. Placing pivot immediately after the smaller region (at limit+1).`
        });

        let tmp = arr[limitIndex];
        arr[limitIndex] = arr[pivotIndex];
        arr[pivotIndex] = tmp;

        frames.push({
            arr: cloneArray(arr),
            pointers: [
                { id: 'pivot_placed', label: 'pivot_placed', index: limitIndex, class: 'ptr-start', level: 0 }
            ],
            highlights: [ {index: limitIndex, type: 'sorted'} ],
            action: `Pivot placed at its final, sorted position ${formatAddr(limitIndex)}.`
        });

        return limitIndex;
    }"""
text = text.replace(qs_old, qs_new)

with open("visualizer/index.html", "w", encoding="utf-8") as f:
    f.write(text)
