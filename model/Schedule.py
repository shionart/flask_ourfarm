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
        Fungsi untuk mengecek secara berkala Control pada tiap Control ke Main Web
        """
        print("memulai getlistcontrol")
        try:
            a = Control().read_list_control() 
            if a!=None:#cek local ada Control atau tidak
                for control in a:
                    # print("Satuan control")
                    #Membuat obj control tiap baris pada table control
                    c = Control(id_arduino=control['id_arduino'], id_user=control['id_user'])
                    c.sync_get_control() #Ngambil data terbaru
            else:
                print("KOSONG")
        except Exception as e:
            print(e)
