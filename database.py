__author__ = 'elliott'

import sqlite3
conn = sqlite3.connect("record.db")
c = conn.cursor()
c.execute('''insert into records (username, record_text, record_date) values('test1', 'test2', 'test' )''')
conn.commit()
c.execute('''select * from records''')
print c.fetchall()