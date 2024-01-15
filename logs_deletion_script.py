import os
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import shutil


def remove_180_days_older_logs(files_path):
    processes_files_path = files_path
    process_files = os.listdir(processes_files_path)

    for process in process_files:
        myFlag = False
        file_path = f"{files_path}/{process}/builds"
        if os.path.exists(file_path):
            
            files = os.listdir(file_path)
            print(files)
            files_int= [item for item  in files if item.isdigit()]
            files_int1=[int(item) for item in files_int if item.isdigit()]
            print(files_int1)         

            files_sort = sorted(files_int1)
            print("Files in the folder:", files_sort)
            for file in files_sort:
                try:
                    xml_file_path = f'{file_path}/{file}/robot-plugin/output.xml'
                    remove_job_file_path = f'{file_path}/{file}'
                    if os.path.exists(file_path):
                        files = os.listdir(file_path)
                        if os.path.exists(xml_file_path):
                            print(xml_file_path)
                            try:

                                tree = ET.parse(xml_file_path)
                                root = tree.getroot()
                            except ET.ParseError as e:
                                print(f"Error parsing XML file '{xml_file_path}': {e}")
                                continue
                            for msg_element in root.iter('msg'):
                                temp = msg_element.get('timestamp')
                                if temp:
                                    print(temp)
                                    original_datetime = datetime.strptime(temp, "%Y%m%d %H:%M:%S.%f")
                                    formatted_time = original_datetime.strftime("%Y-%m-%d")

                                    current_datetime = datetime.now()
                                    current_date = current_datetime.date()
                                    six_months_ago = current_date - timedelta(days=180)

                                    six_months_back_formatted =  six_months_ago.strftime("%Y-%m-%d")
                                    if formatted_time < six_months_back_formatted:
                                        print(True)
                                        if os.path.exists(remove_job_file_path):
                                            shutil.rmtree(remove_job_file_path)
                                            print(f"File '{remove_job_file_path}' has been successfully removed.")
                                    else:
                                        myFlag = True
                                        print("Break the loop")
                                        break
                                    break
                except FileNotFoundError:
                    print("file not found")

                if myFlag:
                     break

files_path ="/usr/local/Autosphere/Orchestrator/jobs/PtclCallCenter/jobs"
remove_180_days_older_logs(files_path)


