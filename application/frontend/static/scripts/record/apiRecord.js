import { ApiRequest } from '../apiRequest.js';
import { BASE_URL, API_START_RECORD, API_STOP_RECORD, API_USER_LIST } from '../consts/apiConstants.js';

const API = new ApiRequest(BASE_URL);

const START_RECORD = async () => {
    const USERNAME = document.getElementById("username").value;
    const ACTIVITY = document.getElementById('activitySelect').value;
    const IS_MAIN_USER = document.getElementById("isMainUser").checked

    const BODY_DATA = {
                        main_user: IS_MAIN_USER,
                        user_running: USERNAME,
                        activity: ACTIVITY
                      };

    const response = await API.post(API_START_RECORD, BODY_DATA);
    return response.data;
};

const STOP_RECORD = async () => {
    const response = await API.post(API_STOP_RECORD);
    return response.data;
};

export { START_RECORD, STOP_RECORD };
