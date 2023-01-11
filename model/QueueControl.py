from config.db import connect_db

class QueueControl(object):
    """
    docstring
    """
    def __init__(self, **kwargs):
        """
        Inisiasi Objek QueueControl
        Parameter : id_arduino, id_user, perintah, 
        """
        if len(kwargs) > 0:
            self.id_arduino = kwargs.pop("id_arduino", None)
            self.id_user = kwargs.pop("id_user", None)
            self.perintah = kwargs.pop("perintah", None)
        else:
            self.id_arduino = None
            self.id_user = None
            self.perintah = None

    def queue_to_control(self):
        """
        untuk stack perubahan control jika response tidak ok
        Obj Control attr : id_arduino, id_user, perintah
        """
        conn=connect_db()
        cur=conn.cursor()
        try:
            cur.execute("INSERT INTO queue_control (id_arduino, id_user, perintah) VALUES(%s,%s,%s)", [
                            self.id_arduino, self.id_user, self.perintah])
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()
    
    def queue_clear(self):
        """
        Clear table queue_control
        """
        conn=connect_db()
        cur=conn.cursor()
        try:
            cur.execute("DELETE FROM queue_control")
            conn.commit()
        except Exception as e :
            print(e)
        finally:
            cur.close()
            conn.close()
    def queue_clear_id(self,idqueue):
        """
        Clear table queue_control
        """
        conn=connect_db()
        cur=conn.cursor()
        try:
            cur.execute("DELETE FROM queue_control where idqueue_control=%s",[idqueue])
            conn.commit()
        except Exception as e :
            print(e)
        finally:
            cur.close()
            conn.close()
        
    def read_queue_control(self):
        """
        Baca control yg ga ke submit
        """
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * from queue_control where id_arduino=%s",[self.id_arduino])
        list_control = cur.fetchall()
        if not list_control:
            list_control = "KOSONG"
        return list_control