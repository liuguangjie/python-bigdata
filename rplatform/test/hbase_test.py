#!/usr/bin/python
# -*- coding: utf-8 -*-
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from hbase import Hbase
from hbase.ttypes import *



class HbaseApi(object):


    def __init__(self, hostname='192.168.56.12', port='9090'):

        #初始化变量
        self.tableName = ''

        '''
         创建链接
        '''
        self.socket = TSocket.TSocket(hostname, port)


        self.ttransport = TTransport.TBufferedTransport(self.socket)

        self.protocol = TBinaryProtocol.TBinaryProtocol(self.ttransport)

        self.client = Hbase.Client(self.protocol)
        self.ttransport.open()

    """
     释放资源
    """
    def __del__(self):
        self.ttransport.close()
        self.socket.close()
    """
    向 hbase数据库 添加表和 添加列族
    """
    def createTable(self, columnFamilies):
        #判断 表释放存在 存在不创建 , 不存在 创建
        tables = self.client.getTableNames()

        if self.tableName not in tables:
            # 定义 列族 user, address,
            columns = []
            for column in columnFamilies:
                columns.append(Hbase.ColumnDescriptor(column))

            self.client.createTable(self.tableName, columns)
            print('创建成功')
        else:
            print("表明已经创建了")
            print(self.client.isTableEnabled(self.tableName))




    """
    添加行 或修改行
    """
    def putRow(self, rowName, rowKey, **keys):
        # 插入数据。如果在test表中row行cf:a列存在，将覆盖

        columns = []
        for k in keys:
            name = rowName + ':' + k
            value = keys[k]
            #必须要写 column=name, value=value 参数形式 不然要报错
            columns.append(Hbase.Mutation(column=name, value=value))

        self.client.mutateRow(self.tableName, rowKey, columns)


    """
    删除行
    """
    def delRow(self, rowKey, column=None):

        #删除整行
        if column == None:
            self.client.deleteAllRow(self.tableName, rowKey)
        else:
            #删除 rowKey 指定的 user:age 行
            self.client.deleteAll(self.tableName, rowKey, column)


    """
    根据id获取行 列表
    """

    def queryRow(self, rowKey, column=None):
        scannerId = self.client.scannerOpen(self.tableName, rowKey, column)
        while True:
            result = self.client.scannerGet(scannerId)
            if not result:
                break
            for res in result:

                for k in res.columns:
                    print(k)
                    print(res.columns[k].value)




api = HbaseApi()
api.tableName = 'test_'
#创建 表 和列族
#api.createTable(['user', 'address'])

#创建 或更新 一条记录
#api.putRow('user', 't1', name='test1', age='7777')

#删除 rowKey
#api.delRow('t1')


#获取 rowKey

api.queryRow('t1', ['user:age', 'user:name'])




