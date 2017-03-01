# Livia Python Sync Tool

This tool pulls down HTML out of a MySQL database and stores them as HTML files and also uploads those HTML files back into the MySQL database again.

It is for a proprietary CMS I have to use occasionally.

## Usage

You need python3 and a number of packages.  Create a config.json file or take the included example and change it's values to be correct.

```
{
    "mysql_host":"localhost",
    "mysql_user":"user",
    "mysql_password":"password",
    "mysql_database":"database"
}
```

Put it in a folder where you want your content so it looks like this:

```
content_folder/
	templates/
	uploads/
	config.json
```

The idea is you can keep the content folder in it's own separate source control but how you choose to use it is your deal.

The python script does not upload upload files.  I just use rsync for that, you can use whatever.  As long as the config.json is in the parent folder of the templates folder you should be set.

From there, run main.py like such:

```
python3 main.py -c /path/to/config.json -o download
python3 main.py -c /path/to/config.json -o upload
```

The uploader should only update records that have matching files in the templates folder.  Take backups and use this at your own peril.

## CentOS 7

For some reason CentOS 7 does not have Python 3 in it's default repositories.  

Thankfully DigitalOcean understands:
https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7

Alternatively if you are lazy and willing to post root commands from someone on the internet you can do this:

```
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm;\
sudo yum -y install python35u-3.5.2 python35u-pip python35u-devel;\
sudo yum install mysql-devel gcc;\
sudo pip3.5 install ftfy mysqlclient;
```

You might want to fix the symlinks instead of typing pip3.5 or python3.5:
```
sudo ln -s /usr/bin/python3.5 /usr/bin/python3;\
sudo ln -s /usr/bin/pip3.5 /usr/bin/pip3
```
