import pymysql

def get_connection():
    return pymysql.connect(
        host="8.135.101.43",
        port=3607,
        database="Sentiment57",
        user="hzwuser",
        password="Q7fUer0dy4LDeAak",
    )
def query_db(sql):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute(sql)
        data=cursor.fetchall()
        return data

def insert_db(sql,value):
    try:
        # sql = "INSERT INTO `sentiment_material` (`mid`, `keywork`, `platform`,`location`,`title`,`status`) VALUES (%s, %s, %s,%s, %s, %s)"
        # values = ('value1', 'value2', 'value3','value1', 'value2', 'value3')
        # sql='INSERT INTO `user_info` ("","","") values(%s);'
        with get_connection() as con:
            cursor=con.cursor()
            cursor.execute(sql,value)
            con.commit()
            return True
    except Exception as e:
        print(e)
    return  False
# insert_db("","")
#
# data=query_db("select * from sentiment_source_keyword where status=0 limit 1")
# print(data[0][0])