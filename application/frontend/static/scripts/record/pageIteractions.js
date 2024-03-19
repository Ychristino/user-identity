import { START_RECORD, STOP_RECORD } from './apiRecord.js';

document.getElementById('isMainUser').addEventListener('click', (event)=>{
    const USERNAME = document.getElementById('username');

    USERNAME.disabled = event.target.checked;
    USERNAME.value = '';

})

document.getElementById("BtmPlay").addEventListener("click", ()=> {

    const IS_MAIN_USER = document.getElementById('isMainUser').checked;
    const USERNAME = document.getElementById('username').value.trim();

    if (!IS_MAIN_USER && USERNAME === ''){
        throw new Error('Invalid username. Please specify the user running the app or sign the main user button.');
    }
    else START_RECORD(event)

});

document.getElementById("BtmStop").addEventListener("click", STOP_RECORD);

