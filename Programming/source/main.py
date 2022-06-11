#!/usr/bin/python3
from MySQL_Database import Database
# from Pydict_Database import Database

# 使用MySQL_Database模块前需要填写MySQL数据库基本信息。
# 如果使用PyDict_Database则无需填写。
database_host = "127.0.0.1"
database_user = ""
database_password = ""
database_port = 3306
database_name = "StudentsData"

# 使用PyDict_Database模块前需要指定yaml文件的路径。
# 如果使用MySQL_Database则无需填写。
yaml_path = "./data.yaml"


def show_all():
    field = ''
    way = ''
    print('\n[Manager] Information of all students:')
    order = input('\tOrder the list? [Y/N]: ')
    if order in 'Yy' and order != '':
        order = True
    else:
        order = False
    if order:
        field = input('\tInput which label to order [id, name, sex, school, major, grade]: ')
        way = input('\tChoose how to order (1 for ASC, 2 for DESC): ')
        if way == '2':
            way = 'DESC'
        else:
            way = 'ASC'

    all_data_list = db.get_all_data(order, field, way)
    print('[Manager] (Sex 1 for Male, 2 for Female)')
    print('\tID\t\tName\t\tSex\tSchool\t\t\tMajor\t\t\tGrade')
    for i in all_data_list:
        print('\t{0}\t{1}\t\t{2}\t{3}\t{4}\t{5}'.format(i[0], i[1], i[2], i[3], i[4], i[5]))
    cmd = input('\nPress Enter...')


def add():
    print('\n[Manager] Add a new student:')
    stu_id = input('\tInput student\'s ID: ')
    try:
        stu_id = int(stu_id)
    except Exception as e:
        print(e)
        print('[Manager] Error: Not an int value! ')
        return
    name = input('\tInput student\'s name: ')
    sex = input('\tInput student\'s sex: (1 for Male, 2 for Female)')
    try:
        sex = int(sex)
        if sex != 1 and sex != 2:
            print('[Manager] Error: Not a correct value for sex! ')
            return
    except Exception as e:
        print(e)
        print('[Manager] Error: Not an int value! ')
        return
    school = input('\tInput student\'s school: ')
    major = input('\tInput student\'s major: ')
    grade = input('\tInput student\'s grade: ')
    try:
        grade = int(grade)
    except Exception as e:
        print(e)
        print('[Manager] Error: Not an int value! ')
        return
    db.add_data(stu_id, name, sex, school, major, grade)
    cmd = input('\nPress Enter...')


def update():
    print('\n[Manager] Update a student\'s information:')
    stu_id = int(input('\tInput student\'s ID: '))
    label = input('\tInput which label to update [id, name, sex, school, major, grade]: ')
    obj = input('\tInput the value after change: ')
    db.update_data(stu_id, label, obj)
    cmd = input('\nPress Enter...')


def remove():
    print('\n[Manager] Remove a student:')
    stu_id = int(input('\tInput the ID of student who will be removed: '))
    db.remove_data(stu_id)
    cmd = input('\nPress Enter...')


def search():
    print('\n[Manager] Search for some students:')
    field = ''
    way = ''
    label = input('\tInput which label to search [id, name, sex, school, major, grade]: ')
    obj = input('\tInput the value for search: ')
    order = input('\tOrder the list? [Y/N]: ')
    if order in 'Yy' and order != '':
        order = True
    else:
        order = False
    if order:
        field = input('\tInput which label to order [id, name, sex, school, major, grade]: ')
        way = input('\tChoose how to order (1 for ASC, 2 for DESC): ')
        if way == '2':
            way = 'DESC'
        else:
            way = 'ASC'
    data_list = db.get_data(label, obj, order, field, way)
    print('\tID\t\tName\t\tSex\tSchool\t\t\tMajor\t\t\tGrade')
    for i in data_list:
        print('\t{0}\t{1}\t\t{2}\t{3}\t{4}\t{5}'.format(i[0], i[1], i[2], i[3], i[4], i[5]))
    cmd = input('\nPress Enter...')


def menu():
    print('\n[Manager] Menu of Manage System:')
    print('\t1. Show information of all students.')
    print('\t2. Add a new student.')
    print('\t3. Update a student\'s information.')
    print('\t4. Remove a student.')
    print('\t5. Search for some students.')
    print('\t6. Exit.')
    cmd = input('Please choose: ')
    if cmd == '1':
        show_all()
    elif cmd == '2':
        add()
    elif cmd == '3':
        update()
    elif cmd == '4':
        remove()
    elif cmd == '5':
        search()
    elif cmd == '6':
        print('[Manager] Bye')
        db.close()
        exit(0)


if __name__ == '__main__':
    print('Students Data Manage System')
    print('by zhangxinhui02')
    print('GitHub: https://github.com/zhangxinhui02/RoboticsAssociationAssessment2022\n')

    print('[Manager] Connecting to database...')

    # 适用于MySQL_Database模块
    db = Database(database_host,
                  database_user,
                  database_password,
                  database_name,
                  database_port)

    # 适用于MySQL_Database模块
    # db = Database(yaml_path)

    if db.available is not True:
        print('[Manager] Database is not available!')
        exit(0)
    while True:
        menu()
