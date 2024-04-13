import threading

from common.activity import Activity
from objects.monitor.record_data import RecordData


class RecordService:
    def __init__(self):
        self.recording = False
        self.record_data = None
        self.recording_thread = None

    def start_record(self, user_running: str, activity: Activity):
        if not self.recording:
            self.record_data = RecordData(user_running, activity)
            self.recording_thread = threading.Thread(target=self.record_data.record_all)
            self.recording_thread.start()
            self.recording = True
            return True  # Indica que a gravação foi iniciada com sucesso
        else:
            return False  # Indica que a gravação já está em andamento

    def stop_record(self):
        if self.recording:
            self.record_data.stop_all()
            self.recording_thread.join()
            self.recording = False
            return True  # Indica que a gravação foi interrompida com sucesso
        else:
            return False  # Indica que não há gravação em andamento
