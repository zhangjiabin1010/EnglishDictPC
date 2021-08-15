#!/usr/bin/python
# coding: utf-8
import sqlite3
import os


class simpleToolSql():
    """
    simpleToolSql for sqlite3
    简单数据库工具类
    编写这个类主要是为了封装sqlite，继承此类复用方法
    """

    def __init__(self, filename="stsql"):
        """
        初始化数据库，默认文件名 stsql.db
        filename：文件名
        """
        self.filename = filename + ".db"
        self.db = sqlite3.connect(self.filename)
        self.c = self.db.cursor()

    def close(self):
        """
        关闭数据库
        """
        self.c.close()
        self.db.close()

    def execute(self, sql, param=None):
        """
        执行数据库的增、删、改
        sql：sql语句
        param：数据，可以是list或tuple，亦可是None
        retutn：成功返回True
        """
        try:
            if param is None:
                self.c.execute(sql)
            else:
                if type(param) is list:
                    self.c.executemany(sql, param)
                else:
                    self.c.execute(sql, param)
            count = self.db.total_changes
            self.db.commit()
        except Exception as e:
            print(e)
            return False, e
        finally:
            self.close()
        if count > 0:
            return True
        else:
            return False


    def query(self, sql, dict_mark=False, param=None):
        """
        查询语句
        sql：sql语句
        param：参数,可为None
        retutn：成功返回True
        """
        try:
            result = []
            if param is None:
                if dict_mark:
                    self.c.execute(sql)
                    fields = [desc[0] for desc in self.c.description]
                    rst = self.c.fetchall()
                    if rst:
                        result = [dict(zip(fields, rows)) for rows in rst]
                else:
                    self.c.execute(sql)
                    result = self.c.fetchall()

            else:
                self.c.execute(sql, param)
                result = self.c.fetchall()
            return result
        except Exception as e:
            result = str(e)
            return result

        finally:
            self.close()


if __name__ == "__main__":
    """
    测试代码
    """
    sql = simpleToolSql("data")
    selectSql = "select * from EnglishDic where IELTS = '1' order by random() limit 3;"
    res = sql.query(selectSql,dict_mark=True)
    print(res)
    # sql.execute("insert into test (id,name) values (?,?);", (3, 'bac'))
    # sql.execute("update EnglishDic set REMARK = '8' WHERE word = 'vacant';")
    # res = sql.query("select * from test where id=?;", (3,))
    sql.close()