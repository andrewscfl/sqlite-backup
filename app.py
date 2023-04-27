import schedule
import sys
import os
import requests
import shutil
from time import sleep
import datetime

class BackupSystem:
    def __init__(self):
        # get command line args 
        arguments = sys.argv[1:]

        # show help flag
        if '--help' in arguments:
            self.render_help()
            sys.exit()

        # map items by flag
        self.arg_helper(arguments)

    
        # check if self.db_file_path is a valid file and self.backup_folder_path is a valid folder
        # if not, show help and exit
        if not os.path.isfile(self.db_file_path):
            print("Invalid db file path")
            self.render_help()
            sys.exit()

        # if self.backup_folder_path is not a valid folder or endpoint, show help and exit
        if not os.path.isdir(self.backup_folder_path):
            print("Invalid backup folder path")
            self.render_help()
            sys.exit()

        # setup backup jobs
        self.run()

    def arg_helper(self,argList):
        argument_dict = {
            '-i': 'db_file_path',
            '-o': 'backup_folder_path',
            '-e': 'external_url',
            '-t': 'time_stamp'
        }

        for idx,item in enumerate(argList):
            if item in argument_dict:
                next_element = idx + 1
                if next_element < len(argList):
                    setattr(self,argument_dict[item],argList[next_element])
                


    def run_external_backup(self):
        try:
            files = {'file': open(self.db_file_path, 'rb')}
            requests.post(self.external_url, files=files)
        except:
            print("Invalid external url")
            self.render_help()
            sys.exit()

    def log_progress(self,status, remaining, total):
        print(f'Copied {total-remaining} of {total} pages...')

    def run_internal_backup(self):
        print(self.db_file_path, self.backup_folder_path)
        backup_location = self.backup_folder_path + f'/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}backup_database.db'
        
        # copy file to backup folder
        shutil.copyfile(self.db_file_path, backup_location, follow_symlinks=True)

        print(f'[{datetime.datetime.now()}]: Backup Job Completed 🎉') 


    def backup(self):
        print(f'[{datetime.datetime.now()}]: Starting Backup Job 🚀')
        if hasattr(self,'external_url'):
            self.run_external_backup()
        else:
            self.run_internal_backup()


    def run(self):
        self.schedule = schedule
        # run backup job every day at midnight
        if hasattr(self,'time_stamp'):
            print('timestamp for running ', self.time_stamp)
            self.schedule.every().day.at(self.time_stamp.strip()).do(self.backup)
        else:
            self.schedule.every().day.at('00:00').do(self.backup)
        print(f'[{datetime.datetime.now()}]: Started Backup Job Scheduler 👋')
        while True:
            self.schedule.run_pending()
            # sleep till next minute
            sleep(60)

    def render_help(self):
        print(
        """
        Usage: python3 app.py <path to db file> <path to destination folder or server>

        Options:
            --help     Show this screen.
            -i         Path to database file
            -o         Path to destination folder
            -e         External URL to send backup to
            -t         Time to run backup job (24 hour format)
                
        """
        )


if __name__ == "__main__":
    backup = BackupSystem()
    backup.run()