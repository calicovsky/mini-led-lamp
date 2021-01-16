(() => {
    console.log('awww wifi settings iife');

    // Get the currently connected WiFi access point
    fetch('/get-currently-connected-wireless-ap-info')
    .then(res => res.json())
    .then(data => {
        let text = ''
        if(0 < data.ssid.length) {
            text = `Your Raspbery Pi is connected to "${data.ssid}".`;
        } else {
            text = 'Your Raspbery Pi does not appear to be connected to any WiFi network.';
        }
        document.querySelector('#currently-connected-network').textContent = text;
    });

    // // Populate the select element with the available WiFi access points
    // let selectElement = document.querySelector('#wifi-network-list');
    // fetch('/available-wifi-networks')
    // .then(res => res.json())
    // .then(data => {
    //     let index = 0;
    //     console.log(data.networks);
    //     for(network of data.networks) {
    //         let opt = document.createElement('option');
    //         opt.value = index;
    //         //opt.textContent = network.ssid;
    //         opt.innerHTML = network.ssid;
    //         opt.setAttribute('class', 'wifi-network');
    //         selectElement.appendChild(opt);
    //         index += 1;
    //     }
    // });

    // initModal('password-modal', 'connect-button', 'modal-close');

    document.querySelector('#connect-button').addEventListener('click', (event) => {
        const ssid = document.querySelector('#ssid');
        const password = document.querySelector('#wifi-password');
        console.log(`Connecting to ${ssid}`);

        const results = postData(
            '/connect-to-wireless-ap',
            {ssid: ssid, password: password});

        if(results.status == 'success') {
            alert(`Connected to ${ssid}`);
        } else {
            alert(`Couldn't onnect to ${ssid}\nError: ${results.message}`);
        }
    });
})()

