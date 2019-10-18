# -*- coding:utf8 -*-
#excelCompare用于两个相同表头的表格做比较，可指定需要比较的列名，获得新增、减少和相同项。
#指定列的值相同的行被认定为相同行，将被去重，且被判定为相同项，所以指定的列必须能唯一确定一行（通数据库主键）。
#不指定列名，则比较所有列。
#依赖组件：pandas,xlrd
#解释器：python3.x
#用法：python excelCompare.py <old.xlsx> <new.xlsx> <key1,key2,key3...>


####################################################
# 发布：2019年10月18日                              #
# https://github.com/shashade250/mytools           #
####################################################


import pandas
import time
import sys
import os
import re

def compare(oldPath,newPath,keys):
    data1=pandas.read_excel(oldPath, 'Sheet1', index_col=None) 
    data2=pandas.read_excel(newPath, 'Sheet1', index_col=None) 
    keys1=data1.keys().tolist()
    keys2=data2.keys().tolist()
    #check
    if keys1!=keys2:
        print('两个表格表头不一致，不能比对！')
        return
    if keys==[]:
        keys=keys1
    elif not set(keys).issubset(set(keys1)):
        print('请在表头内选择关键字！')
        return
    
    #取交集，为相同项
    print('正在比对，查找相同项...')
    data1AndData2=pandas.merge(data1,data2,on=keys)
    keys_y=[i+'_y' for i in (set(keys1)-set(keys))]
    keys_x={x+'_x':y for x,y in zip(set(keys1)-set(keys),set(keys1)-set(keys))}
    data1AndData2.drop(keys_y, axis=1, inplace=True)
    data1AndData2.rename(columns=keys_x, inplace = True)
    #取差集，为新增项
    print('正在比对，查找新增项...')
    addObj=data2.append(data1AndData2).drop_duplicates(subset=keys,keep=False)
    addObj.insert(data1.shape[1],'对比结果','新增') 
    #取差集，为减少项
    print('正在比对，查找减少项...')
    subObj=data1.append(data1AndData2).drop_duplicates(subset=keys,keep=False)
    subObj.insert(data1.shape[1],'对比结果','减少') 
    data1AndData2.insert(data1.shape[1],'对比结果','相同')
    #输出文件
    print('正在整合数据...')
    data1AndData2.append(addObj).append(subObj).to_excel(os.getcwd()+r'\compare_{}.xlsx'.format(time.strftime("%Y%m%d%H%M%S", time.localtime())),index=False)
    print('输出excel文件为'+os.getcwd()+r'\compare_{}.xlsx'.format(time.strftime("%Y%m%d%H%M%S", time.localtime())))

if __name__=='__main__':
    if len(sys.argv)==4:
        compare(sys.argv[1],re.split(',|，',sys.argv[2],sys.argv[3]))
    elif len(sys.argv)==3:
        compare(sys.argv[1],sys.argv[2],[])
    else:
        print('Usage: '+sys.argv[0]+' <old.xlsx> <new.xlsx> [key1,key2,key3...]')
        print('Example: 从销售统计表中过的本季度新上线产品和下架产品\npython3'+sys.argv[0]+' 上季度销量统计.xlsx 本季度销量统计.xlsx 产品名称,产品编号')
        

