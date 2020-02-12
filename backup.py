#!/usr/bin/python3

import sys
import os
import shutil
import datetime


backup_days_duration = 3
db_host = 'localhost'

def dump_database(db, db_backup_directory_path, db_user, db_user_pw):
    dumpcmd = "mysqldump -h " + db_host + " -u " + db_user + " -p" + db_user_pw + " " + db + " > " +  "/tmp/" + db + ".sql"
    os.system(dumpcmd)
    return db + ".sql"


def get_file_age(file):
    file_path = os.path.join(os.getcwd(), file)
    file_age = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    return file_age


def remove_old_backups(db_backup_directory_path):
    os.chdir(db_backup_directory_path)
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            time_diff = datetime.datetime.today() - get_file_age(file) 
            if   time_diff.days > backup_days_duration:
                os.remove(os.path.join(os.getcwd(), file))

def main(argv):
    print("Will perform db backup now")
    if(len(argv) != 6):
        print("incorrect usage\n usage: backup.py <db_dir> <db_backup_dir> <db_name> <db_user_name> <db_user_pw>")
        return 1
    
    db_directory_path = argv[1]
    db_backup_directory_path = argv[2]
    db_name = argv[3]
    db_user = argv[4]
    db_user_pw = argv[5]

    os.chdir(db_directory_path)
    for root, dirs, files in os.walk(db_directory_path):
        for file in dirs:
            if file == db_name:
                current_date_suffix = "_" + datetime.datetime.today().strftime('%Y-%m-%d-%H-%M')
                db_bk_name = dump_database(file, db_backup_directory_path, db_user, db_user_pw)
                split_file = os.path.splitext(db_bk_name)
                shutil.copyfile("/tmp/"+ db_bk_name, os.path.join(db_backup_directory_path, split_file[0] + current_date_suffix + split_file[1]))
                os.remove("/tmp/"+ db_bk_name)
                break
    remove_old_backups(db_backup_directory_path)

if __name__ == "__main__":
   main(sys.argv)
