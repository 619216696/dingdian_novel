import pymysql
from dingdian import settings

mysql_host = settings.mysql_host
mysql_user = settings.mysql_user
mysql_password = settings.mysql_password
mysql_db = settings.mysql_db

db = pymysql.connect(host = mysql_host,user = mysql_user,password = mysql_password,db = mysql_db,charset = 'utf8')
cur = db.cursor()

class Sql:

    @classmethod
    def insert_dd_name(cls,xs_name,xs_author,category,name_id):
        sql = 'insert into dd_name (xs_name,xs_author,category,name_id) values (%(xs_name)s,%(xs_author)s,%(category)s,%(name_id)s)'
        value = {
            'xs_name': xs_name,
            'xs_author': xs_author,
            'category': category,
            'name_id': name_id
        }
        cur.execute(sql,value)
        db.commit()

    @classmethod
    def select_name(cls,name_id):
        sql = 'select exists(select 1 from dd_name where name_id=%(name_id)s)'
        value = {
            'name_id': name_id
        }
        cur.execute(sql,value)
        return cur.fetchall()[0]