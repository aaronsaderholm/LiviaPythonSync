import MySQLdb
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
template_path = dir_path + "/templates"

if not os.path.exists(template_path):
    os.makedirs(template_path)

credentials = [line.rstrip('\n') for line in open(dir_path + "/.mysql_info")]

db = MySQLdb.connect(credentials[0], credentials[1], credentials[2], credentials[3])
c = db.cursor()

c.execute("""SELECT idCMSLayout, LayoutMarkup from livia.CMSLayout""")
result = c.fetchone()

while result is not None:
    file = template_path + "/%s.html" % (result[0])
    f = open(file, 'w')

    if result[1] is None:
        continue

    f.write(str(result[1]))

    f.close()
    result = c.fetchone()
