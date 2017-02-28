import MySQLdb
import os, time
import re


dir_path = os.path.dirname(os.path.realpath(__file__))
template_path = dir_path + "/templates"

if not os.path.exists(template_path):
    os.makedirs(template_path)

credentials = [line.rstrip('\n') for line in open(dir_path + "/.mysql_info")]

db = MySQLdb.connect(credentials[0], credentials[1], credentials[2], credentials[3])
c = db.cursor()
print("Connected.")
c.execute("""SELECT idCMSLayout, LayoutMarkup, Name from livia.CMSLayout""")
result = c.fetchone()

while result is not None:
    #print(result)
    # We scrub everything except alphabetic characters from the template name.
    # The uploader get the template id from the file name - so digits can't
    # be allowed here and other characters are a headache for a label.
    template_name = re.sub(r'[^a-zA-Z]', '', result[2])
    
    file = template_path + "/%s-%s.html" % (result[0], template_name)
    print("Reading template %s ... writing to %s" % (result[0], file))
    f = open(file, 'w')

    if result[1] is None:
        continue

    f.write(str(result[1]))
    f.close()

    result = c.fetchone()
    
    time.sleep(.25)
