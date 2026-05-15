const BASE_ADDR = 0x1000;
const ELEMENT_SIZE = 0x40; // 64 bytes
const GAP = 24; // 1.5rem in px
const ELEMENT_WIDTH = 140; 
const TOTAL_ELEMENT_WIDTH = ELEMENT_WIDTH + GAP;

const initialState = [
    { name: "Dan", distance: 300, duration: 45, frequency: 10 },
    { name: "Alice", distance: 100, duration: 20, frequency: 30 },
    { name: "Charlie", distance: 500, duration: 60, frequency: 5 },
    { name: "Bob", distance: 200, duration: 30, frequency: 20 }
];

let frames = [];
let currentFrameIndex = 0;
let playing = false;
let playInterval;

const arrayContainer = document.getElementById('array-container');
const pointersContainer = document.getElementById('pointers-container');
const actionText = document.getElementById('action-text');
const logList = document.getElementById('log-list');
const btnStart = document.getElementById('btn-start');
const btnPrev = document.getElementById('btn-prev');
const btnNext = document.getElementById('btn-next');
const btnPlayPause = document.getElementById('btn-play-pause');
const stepCurrent = document.getElementById('step-current');
const stepTotal = document.getElementById('step-total');
const speedSlider = document.getElementById('speed-slider');

function formatAddr(index) {
    return `0x${(BASE_ADDR + index * ELEMENT_SIZE).toString(16).toUpperCase()}`;
}

function cloneArray(arr) {
    return JSON.parse(JSON.stringify(arr));
}

function compare(a, b, metric) {
    if (metric === 'name') {
        return a.name.localeCompare(b.name);
    }
    return a[metric] - b[metric];
}

function simulateBubbleSort(data, metric) {
    frames = [];
    let arr = cloneArray(data);
    let len = arr.length;
    
    frames.push({
        arr: cloneArray(arr),
        pointers: [
            { id: 'start', label: 'start', index: 0, class: 'ptr-start', level: 0 },
            { id: 'end', label: 'end', index: len, class: 'ptr-end', level: 0 }
        ],
        highlights: [],
        action: `Starting Bubble Sort by ${metric}`
    });

    for (let i = 0; i < len; i++) {
        for (let j = 0; j < len - i - 1; j++) {
            let cmpVal = compare(arr[j], arr[j+1], metric);
            
            frames.push({
                arr: cloneArray(arr),
                pointers: [
                    { id: 'start', label: 'start', index: 0, class: 'ptr-start', level: 0 },
                    { id: 'end', label: 'end', index: len, class: 'ptr-end', level: 0 },
                    { id: 'j', label: 'start + j', index: j, class: 'ptr-j', level: 1 },
                    { id: 'j1', label: 'start + j + 1', index: j+1, class: 'ptr-j1', level: 2 }
                ],
                highlights: [ {index: j, type: 'comparing'}, {index: j+1, type: 'comparing'} ],
                action: `Comparing ${arr[j].name} and ${arr[j+1].name}`
            });

            if (cmpVal > 0) {
                frames.push({
                    arr: cloneArray(arr),
                    pointers: [
                        { id: 'j', label: 'start + j', index: j, class: 'ptr-j', level: 1 },
                        { id: 'j1', label: 'start + j + 1', index: j+1, class: 'ptr-j1', level: 2 }
                    ],
                    highlights: [ {index: j, type: 'swapping'}, {index: j+1, type: 'swapping'} ],
                    action: `Swapping ${arr[j].name} and ${arr[j+1].name}`
                });

                let tmp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = tmp;

                frames.push({
                    arr: cloneArray(arr),
                    pointers: [
                        { id: 'j', label: 'start + j', index: j, class: 'ptr-j', level: 1 },
                        { id: 'j1', label: 'start + j + 1', index: j+1, class: 'ptr-j1', level: 2 }
                    ],
                    highlights: [],
                    action: `Swap complete`
                });
            }
        }
        
        frames.push({
            arr: cloneArray(arr),
            pointers: [
                { id: 'start', label: 'start', index: 0, class: 'ptr-start', level: 0 },
                { id: 'end', label: 'end', index: len, class: 'ptr-end', level: 0 }
            ],
            highlights: [ {index: len - i - 1, type: 'sorted'} ],
            action: `Element at ${formatAddr(len - i - 1)} is fully sorted`
        });
    }

    frames.push({
        arr: cloneArray(arr),
        pointers: [],
        highlights: arr.map((_, idx) => ({index: idx, type: 'sorted'})),
        action: `Bubble Sort Complete!`
    });
}

function simulateQuickSort(data, metric) {
    frames = [];
    let arr = cloneArray(data);
    let len = arr.length;

    frames.push({
        arr: cloneArray(arr),
        pointers: [
            { id: 'start', label: 'start', index: 0, class: 'ptr-start', level: 0 },
            { id: 'end', label: 'end', index: len, class: 'ptr-end', level: 0 }
        ],
        highlights: [],
        action: `Starting Quick Sort by ${metric}`
    });

    function partition(start, end) {
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
    }

    function qs(start, end) {
        if (start >= end) return;
        let p = partition(start, end);
        qs(start, p);
        qs(p + 1, end);
    }

    qs(0, len);

    frames.push({
        arr: cloneArray(arr),
        pointers: [],
        highlights: arr.map((_, idx) => ({index: idx, type: 'sorted'})),
        action: `Quick Sort Complete!`
    });
}

function renderFrame(index) {
    if (index < 0 || index >= frames.length) return;
    currentFrameIndex = index;
    const frame = frames[index];

    arrayContainer.innerHTML = '';
    
    let maxPointerIndex = frame.arr.length; 
    frame.pointers.forEach(p => { if(p.index > maxPointerIndex) maxPointerIndex = p.index; });
    arrayContainer.style.width = `${(maxPointerIndex + 1) * TOTAL_ELEMENT_WIDTH}px`;

    // Persist sorted elements across frames conceptually (basic check)
    let sortedIndices = frame.highlights.filter(h => h.type === 'sorted').map(h => h.index);

    frame.arr.forEach((bus, i) => {
        let el = document.createElement('div');
        el.className = 'array-element';
        
        let highlight = frame.highlights.find(h => h.index === i);
        if (highlight) {
            el.classList.add(highlight.type);
        } else if (sortedIndices.includes(i)) {
            el.classList.add('sorted');
        }

        el.style.left = `${i * TOTAL_ELEMENT_WIDTH + 32}px`; // +32 for padding

        el.innerHTML = `
            <div class="element-header">${bus.name}</div>
            <div class="element-stat"><span class="label">Dist:</span> ${bus.distance}</div>
            <div class="element-stat"><span class="label">Dur:</span> ${bus.duration}</div>
            <div class="element-stat"><span class="label">Freq:</span> ${bus.frequency}</div>
            <div class="address-label">${formatAddr(i)}</div>
        `;
        arrayContainer.appendChild(el);
    });

    pointersContainer.innerHTML = '';
    frame.pointers.forEach(p => {
        let el = document.createElement('div');
        el.className = `pointer ${p.class}`;
        
        let leftPos = p.index * TOTAL_ELEMENT_WIDTH + (ELEMENT_WIDTH / 2);
        if (p.index < 0) leftPos = -TOTAL_ELEMENT_WIDTH + (ELEMENT_WIDTH / 2);

        el.style.left = `${leftPos + 32}px`; 

        el.innerHTML = `
            <div class="label">${p.label}</div>
            <div class="arrow"></div>
        `;
        
        let offset = p.level * 25; 
        el.style.top = `${offset}px`;

        pointersContainer.appendChild(el);
    });

    actionText.textContent = frame.action;
    stepCurrent.textContent = currentFrameIndex + 1;
    stepTotal.textContent = frames.length;

    if (!logList.children[index] && index === logList.children.length) {
        let li = document.createElement('li');
        li.textContent = `[${index + 1}] ${frame.action}`;
        logList.appendChild(li);
    } else if (logList.children.length === 0) {
        // rebuild log list if skipping around
        frames.forEach((f, i) => {
            let li = document.createElement('li');
            li.textContent = `[${i + 1}] ${f.action}`;
            logList.appendChild(li);
        });
    }
    
    Array.from(logList.children).forEach((li, i) => {
        li.className = i === index ? 'active' : '';
        if (i === index) li.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });

    btnPrev.disabled = currentFrameIndex === 0;
    btnNext.disabled = currentFrameIndex === frames.length - 1;
}

function nextStep() {
    if (currentFrameIndex < frames.length - 1) renderFrame(currentFrameIndex + 1);
    else stopPlayback();
}

function prevStep() {
    if (currentFrameIndex > 0) renderFrame(currentFrameIndex - 1);
}

function togglePlayback() {
    playing = !playing;
    btnPlayPause.textContent = playing ? '⏸' : '▶';
    if (playing) {
        if (currentFrameIndex === frames.length - 1) renderFrame(0);
        let speed = 11 - parseInt(speedSlider.value); 
        playInterval = setInterval(nextStep, speed * 200);
    } else {
        clearInterval(playInterval);
    }
}

function stopPlayback() {
    playing = false;
    btnPlayPause.textContent = '▶';
    clearInterval(playInterval);
}

speedSlider.addEventListener('change', () => {
    if (playing) {
        stopPlayback();
        togglePlayback();
    }
});

btnStart.addEventListener('click', () => {
    const algo = document.getElementById('algorithm-select').value;
    const metric = document.getElementById('metric-select').value;
    
    stopPlayback();
    logList.innerHTML = '';
    
    if (algo === 'bubble') simulateBubbleSort(initialState, metric);
    else simulateQuickSort(initialState, metric);

    btnPrev.disabled = false;
    btnNext.disabled = false;
    btnPlayPause.disabled = false;

    renderFrame(0);
});

btnNext.addEventListener('click', () => { stopPlayback(); nextStep(); });
btnPrev.addEventListener('click', () => { stopPlayback(); prevStep(); });
btnPlayPause.addEventListener('click', togglePlayback);

// Initial render to show empty array
frames = [{
    arr: cloneArray(initialState),
    pointers: [],
    highlights: [],
    action: "Select algorithm and metric, then click Start Simulation"
}];
renderFrame(0);
btnPrev.disabled = true;
btnNext.disabled = true;
btnPlayPause.disabled = true;
