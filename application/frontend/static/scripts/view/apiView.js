import { ApiRequest } from '../apiRequest.js';
import { BASE_URL, API_USER_LIST, API_MOUSE_MOVE } from '../consts/apiConstants.js';

const API = new ApiRequest(BASE_URL);

const MOUSE_MOVE = async (username) => {
    try {
        console.log(API.get_user_endpoint(API_MOUSE_MOVE, username))
        const response = await API.get(API.get_user_endpoint(API_MOUSE_MOVE, username));
        return response.data;
    } catch (error) {
        console.error('Falha ao obter dados do usuário:', error);
        return null;
    }
};

const USER_LIST = async () => {
    try {
        const response = await API.get(API_USER_LIST);
        return response.data
    } catch (error) {
        console.error('Falha ao obter lista de usuários:', error);
        return null;
    }
};

export { USER_LIST, MOUSE_MOVE };
