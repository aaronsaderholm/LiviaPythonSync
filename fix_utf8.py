locals()import MySQLdb
import os

# This removed 'bad UTF-8 characters' (or something)
# that in the database.

dir_path = os.path.dirname(os.path.realpath(__file__))
template_path = dir_path + "/templates"

if not os.path.exists(template_path):
    os.makedirs(template_path)

credentials = [line.rstrip('\n') for line in open(dir_path + "/.mysql_info")]

db = MySQLdb.connect(credentials[0], credentials[1], credentials[2], credentials[3])
cursor = db.cursor()

sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % credentials[3]
cursor.execute(sql)

results = cursor.fetchall()
for row in results:
  sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
  cursor.execute(sql)
db.close()
