from config.db import connect_db

class User(object):
    """
    Kelas User untuk akses login, register
    ---------
    Parameter : 
        - email
        - password
        - id_user
    """
    
    def __init__(self, **kwargs):
        """
        Constructor User \n
        Parameters : email, password, id_user
        """
        if len(kwargs)>0:
            self.email = kwargs.pop("email", None)
            self.password = kwargs.pop("password", None)
            self.id_user =  kwargs.pop("id_user", None)
        else:
            self.email = None
            self.password = None
            self.id_user =  None

    def read_user(self):
        """
        Baca email & password user 1 email
        """
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM user WHERE email=%s",[self.email])
            account = cur.fetchone()
            return account
        except Exception as e:
            return 'error :{}'.format(e)

    def cu_user(self):
        """
        Create account dan update id_user pada account
        """
        conn = connect_db()
        cur = conn.cursor()
        try:
            if self.id_user is None:
                cur.execute("UPDATE user SET password=%s WHERE email=%s",[self.password,self.email])
                print("update id_user executed")
            elif self.password is None:
                cur.execute("UPDATE user SET id_user=%s WHERE email=%s",[self.id_user,self.email])
                print("update id_user executed")
            else :
                cur.execute("INSERT INTO user (email,password,id_user) VALUES (%s, %s, %s)",[self.email,self.password, self.id_user])
                print("insert user executed")
            conn.commit()
        except Exception as error:
            conn.rollback()
            print("error :{}".format(error))
        finally:
            if (conn):
                cur.close()
                conn.close()
                print("MySql ditutup")
        return "selesai create update user" 