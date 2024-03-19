import time
import threading

from objects.monitor.record_data import RecordData

if __name__ == '__main__':
    record_data = RecordData('vitao')
    recording_thread = threading.Thread(target=record_data.record_all)
    recording_thread.start()
    print('Início')

    time.sleep(5)

    print('Fim')
    record_data.stop_all()

    print('Encerrando processos...')
    recording_thread.join()
