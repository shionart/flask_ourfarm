from MySQLdb import cursors, connect
import asyncio

sensor_not_sent = []


def stringed_sensor(a):
    """
    docstring
    """
    result = "0"
    for b in a:
        result+=" ,"+b
    return result

async def count_sensor():
    conn = connect(host ='localhost', port =3306 , user= 'root' , passwd='dragonica025', db='db_sister', cursorclass=cursors.DictCursor)
    cur = conn.cursor()
    cur.execute("select count(*) as jumlah from sensor where queue=0")
    c = cur.fetchone()
    print("jumlah posted data :")
    print(c['jumlah'])
    cur.close()
    conn.close()
    return c


async def delete_sensor():
    try:
        print("inisiasi delete table sensor")
        conn = connect(host ='localhost', port =3306 , user= 'root' , passwd='dragonica025', db='db_sister', cursorclass=cursors.DictCursor)
        cur = conn.cursor()
        cur.execute("delete from sensor where queue=0 order by time ASC limit 25000")
        conn.commit()       
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
    print("delete selesai")

async def housekeep_sensor():
    """
    docstring
    """
    jml = await count_sensor()
    if jml['jumlah'] >=40000 : 
        await delete_sensor()
    else : 
        print("Nothing to delete.")

async def main() :
    await housekeep_sensor()

if __name__ == '__main__':
    asyncio.run(main())