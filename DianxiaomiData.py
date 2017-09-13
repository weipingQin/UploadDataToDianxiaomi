# coding= utf-8
import sqlite3
import xlrd

def initDB():
	print '----initDB Success-----'
	return sqlite3.connect('dianxiaoer.db');


def executeSQL(conn,sqlstr):
	print '----executeSQL-----'
	conn.cursor().execute(sqlstr);
	conn.cursor().commit();
	print '----executeSQLSuccess-----'

def createTable(conn):
	print '----startCreateTable-----'
	sql = 'create table if not exists shopdata (Id integer primary key autoincrement not null,ProductId text default null,ProductName text not null,Description text not null,Tags text not null,[Parent UniqueId] text not null,UniqueId text not null,Price real,Quantity integer not null,Shipping integer not null,[Main Image URL] text not null,[Extra Image URLList] text default null)'
	conn.cursor().execute(sql);
	conn.commit();
	print '----startCreateTableSuccess-----'

### 将数据库中的imageurl 更新成fileId
def update_db_picurl_tofileId(parentSKU,fileId,conn):
	print '----startUpdatePicID-----'
	cursor = conn.cursor();
	# 更新的数据库语句 update data set [Main Image URL] = '2.jpg'where [Parent UniqueId]= 'ZYH-YDEJ-0001;
	cursor.execute('update shopdata set [Main Image URL] =(?) where [Parent UniqueId]=(?)',(fileId,parentSKU))
	conn.commit()
	print '----endUpdatePicID-----'
	
def insertData(conn):
	print '----insertData-----'
	cursor = conn.cursor();
	## 首先从execel中获取数据
	data = xlrd.open_workbook('data.xls')
	table =data.sheets()[0]
	nrows = table.nrows;
	nclos = table.ncols;
	row_list = []
	for rownum in range(1,nrows):
		row = table.row_values(rownum);
		row_list.append(row)
		n = rownum-1;
		parentId = row_list[n][2];
		print 'parentId', parentId;
		#showAllData(conn)
		sql1 = "select * from shopdata where `Parent UniqueId`=(?)"
		cursor.execute(sql1,[parentId]);
		res = cursor.fetchall();
		if(len(res) > 0):
			print '该条数据已存在!'
		else:
			str = row_list[n][5]+row_list[n][6];
			print '------tags-----',str
			print '------excel table data test-------'
			print row_list[n][1]
			print row_list[n][2] # sku
			print row_list[n][3] # productName
			print row_list[n][4] # describe
			print row_list[n][5] # tags
			print row_list[n][6] # 第二个tags
			print row_list[n][7] # MSRP
			print row_list[n][8] # price
			print row_list[n][9] # shipping
			print row_list[n][10] # send date
			print row_list[n][11] # quantity
			print row_list[n][12] # color
			print row_list[n][13] # size
			print row_list[n][14] # price
			print row_list[n][15] # send price
			print '------excel table data test end-------'
			cursor.execute("insert into shopdata(ProductName,Description,Tags,[Parent UniqueId],UniqueId,Price,Quantity,Shipping,[Main Image URL],[Extra Image URLList])values(?,?,?,?,?,?,?,?,?,?)",
									  (row_list[n][3],row_list[n][4],str,row_list[n][2],'',row_list[n][8],row_list[n][11],row_list[n][10],'1.jpg','jsonstringlist'))
		
			conn.commit()
	print '----insertDataSuccess-----'
	
#######将数据库所有的数据拿出来转化成list 
def showAllData(conn):
	print '----AllDataShowing-----'
	cursor = conn.cursor();
	###########列名称#################
	#col_name_list = [tuple[0] for tuple in cursor.description];
	#print col_name_list;
	alldata = [];
	results = cursor.execute('select * from shopdata').fetchall()
	result = list(results)
	items = {}
	for shopitemdata in result:
		print shopitemdata;
	print '----AllDataShowingEnd-----'
	return result;

def get_fileId_And_SkufromDB(result):
	print '------start 组装数据库字段--------'
	items = {}
	for shopitemdata in result:
		# index = 9是图片
	    items[shopitemdata[5]] = shopitemdata[10]
	return items;
	print 'items--',items;
	print '------end 输出对应的hashMap--------'

def main():
    conn = initDB();
    createTable(conn);
    insertData(conn);
 #   showAllData(conn);
    
if __name__ == '__main__':
    main()


