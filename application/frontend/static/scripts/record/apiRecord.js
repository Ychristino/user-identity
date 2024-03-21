import { ApiRequest } from '../apiRequest.js';
import { BASE_URL, API_START_RECORD, API_STOP_RECORD, API_USER_LIST } from '../consts/apiConstants.js';

const API = new ApiRequest(BASE_URL);

const START_RECORD = async () => {
    try {
        const USERNAME = document.getElementById("username").value;
        const IS_MAIN_USER = document.getElementById("isMainUser").checked

        const BODY_DATA = {
                                main_user: IS_MAIN_USER,
                                user_running: USERNAME
                            }
        const response = await API.post(API_START_RECORD, BODY_DATA);
        return response.data;
    } catch (error) {
        console.error('Falha ao iniciar a gravação:', error);
    }
};

const STOP_RECORD = async () => {
    try {
        const response = await API.post(API_STOP_RECORD);
        return response.data;
    } catch (error) {
        console.error('Falha ao iniciar a gravação:', error);
    }
};

export { START_RECORD, STOP_RECORD };
