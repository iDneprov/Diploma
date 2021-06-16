import os

def is_interesting(filepath):
    for name in ('migrations', '__', 'DS_Store', '__pycache__'):
        if filepath.find(name) != -1:
            return False
    return True

for dir in ('Accountant', 'accounting', 'main', 'userPages'):
    for subdir, dirs, files in os.walk(dir):
        if not is_interesting(subdir):
            break
        print()
        print()
        print(subdir + ':')
        for file in files:
            filepath = subdir + os.sep + file
            if is_interesting(filepath):
                print('-', file)
                print()
                f = open(filepath)
                notComment = True
                for line in f.readlines():
                    '''if line.find('"""') == -1:
                        notComment = not notComment'''
                    if len(line) >= 2 and line.find('#') == -1: #and notComment:
                        print(line, end='')
                f.close()
                print()
