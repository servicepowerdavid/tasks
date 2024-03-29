# -*- coding: utf-8 -*-
"""tasks.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_yL83gz70VNrkXZMz5OA4-P4I-9Y9mED
"""
import datetime, os, pickle, argparse
from colors import color


def initialize():
    taskCount = 0
    innerTaskList = []
    masterTaskList = {'Tasks': innerTaskList,
                      'Task Count': taskCount}
    return masterTaskList, innerTaskList, taskCount


# If no datafile exists, create empty variables and new data file
if 'data.pkl' not in os.listdir():
    (masterTaskList, innerTaskList, taskCount) = initialize()
    with open('data.pkl', mode='wb') as f:
        pickle.dump(masterTaskList, f)
# Otherwise, read in data file and assign variables
else:
    with open('data.pkl', mode='rb') as f:
        masterTaskList = pickle.load(f)
        innerTaskList = masterTaskList['Tasks']
        taskCount = masterTaskList['Task Count']

parser = argparse.ArgumentParser(description='Simple task manager')
parser.add_argument("--add", help="Adds a new task.")
parser.add_argument("--list", help="Lists all tasks, sorted by status. Displays taskIDs.",
                    action="store_true")
parser.add_argument("--stop", help="Stop task based on ID, changing status to 'complete'.",type=int)
parser.add_argument("--delete", help="Deletes task based on ID from list.", type=int)
#parser.parse_args()
args = parser.parse_args()


def newTask(name):
    global taskCount
    taskCount += 1
    startTime = datetime.datetime.now()
    taskStatus = 'In Progress'    
    taskName = name
    return{'Name': name,
           'Status' : taskStatus,
           'Start Time': startTime,
           'ID' : taskCount}


def updateMasterList(tasks):
    global masterTaskList
    masterTaskList = {
                'Task Count' : len(masterTaskList['Tasks']),
                'Tasks' : tasks
            }
    with open('data.pkl','wb') as f:
        pickle.dump(masterTaskList, f)


if args.add:
    print(f'\nAdding Task: {args.add}')
    innerTaskList.append(newTask(f'{args.add}'))
    updateMasterList(innerTaskList)
    print(f'\nTotal Task Count: {taskCount}')
elif args.list:
    print("\n" + color(('Current Tasks').center(31,'='), fg="#399CFF") + "\n")
    for task in innerTaskList:
        if task['Status'] == 'In Progress':
            print(f"Name: {task['Name']} - "
                  f"Status: {task['Status']} - "
                  f"Task ID: {task['ID']}")
    print("\n" + color(('Completed Tasks').center(31, '='), fg='green') + "\n")
    #print('\n' + ('Completed Tasks').center(31,'='))
    for task in innerTaskList:
        if task['Status'] == 'Complete':
            print(f"Name: {task['Name']} - "
                  f"Status: {task['Status']} - "
                  f"Time Spent: {task['Total Time']} - "
                  f"Task ID: {task['ID']}")
elif args.delete:
    count = 0
    for task in innerTaskList:
        count += 1
        if task['ID'] == args.delete:
            print(f"\nDeleted Task: {task['Name']}")
            innerTaskList.pop(count-1)
            updateMasterList(innerTaskList)
elif args.stop:
    for task in innerTaskList:
        if task['ID'] == args.stop:
            startTime = task['Start Time']
            totalTaskTime = datetime.datetime.now() - startTime
            task.update([('End Time', datetime.datetime.now()), ('Status', 'Complete'), ('Total Time', totalTaskTime)])
            updateMasterList(innerTaskList)
            print(f'\nTask Completed. Total Time Spent: {totalTaskTime}')
