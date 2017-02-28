import sys
import atexit
import MySQLdb
import os
import ftfy # This probably need to go.
import json
import os.path
import re
import time


sys.path.append(os.path.realpath('..'))

config = None
mysql_connection = None


def get_config(path):
    path = os.path.realpath(path)

    if os.path.isfile(path) is False:
        print("Could not open config file at: %s" % path)
        exit()

    f = open(path)

    with f as json_data:
        global config
        config = json.load(json_data)
        f.close()

    config['path'] = os.path.dirname(f.name)
    config['template_path'] = os.path.realpath(path + "/templates")
    print(config)
    open_mysql()
    exit()


def open_mysql():

    global config, mysql_connection

    mysql_connection = MySQLdb.connect(
        host= config['mysql_host'],
        user=config['mysql_user'],
        passwd=config['mysql_password'],
        db=config['mysql_database']
    )
    print("Opening mysql.")

    # atexit fires when exit() is called so we
    # close the mysql connection cleanly.

    atexit.register(close_mysql)
    return mysql_connection


def close_mysql():
    print("Closing mysql.")
    global mysql_connection
    if mysql_connection is not None:
        mysql_connection.close()
        mysql_connection = None
        return True

    return False


def upload_templates():
    global mysql_connection, config
    c = mysql_connection.cursor()

    template_path = config['template_path']

    for filename in os.listdir(template_path):
        if filename.endswith(".html"):
            f = open(template_path + "/" + filename, encoding="utf-8")
            html = f.read()
            idCMSLayout = int(filename.replace(".html", ""))

            if html is None:
                continue

            html = ftfy.fix_text(html)

            print(idCMSLayout)
            output = c.execute("""UPDATE livia.CMSLayout
                          SET LayoutMarkup=%s
                          WHERE idCMSLayout=%s""",
                               (html, idCMSLayout))
            mysql_connection.commit()
    c.close()


def download_templates():
    global mysql_connection, config
    c = mysql_connection.cursor()

    template_path = config['template_path']

    if not os.path.exists(template_path):
        os.makedirs(template_path)

    c = mysql_connection.cursor()
    print("Connected.")
    c.execute("""SELECT idCMSLayout, LayoutMarkup, Name from livia.CMSLayout""")
    result = c.fetchone()

    while result is not None:
        # print(result)
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


def main():
    config_path = None
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    if config_path is None:
        print("Missing config file path as first parameter.")
        exit()

    global config
    config = get_config(config_path)


if __name__ == '__main__':
    main()


