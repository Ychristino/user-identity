const BASE_URL = "http://127.0.0.1:5000";

const API_START_RECORD = "start_recording";
const API_STOP_RECORD = "stop_recording";

const API_ACTIVITY_LIST = "activities";

const API_CHECK_USER = "check_user/{username}";
const API_USER_LIST = "users_list";

const API_MOUSE_MOVE = "view/mouse_position/{username}"
const API_MOUSE_CLICK = "view/mouse_click/{username}"
const API_MOUSE_FULL = "view/mouse_full/{username}"

const API_KEYBOARD_STATS = "/stats/keyboard/{username}"
const API_MOUSE_STATS = "/stats/mouse/{username}"
const API_FULL_STATS ="/stats/full/{username}"

export { BASE_URL, API_START_RECORD, API_STOP_RECORD, API_CHECK_USER, API_USER_LIST, API_MOUSE_MOVE, API_MOUSE_CLICK,
         API_MOUSE_FULL, API_KEYBOARD_STATS, API_MOUSE_STATS, API_FULL_STATS };