import MySQLdb
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
template_path = dir_path + "/templates"

credentials = [line.rstrip('\n') for line in open(dir_path + "/.mysql_info")]

db = MySQLdb.connect(credentials[0], credentials[1], credentials[2], credentials[3])
c = db.cursor()

for filename in os.listdir(template_path):
    if filename.endswith(".html"):
        f = open(template_path + "/" + filename)
        html = f.read()
        idCMSLayout = int(filename.replace(".html", ""))

        if html is None:
            continue

        output = c.execute("""UPDATE livia.CMSLayout
                      SET LayoutMarkup=%s
                      WHERE idCMSLayout=%s""",
                  (html, idCMSLayout))
        db.commit()
c.close()





