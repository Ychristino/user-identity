from enum import Enum


class Activity(Enum):
    LEAGUE_OF_LEGENDS = {'label': 'League of Legends',
                         'value': 'lol',
                         'folder': 'league_of_legends',
                         'id': 1
                         }
    VALORANT = {'label': 'Valorant',
                'value': 'val',
                'folder': 'valorant',
                'id': 2
                }
    MINECRAFT = {'label': 'Minecraft',
                 'value': 'mine',
                 'folder': 'minecraft',
                 'id': 3
                 }
    WEB_BROWSER = {'label': 'Navegador',
                   'value': 'wb',
                   'folder': 'web_browser',
                   'id': 4
                   }
    COUNTER_STRIKE = {'label': 'CS 2',
                      'value': 'cs',
                      'folder': 'counter_strike',
                      'id': 5
                      }


# Função para encontrar a atividade pelo valor
def find_activity_by_value(value):
    for activity in Activity:
        if activity.value['value'] == value:
            return activity
    return None
