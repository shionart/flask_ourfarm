from config.config import *
from route import *
from model.Schedule import *
import atexit

  
# scheduler.start()

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

# App Configuration Server
# my_loader = jinja2.ChoiceLoader([
#         app.jinja_loader,
#         jinja2.FileSystemLoader(['/flaskapp/userdata', 
#                                  '/flaskapp/templates']),
#     ])
# app.jinja_loader = my_loader
if __name__ == "__main__":
    ## sync start
    # s = Schedule()
    # scheduler.add_job(func=s.getListControl, trigger="interval", seconds=5, max_instances=10)
    # scheduler.start()
    # atexit.register(lambda: scheduler.shutdown())
    # atexit.register(lambda: scheduler.remove_all_jobs())
    ## sync end
    main.run(host='0.0.0.0',port='5000', threaded=True)