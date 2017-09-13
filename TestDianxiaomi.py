# coding= utf-8
import sqlite3
from pip._vendor import requests
from pip._vendor.requests.api import head
import json
import DianxiaomiData;

dianxiaomi_login_url = "https://www.dianxiaomi.com/home.htm?ts=1504952116"
dianxiaomi_add_product="https://www.dianxiaomi.com/smtProduct/add.htm";
dianxiaomi_save_product = "https://www.dianxiaomi.com/product/offlineEdit.json";
dianxiaomi_upload_pic_url ="http://www.dianxiaomi.com/album/getSign.json";

# 定义Http相关的头信息 
# # 定义Http相关的配置头信息 
user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Mobile Safari/537.36'
cookies = 'china-redirect=closed; app_locale=ZH; __utma=96128154.1058405477.1503758723.1504007266.1504611857.4; __utmc=96128154; __utmz=96128154.1503758723.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); IR_PI=1503758709034.mmyzlkysrw; IR_4953=1504611861028%7C0%7C1504611861028; __zlcmid=iFghtwr5BXMECa; rd="2|1:0|10:1504709274|2:rd|48:NDAwMTc3MjQtOGNjMS0xMWU3LTkyZjYtMDI2MjYzNTIxZTYy|0cdb1367f9f60742f1da1c18a07f8d7128f1e9d2ae5fdd37ed3753a67566d7d2"; remember_me=tangqiyunwish%40sina.com; bsid=33d4d18364534c6ca3da17bc5c51d13c; session="2|1:0|10:1504709274|7:session|84:MjAxNy0wOS0wNiAxNDo0Nzo1NC4wNzk0NjQ1ZDM4ZWIyYy05MzEyLTExZTctYTAzOC0wNjJlZmUwZmM0MjA=|c13b939df37b1f60eb07a509aa02de7cccef304223afb1828ebfa80da2e4e876"'
host = 'www.dianxiaomi.com'
origin = 'https://www.dianxiaomi.com'
referer = 'https://www.dianxiaomi.com/index.htm?ts=1504952074'
Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'


#### 添加产品get访问的相关参数  
host2='www.dianxiaomi.com'
referer2='https://www.dianxiaomi.com/smtProduct/add.htm'
Accpet2='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
cookie2 = 'dxm_vc=MDk2OTE2YmIxNDUyNjc3NjhmMjQwZjE1ZjlkMmVhYTQhMTUwNDk1MjA3NDk0Ng; dxm_i=MTQxODA0IWFUMHhOREU0TURRITY2ZmYxODYyMTdjNzE1MmM1YTU0MjExYzc3MDY3ZjVj; dxm_t=MTUwNDk1MjExNiFkRDB4TlRBME9UVXlNVEUyITBjY2Q2MzhiZTc2MjMxOTk2NjZmODI1ZDFjY2NlNzZh; dxm_c=SlJVVFNZdUghWXoxS1VsVlVVMWwxU0EhMGE2MWIyYTI3OWUzNzdhNWQ1ZTI5MzU0ZTg1MTcxOTU; dxm_w=NzhiY2YwOWFjZjc0YTRmZTM4YTZiOTgzNzg5N2IwMTAhZHowM09HSmpaakE1WVdObU56UmhOR1psTXpoaE5tSTVPRE0zT0RrM1lqQXhNQSE0Yjc2YTBiYWQ0YjExMzg3NDdhMjQ3ZTBjNzRmZGQ2Mg; dxm_s=L5R7h3MwDuVwXQlmZbJ23s6iM85iZN2EqYVXhHjknnU; JSESSIONID=A4162B5B0D9BB3BE9D69F9D1FCBAF245; Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1504323852,1504915538,1504950009,1504997047; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1505083884; sid=fa1ae5d9-bee8-4908-b3d4-5b0456b02283; rememberMe=5WXwg/M2Ko4/omPfVnnbzCq+92EUue86J77+IP7qNGffeVnXEGvADn4am0xrgi1zVMoXhoSMPfiwa3leKVqotQWwIcUh90gvysQwfHbhqp27wabfV0SFxapaFYGtEaEiH840Fd905iiuFApC5UWk7GXWszpDzR0+jiAWxJCJb7NAumiql4z8aMeMUgIBr2tHx2/RCQdGMg5a871ZOSD8ygP4EjRmqoX67klouNlFWLyUUmCcbsn+22P1T+f1JPzJTj0tuFGwJO3ekEz6fbzrC5TRlkTAUxTnmMl7UZdRGfV+/4aXtNLNzEPS/KBpCwBoptt6H2NCdsNrA+MyBCQUe/4h22+bGawD/KbCqvpiAZ6zix+f3j7fE7SB27NVi1XyL4KvC4tbwMtPMgpi4sbTPO9+y2SdvM+KGiBBUXCVUtdA9kv9658tODzGNJWJ9qO24flNdUfhwrNgHgpumAUNxomkSAMFnle+HW6GEbqfpUca2i1g3Knl06nPXvuk5TRqExuL9vYyIYxndJN9sA3oLs7VouGJkwp+tJgMOhzNVSlPmtlJl+RORUiMwU4/buAZ'

### 添加产品的post访问的参数 
Accept3 = 'application/json, text/javascript, */*; q=0.01'
ContentType='application/x-www-form-urlencoded; charset=UTF-8'

def get_headers(user_agent, cookies, host, origin, referer, Accept):
	   return {'User-Agent': user_agent, 'Cookie':cookies, 'Host':host, 'Origin':origin, 'Referer':referer, 'Accept':Accept}

## 访问电小秘网站的信息 
def get_content(url,data):
	headers = get_headers(user_agent,cookies,host,origin,referer,Accept);
	proxies = {'http':'http://117.158.1.210:9999','http':'http://60.174.237.43:9999','http':'http://221.237.154.57:9999','http':'http://219.150.242.54:9999','http':'http://183.62.71.242:3128'}
	res = requests.post(url,headers=headers,data=data).text.encode('utf-8')
	print res;
	
## 使用get方式来访问添加产品页面 获取cookie存入到本地的文件里 此处cookie先写死
def get_cookie_save_file(url):
	headers = get_headers(user_agent,cookie2,host2,'',referer2,Accpet2);
	#proxies = {'http':'http://117.158.1.210:9999','http':'http://60.174.237.43:9999','http':'http://221.237.154.57:9999','http':'http://219.150.242.54:9999','http':'http://183.62.71.242:3128'}
	res = requests.get(url,headers=headers).text.encode('utf-8')
	print res;

#上传图片返回相应的Key 	
def get_sign_fileId_fromserver(url,localImagePath):
	print '----send picture-----'
	headers = get_headers(user_agent,cookie2,host2,'',referer2,Accpet2);
	data = {'bucket':'wxalbum','fileName':localImagePath}
	res = requests.post(url,headers = headers,data= data).text.encode('utf-8')
	jsonstring = json.loads(res,'utf-8')
	print jsonstring;
	sign = jsonstring.get('sign');
	fileId =jsonstring.get('fileId');
	print 'get sign from server---',sign
	print 'fileId--',fileId;
	return fileId;
	print '---send picture end--'

### 上传图片到服务器
def upload_pic_toServer(sign,url):
	print 'upload_pic_toServer--start'
	
	print 'upload_pic_toServer--end'
	
def post_data_todianxiaomi(url):
	headers = get_headers(user_agent,cookie2,host2,'','https://www.dianxiaomi.com/product/add.htm',Accept3);
	proxies = {'http':'http://117.158.1.210:9999','http':'http://60.174.237.43:9999','http':'http://221.237.154.57:9999','http':'http://219.150.242.54:9999','http':'http://183.62.71.242:3128'}
	##构造发送post数据的表单
	data = {'shopIds': '353999,354000','parentSku': 'ZYH-YDEJ-000204',
		'name':'Universal Wireless Bluetooth Stereo Earbuds Sport Earphone Handfree for All Phone Headsets Headphones',
	    'description': '100% brand new and high quality Fully compatible with most models of cellphone and pad, available at any time High capacity battery lengthen working time',
'tags': 'unisex ear phone,sport headset,bluetooth earphones,earphones head phones,wireless earphone,earbuds ear phone,Earphone',
'mainImage': 'wxalbum/141804/20170911065614/4ceb7be99ac5a9b78b2b0b0cb0daa17d.jpg',
'msrp': '20',
'shipping': '2',
'price': '6',
'shippingTime': '10-15',
'skuStr': 'ZYH-YDEJ-0001-Pack of 100-white assorted&-&ZYH-YDEJ-0001-Pack of 100-sacramento state green'
};
	res = requests.post(url,headers=headers,data=json.dumps(data)).text.encode('utf-8')
	print res;
	
#####通过使用XPath来获取checkbox中的name =ShopIdBox 中的value值 组成一个数组来实现 
def get_shopIdList():
	shopIdList = ['353999','354000'];
	print shopIdList;

def main():
	data = {'account':username,'password':password,'remeber':'remeber'};
	#get_content(dianxiaomi_login_url,data)	
	get_cookie_save_file(dianxiaomi_add_product);
	
	conn = DianxiaomiData.initDB();
# 	appdataList = DianxiaomiData.showAllData(conn);
# 	hashItems = DianxiaomiData.get_fileId_And_SkufromDB(appdataList);
# 	#########通过循环遍历取出其中的imagePath 发送到服务器 
# 	for itemdata in appdataList:
# 		for key,value in hashItems.items():
# 			if(key == itemdata[5]):
# 				fileId = get_sign_fileId_fromserver(dianxiaomi_upload_pic_url,hashItems.get(key));
# 				print 'image fileId--------->',fileId;
# 				#######获取到fileId之后 可以update更新数据 
# 				conn.cursor().execute('update shopdata set [Main Image URL] =(?) where [Parent UniqueId]=(?)',(fileId,key));
# 				conn.commit();
# 				print 'update imagePath to imageFiled success '
				
	##将fileId从数据库更新掉 
	post_data_todianxiaomi(dianxiaomi_save_product);
	#print updateLocalDataToServer()
	#print updateLocalDataToServer();
	
############ 将所有的数据上传到Server ###############
def updateLocalDataToServer():
	print '-------update local data start----------'
	data = {'shopIds': '353999,354000','parentSku': 'ZYH-YDEJ-000182',
		'name':'Universal Wireless Bluetooth Stereo Earbuds Sport Earphone Handfree for All Phone Headsets Headphones',
	    'description': '100% brand new and high quality Fully compatible with most models of cellphone and pad, available at any time High capacity battery lengthen working time',
'tags': 'unisex ear phone,sport headset,bluetooth earphones,earphones head phones,wireless earphone,earbuds ear phone,Earphone',
'mainImage': 'wxalbum/141804/20170911065614/4ceb7be99ac5a9b78b2b0b0cb0daa17d.jpg',
'msrp': '20',
'shipping': '2',
'price': '6',
'inventory': '10000',
'shippingTime': '10-15',
'skuStr': 'ZYH-YDEJ-0001-Pack of 100-white assorted&-&ZYH-YDEJ-0001-Pack of 100-sacramento state green'
}
	
	headers = {'User-Agent': user_agent, 'Cookie':cookies, 'Host':host, 'Origin':origin, 'Referer':referer, 'Accept':Accept3,'Content-Type':ContentType}
	proxies = {'http':'http://117.158.1.210:9999','http':'http://60.174.237.43:9999','http':'http://221.237.154.57:9999','http':'http://219.150.242.54:9999','http':'http://183.62.71.242:3128'}
	res = requests.post(dianxiaomi_save_product,headers = headers,data = data)
	return res.text
	
	print '-------update local data end------------'

if __name__ == '__main__':
    main()
