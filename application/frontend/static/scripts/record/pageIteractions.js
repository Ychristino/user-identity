import { START_RECORD, STOP_RECORD } from './apiRecord.js';
import { show_notification } from '../common/alert.js';

let isPlaying = false;

document.getElementById('isMainUser').addEventListener('click', (event)=>{
    const USERNAME = document.getElementById('username');

    USERNAME.disabled = event.target.checked;
    USERNAME.value = '';

})

document.getElementById("playStop").addEventListener("click", (event)=> {

    const IS_MAIN_USER = document.getElementById('isMainUser').checked;
    const USERNAME = document.getElementById('username').value.trim();
    const toggleButton = event.target;

    if (!IS_MAIN_USER && USERNAME === ''){
        show_notification('Invalid username. Please specify the user running the app or sign the main user button.', 'danger');
        throw new Error('Invalid username. Please specify the user running the app or sign the main user button.');
    }
    else {
        isPlaying = !isPlaying;
        if (isPlaying) {
            if (confirm('The mouse coordinates (X, Y) position will be recorded. Also, we will keep track of your Keyboard to record the times of key presses and release. The data will be used strictly for metrics. For precaution, at this time, avoid using this app while you are authenticating in another app.')){
                START_RECORD(event)
                    .then(() => {
                        toggleButton.textContent = "Stop";
                        toggleButton.classList.add("toggle-button");
                        toggleButton.classList.remove("btn-success");
                        toggleButton.classList.add("btn-danger");
                        show_notification('Record Started', 'success');
                    })
                    .catch((error) => {
                        isPlaying = !isPlaying;
                        show_notification(`Error while trying to start record. ${error}`, 'danger');
                    });
            }
            else isPlaying = !isPlaying;
        }
        else {
            STOP_RECORD(event)
            .then ( ()=>{
                toggleButton.textContent = "Record";
                toggleButton.classList.remove("toggle-button");
                toggleButton.classList.remove("btn-danger");
                toggleButton.classList.add("btn-success");
                show_notification('Record Stopped', 'success');
            })
            .catch((error)=>{
                isPlaying = !isPlaying;
                show_notification(`Error while trying to stop record. ${error}`, 'danger');
            });
        }
    }
});