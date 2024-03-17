import time
import threading

from objects.monitor.record_data import RecordData

record_data = RecordData('user')
recording_thread = threading.Thread(target=record_data.record_all)
recording_thread.start()
print('Início')

time.sleep(5)

print('Fim')
record_data.stop_all()

print('Encerrando processos...')
recording_thread.join()
