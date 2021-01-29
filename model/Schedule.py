from model.Control import Control
from model.Sensor import Sensor
from apscheduler.schedulers.background import BackgroundScheduler


# The "apscheduler." prefix is hard coded
scheduler = BackgroundScheduler({
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '60'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '60'
    },
    'apscheduler.job_defaults.max_instances': '60',
    'apscheduler.timezone': 'UTC',
})
class Schedule():
    """
    Kelas untuk set scheduler dan fungsi yang berkaitan
    """
    
    def getListControl(self):
        """
        Fungsi untuk mengecek secara berkala Control pada tiap Nodes
        """
        print("memulai getlistcontrol")
        try:
            a = Control().read_controls()
            if a!=None:
                for control in a:
                    # print("Satuan control")
                    c = Control(id_arduino=control['id_arduino'], id_user=control['id_user'])
                    c.getControl()
            else:
                print("KOSONG")
        except Exception as e:
            print(e)
