import json
import os

from common.activity import Activity, find_activity_by_value
from common.constants import KEYBOARD_FILE, MOUSE_FILE, BASE_DIR
from objects.analyses.keyboard_analyses import KeyboardAnalyses
from objects.analyses.mouse_analyses import MouseAnalyses
from objects.analyses.keyboard_analyses import read_file as read_keyboard_file
from objects.analyses.mouse_analyses import read_file as read_mouse_file


def _generate_mouse_stats(user_mouse_file_path: str, activity: Activity = None):
    analyses = MouseAnalyses()
    list_mouse_movement_data, list_mouse_click_data = read_mouse_file(mouse_file_path=user_mouse_file_path, activity=activity)

    for move_data in list_mouse_movement_data:
        analyses.mouse_movement_data = move_data

        analyses.extract_velocity_metrics()
        analyses.extract_movement_metrics()
        analyses.extract_distance_metrics()

    for click_data in list_mouse_click_data:
        analyses.mouse_click_data = click_data
        analyses.extract_clicks_metrics()
    return analyses.generate_dataframe().to_json()


def _generate_keyboard_stats(user_keyboard_file_path: str, activity: Activity = None):
    analyses = KeyboardAnalyses()
    list_keyboard_press_data, list_keyboard_release_data = read_keyboard_file(keyboard_file_path=user_keyboard_file_path, activity=activity)

    for index in range(len(list_keyboard_press_data)):
        analyses.keyboard_press_data = list_keyboard_press_data[index]
        analyses.keyboard_release_data = list_keyboard_release_data[index]
        analyses.extract_keyboard_data()

    return analyses.generate_dataframe().to_json()


class StatisticsService:
    def __init__(self):
        self.base_path = os.path.join(BASE_DIR, 'files')

    def get_mouse_statistics(self, username: str = None, activity: str = None):
        if username is not None:
            user_data = {'data': {}}
            user_mouse_file_path = os.path.join(self.base_path, username)
            user_data['data'] = json.loads(_generate_mouse_stats(user_mouse_file_path=user_mouse_file_path,
                                                                 activity=find_activity_by_value(activity)
                                                                 )
                                           )
        else:
            user_data = {'data': []}
            for user_folder in os.listdir(self.base_path):
                user_mouse_file_path = os.path.join(self.base_path, user_folder, MOUSE_FILE)
                user_data['data'].append(
                    {user_folder: json.loads(_generate_mouse_stats(user_mouse_file_path=user_mouse_file_path,
                                                                   activity=find_activity_by_value(activity)
                                                                   )
                                             )})
        return user_data

    def get_keyboard_statistics(self, username: str = None, activity: str = None):
        if username is not None:
            user_data = {'data': {}}
            user_keyboard_file_path = os.path.join(self.base_path, username)
            user_data['data'] = json.loads(_generate_keyboard_stats(user_keyboard_file_path=user_keyboard_file_path,
                                                                    activity=find_activity_by_value(activity)
                                                                    )
                                           )
        else:
            user_data = {'data': []}
            for user_folder in os.listdir(self.base_path):
                user_keyboard_file_path = os.path.join(self.base_path, user_folder)
                user_data['data'].append(
                    {user_folder: json.loads(_generate_keyboard_stats(user_keyboard_file_path=user_keyboard_file_path,
                                                                      activity=find_activity_by_value(activity)
                                                                      )
                                             )})
        return user_data

    def get_full_statistics(self, username: str = None, activity: str = None):
        if username is not None:
            user_data = {'data': {
                'mouse_stats': {},
                'keyboard_stats': {}
            }}
            user_mouse_file_path = os.path.join(self.base_path, username)
            user_keyboard_file_path = os.path.join(self.base_path, username)
            user_data['data']['mouse_stats'] = json.loads(_generate_mouse_stats(user_mouse_file_path=user_mouse_file_path,
                                                                                activity=find_activity_by_value(activity)
                                                                                )
                                                          )
            user_data['data']['keyboard_stats'] = json.loads(_generate_keyboard_stats(user_keyboard_file_path=user_keyboard_file_path,
                                                                                      activity=find_activity_by_value(activity)
                                                                                      )
                                                             )
        else:
            user_data = {'data': []}
            for user_folder in os.listdir(self.base_path):
                user_mouse_file_path = os.path.join(self.base_path, user_folder)
                user_keyboard_file_path = os.path.join(self.base_path, user_folder)
                user_data['data'].append({
                        'username': user_folder,
                        'mouse_info': json.loads(_generate_mouse_stats(user_mouse_file_path=user_mouse_file_path,
                                                                       activity=find_activity_by_value(activity)
                                                                       )
                                                 ),
                        'keyboard_info': json.loads(_generate_keyboard_stats(user_keyboard_file_path=user_keyboard_file_path,
                                                                             activity=find_activity_by_value(activity)
                                                                             )
                                                    )
                })
        return user_data
