// Ref: https://stackoverflow.com/a/11409944/10491977
/**
 * Returns a number whose value is limited to the given range.
 *
 * Example: limit the output of this computation to between 0 and 255
 * (x * 255).clamp(0, 255)
 *
 * @param {Number} value Value to clamp
 * @param {Number} min The lower boundary of the output range
 * @param {Number} max The upper boundary of the output range
 * @returns A number in the range [min, max]
 * @type Number
 */
function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
}

// Ref: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
// Example POST method implementation:
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

let current_brightness = 0;

document.querySelector('#increase-brightness').addEventListener('click',
    () => {
        current_brightness += 20;
        current_brightness = clamp(current_brightness, 0, 100);
        postData(
            '/led-brightness',
            {brightness: current_brightness});
        document.querySelector('#brightness').textContent = current_brightness;
    });

document.querySelector('#decrease-brightness').addEventListener('click',
    () => {
        current_brightness -= 20;
        current_brightness = clamp(current_brightness, 0, 100);
        postData(
            '/led-brightness',
            {brightness: current_brightness});
        document.querySelector('#brightness').textContent = current_brightness;
    });

document.querySelector('#moonlight-button').addEventListener('click',
    () => {
        current_brightness = 5;
        postData(
            '/led-brightness',
            {brightness: current_brightness}
        );
        document.querySelector('#brightness').textContent = current_brightness;
    });

document.querySelector('#off-button').addEventListener('click',
    () => {
        current_brightness = 0;
        postData(
            '/led-brightness',
            {brightness: current_brightness}
        );
        document.querySelector('#brightness').textContent = current_brightness;
    });

document.querySelector('#timer1-on-off').addEventListener('click',
    (event) => {
        let turnOffTime = document.querySelector('#turn-off-time1');
        let edit = document.querySelector('#turn-off-timer1-edit-or-set');
        if(event.target.checked) {
            turnOffTime.style.color = '#c9c9c9';
            edit.style.color = '#c9c9c9';
            edit.disabled = false;
            postData('/turn-off-timer', {enabled: true, timer_index: 0});
        } else {
            turnOffTime.style.color = '#757575';
            edit.style.color = '#757575';
            edit.disabled = false;
            postData('/turn-off-timer', {enabled: false, timer_index: 0});
        }
    });

document.querySelector('#turn-off-timer1-edit-or-set').addEventListener('click',
    (event) => {
        const text = event.target.textContent;
        let inputFields = document.querySelector('#turn-off-timer1-input');
        let offTimeDisplay = document.querySelector('#turn-off-time1');
        let element = document.querySelector('#turn-off-timer1-edit-or-set');
        if(text == 'Edit') {
            inputFields.style.display = 'block';
            offTimeDisplay.style.display = 'none';
            element.textContent = 'Set';
            const h_and_m = offTimeDisplay.textContent.split(':').map(s => parseInt(s));
            document.querySelector('#turn-off-timer1-hour').value = h_and_m[0];
            document.querySelector('#turn-off-timer1-minute').value = h_and_m[1];
        } else if(text == 'Set') {
            inputFields.style.display = 'none';
            offTimeDisplay.style.display = 'block';
            element.textContent = 'Edit';

            // Update the time
            const hour = parseInt(document.querySelector('#turn-off-timer1-hour').value);
            const min = parseInt(document.querySelector('#turn-off-timer1-minute').value);
            if(hour === '') {
                console.log('The hour field is empty');
            } else {
                offTimeDisplay.textContent = `${hour}:${min.toString().padStart(2,'0')}`;
            }

            // Set the turn-off time
            postData('/turn-off-timer', {
                enabled: true,
                timer_index: 0,
                hour:   hour,
                minute: min
            });
        }
    });

// (async () => {
//     const res = await fetch('/led-brightness');
//     current_brightness = res.json().brightness;
//     document.querySelector('#brightness').textContent = current_brightness;
// })();
fetch('/led-brightness')
    .then(res => res.json())
    .then(data => {
        current_brightness = data.brightness;
        document.querySelector('#brightness').textContent = current_brightness;
    }).catch(console.error);

fetch('/turn-off-timer')
    .then(res => res.json())
    .then(data => {
        const timers = data.timers;
        for(let i=0; i<timers.length; i++) {
            const timer = timers[i];
            console.log(timer.enabled);

            const number = i+1;
            document.querySelector(`#timer${number}-on-off`).checked = timer.enabled;
            document.querySelector(`#turn-off-time${number}`).textContent
            = `${timer.hour}:${timer.minute.toString().padStart(2,'0')}`;

            // TODO: support multiple timers
            break;
        }
    }).catch(console.error);