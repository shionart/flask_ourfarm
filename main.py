from controller import *
from model.Sensor import Sensor
from model.Control import *
# s = Sensor()
# s.setId_arduino("8d81e4eaf3d04534a9e3")
c = Control()
c.setUser_id("fpC1dDVM36WpxPkD56pMEOSM8zI2")
c.setId("450591a91d744559aff2")
  
scheduler.add_job(func=c.getControl, trigger="interval", seconds=5, max_instances=10)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# App Configuration Server
if __name__ == "__main__":
    main.run(host='0.0.0.0',port='5000',debug=True, threaded=True)