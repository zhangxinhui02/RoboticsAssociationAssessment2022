"""
由于担心数据存储也是考核的一部分，所以又写了这个模块以代替MySQL_Database模块。
这个模块使用Python原生的字典及yaml文件存储数据到本地文件，无需连接MySQL数据库。
封装接口与MySQL_Database模块几乎完全一致，简单修改引入的模块名即可使用。
"""
import yaml


class Database:
    """
    模拟数据库
    """
    def __init__(self, path):
        """
        初始化数据库对象
        :param path: 存储数据的yaml文件路径
        """
        self.available = False
        self.__path = path
        self.db = []
        print('[Database] Checking the YAML file...')
        try:
            with open(self.__path, 'r') as f:
                self.db = yaml.safe_load(f)
                if self.db is None:
                    self.db = []
            with open(self.__path, 'w+') as f:
                self.__dump()
                print('[Database] Successfully initialized!')
                self.available = True
        except Exception as e:
            print(e)

    def __dump(self):
        with open(self.__path, 'w+') as f:
            yaml.dump(self.db, f)

    def add_data(self, stu_id, name, sex, school, major, grade):
        """
        新增数据
        :param stu_id: 学号
        :param name: 姓名
        :param sex: 性别
        :param school: 学院
        :param major: 专业
        :param grade: 年级
        :return: None
        """
        __data_list = list(self.get_data('id', stu_id))
        if len(__data_list) != 0:
            print('[Database] Error: There is student with the same ID!')
            return
        __new_data = {'id': stu_id, 'name': name, 'sex': sex, 'school': school, 'major': major, 'grade': grade}
        self.db.append(__new_data)
        try:
            self.__dump()
            print('[Database] Successfully added student with ID ' + str(stu_id))
        except Exception as e:
            print('[Database] Error:')
            print(e)

    def get_data(self, label, obj, order=False, field=None, way='ASC'):
        """
        查询指定的数据
        :param label: 要查询的属性
        :param obj: 查询值
        :param order: 是否排序
        :param field: 要排序的属性
        :param way: 升序或降序（默认升序）[ASC/DESC]
        :return:匹配到的列表
        """
        __temp_list = []
        __temp_sort_list = []
        __temp_sorted_list = []
        for i in self.db:
            if str(i[label]) == obj:
                __temp_list.append(i)
        if order:
            for j in __temp_list:
                __temp_sort_list.append(str(j[field]) + '$' + str(j['id']))
            if way == 'ASC':
                __temp_sort_list.sort()
            else:
                __temp_sort_list.sort(reverse=True)
            for k in __temp_sort_list:
                for m in __temp_list:
                    if k.split('$')[1] == str(m['id']):
                        __temp_sorted_list.append(m)
        else:
            __temp_sorted_list = __temp_list
        # 转换为元组以匹配接口
        __temp_converted_list = []
        for n in __temp_sorted_list:
            __temp_converted_list.append((n['id'], n['name'], n['sex'], n['school'], n['major'], n['grade']))
        __temp_converted_list = tuple(__temp_converted_list)
        return __temp_converted_list

    def get_all_data(self, order=False, field=None, way='ASC'):
        """
        获取全部数据
        :return: 全部数据的列表
        """
        __temp_sort_list = []
        __temp_sorted_list = []
        if order:
            for j in self.db:
                __temp_sort_list.append(str(j[field]) + '$' + str(j['id']))
            if way == 'ASC':
                __temp_sort_list.sort()
            else:
                __temp_sort_list.sort(reverse=True)
            for k in __temp_sort_list:
                for m in self.db:
                    if k.split('$')[1] == str(m['id']):
                        __temp_sorted_list.append(m)
        else:
            __temp_sorted_list = self.db
        # 转换为元组以匹配接口
        __temp_converted_list = []
        for n in __temp_sorted_list:
            __temp_converted_list.append((n['id'], n['name'], n['sex'], n['school'], n['major'], n['grade']))
        __temp_converted_list = tuple(__temp_converted_list)
        return __temp_converted_list

    def remove_data(self, stu_id):
        """
        删除数据
        :param stu_id: 学号
        :return: None
        """
        try:
            __data_list = self.get_data('id', stu_id)
            if len(__data_list) == 0:
                print('[Database] Error: There is no student with such ID!')
                return
            for i in self.db:
                if i['id'] == stu_id:
                    self.db.remove(i)
            self.__dump()
            print('[Database] Successfully removed student with ID ' + str(stu_id))
        except Exception as e:
            print('[Database] Error:')
            print(e)

    def update_data(self, stu_id, label, obj):
        """
        修改数据
        :param stu_id: 学号
        :param label: 属性
        :param obj: 修改的内容
        :return: None
        """
        try:
            __data_list = self.get_data('id', stu_id)
            if len(__data_list) == 0:
                print('[Database] Error: There is no student with such ID!')
                return
            if label in ['id', 'sex', 'grade']:
                obj = int(obj)
            for i in self.db:
                if i['id'] == stu_id:
                    i[label] = obj
            self.__dump()
            print('[Database] Successfully updated student with ID ' + str(stu_id))
        except Exception as e:
            print('[Database] Error:')
            print(e)

    def close(self):
        pass
