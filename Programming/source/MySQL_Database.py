"""
使用MySQL数据库存储数据。
"""
import pymysql


class Database:
    """
    封装了pymysql模块的类，用于辅助操作数据库
    没有SQL注入的防范措施（考核不至于吧）
    """
    def __init__(self, host, user, password, database, port=3306):
        """
        初始化数据库对象
        :param host: 数据库地址
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名
        :param port: 端口
        """
        self.available = False
        print('[Database] Connecting to MySQL...')
        self.__host = host
        self.__user = user
        self.__password = password
        self.__name = database
        self.__port = port
        try:
            self.db = pymysql.connect(host=self.__host,
                                      user=self.__user,
                                      passwd=self.__password,
                                      port=self.__port)
            self.cur = self.db.cursor()
            print('[Database] Initialize database...')
            self.cur.execute('show databases;')
            self.__database_list = list(self.cur.fetchall())
            # 判断数据库是不是已经存在，不存在就新建数据库
            if (self.__name.lower(),) in self.__database_list:
                print('[Database] Database: ' + self.__name + ' already exists.')
            else:
                self.cur.execute('create database ' + self.__name)
                self.db.commit()
                print('[Database] Database: ' + self.__name + ' does not exist. Created successfully.')
            self.cur.execute('use ' + self.__name + ';')
            # 如果不存在数据表就新建表
            self.__cmd = """create table if not exists students(
            id int unsigned not null,
            name varchar(10) not null,
            sex int unsigned not null,
            school varchar(30) not null,
            major varchar(30) not null,
            grade int unsigned not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            self.cur.execute(self.__cmd)
            self.db.commit()
            self.available = True
        except Exception as e:
            print(e)

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
        self.__cmd = """insert into students
        (id, name, sex, school, major, grade)
        value
        ( {0}, '{1}', {2}, '{3}', '{4}', {5} );
        """.format(str(stu_id), name, str(sex), school, major, str(grade))
        try:
            self.cur.execute(self.__cmd)
            self.db.commit()
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
        if order:
            self.__cmd = """select * from students where {0}='{1}' order by {2} {3};
                        """.format(label, str(obj), field, way)
        else:
            self.__cmd = """select * from students where {0}='{1}';
            """.format(label, str(obj))
        self.cur.execute(self.__cmd)
        return list(self.cur.fetchall())

    def get_all_data(self, order=False, field=None, way='ASC'):
        """
        获取全部数据
        :return: 全部数据的列表
        """
        if order:
            self.__cmd = """select * from students order by {0} {1};
            """.format(field, way)
        else:
            self.__cmd = """select * from students;
            """
        self.cur.execute(self.__cmd)
        return list(self.cur.fetchall())

    def remove_data(self, stu_id):
        """
        删除数据
        :param stu_id: 学号
        :return: None
        """
        try:
            __data_list = list(self.get_data('id', stu_id))
            if len(__data_list) == 0:
                print('[Database] Error: There is no student with such ID!')
                return
            self.__cmd = """delete from students where id={0};
            """.format(str(stu_id))
            self.cur.execute(self.__cmd)
            self.db.commit()
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
            __data_list = list(self.get_data('id', stu_id))
            if len(__data_list) == 0:
                print('[Database] Error: There is no student with such ID!')
                return
            self.__cmd = """update students set {0}='{1}' where id={2};
            """.format(label, obj, stu_id)
            self.cur.execute(self.__cmd)
            self.db.commit()
            print('[Database] Successfully updated student with ID ' + str(stu_id))
        except Exception as e:
            print('[Database] Error:')
            print(e)

    def close(self):
        self.db.close()
