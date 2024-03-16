from objects.analyses.mouse_analyses import MouseAnalyses
from objects.analyses.keyboard_analyses import KeyboardAnalyses
from objects.analyses.keyboard_analyses import read_file as read_keyboard_file
from objects.analyses.mouse_analyses import read_file as read_mouse_file

mouse_analyses = MouseAnalyses()
list_mouse_movement_data, list_mouse_click_data = read_mouse_file('./files/user/mouse_data.json')

for move_data in list_mouse_movement_data:
    mouse_analyses.mouse_movement_data = move_data

    mouse_analyses.extract_velocity_metrics()
    mouse_analyses.extract_movement_metrics()
    mouse_analyses.extract_distance_metrics()

for click_data in list_mouse_click_data:
    mouse_analyses.mouse_click_data = click_data
    mouse_analyses.extract_clicks_metrics()

keyboard_analyses = KeyboardAnalyses()
list_keyboard_press_data, list_keyboard_release_data = read_keyboard_file('./files/user/keyboard_data.json')

for index in range(len(list_keyboard_press_data)):
    keyboard_analyses.keyboard_press_data = list_keyboard_press_data[index]

    keyboard_analyses.keyboard_release_data = list_keyboard_release_data[index]

    keyboard_analyses.extract_keyboard_data()
