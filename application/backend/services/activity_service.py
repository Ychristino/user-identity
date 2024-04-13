from common.activity import Activity


class ActivityService:

    def get_activity_list(self):
        return_data = {'data': []}
        for activity in Activity:
            return_data['data'].append(activity.value)
        return return_data
