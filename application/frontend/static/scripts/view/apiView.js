import { ApiRequest } from '../apiRequest.js';
import { BASE_URL, API_MOUSE_MOVE, API_FULL_STATS } from '../consts/apiConstants.js';

const API = new ApiRequest(BASE_URL);

const MOUSE_MOVE = async (username) => {
    try {
        const response = await API.get(API.get_user_endpoint(API_MOUSE_MOVE, username));
        return response.data;
    } catch (error) {
        console.error('Falha ao obter dados do usuário:', error);
        return null;
    }
};

const FULL_DATA = async (username) => {
    try {
        const response = await API.get(API.get_user_endpoint(API_FULL_STATS, username));
        return response.data;
    } catch (error) {
        console.error('Falha ao obter dados do usuário:', error);
        return null;
    }
};
export { MOUSE_MOVE, FULL_DATA };
