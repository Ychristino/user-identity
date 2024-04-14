import { ApiRequest } from '../apiRequest.js';
import { BASE_URL, API_MODELS } from '../consts/apiConstants.js';

const API = new ApiRequest(BASE_URL);

const EXECUTE_MODEL = async () => {
    const MODEL = document.getElementById("modelSelect").value;
    const ACTIVITY = document.getElementById("activitySelect").value;
    const ALL_ACTIVITIES = document.getElementById('allActivitiesCheckbox').checked;

    const BODY_DATA = {
                        model: MODEL,
                        activity: !ALL_ACTIVITIES ? ACTIVITY : null,
                      };

        const response = await API.get(API.post(API_MODELS, BODY_DATA));
        return response.data;
};

export { EXECUTE_MODEL };