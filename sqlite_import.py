__author__ = 'vamsi'


import sqlite3


def import_month_data(month):
    db=sqlite3.connect('/home/vamsi/Databases_sqlLite/taxi_data/taxi_data')
    cursor=db.cursor()

    if month<10:
        cond1='2015-'+'0'+str(month)+'-'+'01'
        cond2='2015-'+'0'+str(month+1)+'-'+'01'
    elif month>=10 and month<12:
        cond1='2015-'+str(month)+'-'+'01'
        cond2='2015-'+str(month+1)+'-'+'01'

    cursor.execute('''select * from taxi_data where sector<>'not in New York' and start_time between ? and ?''',(cond1,cond2))
    all_rows=cursor.fetchall()
    #for row in all_rows:
     #   print(row)

    return all_rows



if __name__=='__main__':
    import_month_data(3)