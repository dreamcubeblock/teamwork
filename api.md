# 接口文档
http://47.113.186.74/
## 1.注册系统
### 请求信息
    POST  /api/reg  HTTP/1.1
    Content-Type:   application/x-www-form-urlencoded
### 请求参数
http 请求消息 body 中 参数以 格式 x-www-form-urlencoded 存储  
需要携带如下参数 
 
- username  
用户名
- password  
密码
- plan  
计划每日学习的单词数量

### 响应信息
	HTTP/1.1 200 OK
	Content-Type: application/json
### 响应内容
http 响应消息 body 中， 数据以json格式存储  
如果登录成功，返回如下  

    {   
    "ret": 0
    }

如果注册失败，返回失败的原因，示例如下  

    {
    "ret": 1,
    "msg":  "用户名或者密码错误"
    }
  
ret 不为 0 表示注册失败，msg字段描述注册失败的原因
    
## 1.1修改计划（每日背多少单词）
### 请求信息
    POST  /api/change_plan  HTTP/1.1
    Content-Type:   application/x-www-form-urlencoded
### 请求参数
http 请求消息 body 中 参数以 格式 x-www-form-urlencoded 存储  
需要携带如下参数 
 
- username 
用户名
- plan
设定的每日计划量

### 响应信息
	HTTP/1.1 200 OK
	Content-Type: application/json
### 响应内容
http 响应消息 body 中， 数据以json格式存储  
如果设置成功，返回如下  

    {   
    "ret": 0
    }

如果设置失败，返回失败的原因

    {
    "ret": 1,
    "msg":  ""
    }
  
ret 不为 0 表示设置失败，msg字段描述注册失败的原因

## 2.登录系统
### 请求信息
    POST  /api/login  HTTP/1.1
    Content-Type:   application/x-www-form-urlencoded
### 请求参数
http 请求消息 body 中 参数以 格式 x-www-form-urlencoded 存储  
需要携带如下参数 
 
- username  
用户名
- password  
密码

### 响应信息
	HTTP/1.1 200 OK
	Content-Type: application/json
### 响应内容
http 响应消息 body 中， 数据以json格式存储  
如果登录成功，返回用户id  

    {   
    "ret": 0,
	"username":
    }
- userid 用户id
如果注册失败，返回失败的原因，示例如下  

    {
    "ret": 1,
    "msg":  "用户名或者密码错误"
    }
  
ret 不为 0 表示注册失败，msg字段描述注册失败的原因

## 3.出题
### 请求信息
    POST  /api/get_qu  HTTP/1.1
    Content-Type:   application/x-www-form-urlencoded
### 请求参数
http 请求消息 body 中 参数以 格式 x-www-form-urlencoded 存储  
需要携带如下参数 
 
- username  
用户名

### 响应信息
	HTTP/1.1 200 OK
	Content-Type: application/json
### 响应内容
http 响应消息 body 中， 数据以json格式存储  
如果请求成功，返回示例如下  

    {   
	    "ret": 0,
		"learn_num":50,
		"review_num":50,
		"word_id":2,
		"EN_word":"abandon",
		"CN_word":"vt.丢弃，放弃，抛弃",
		"wrong_CN_word":{
							1:"书本"
							2:"电子计算机"
							3:"学习"
						}
    }
- learn_num 用户今日还需学习的单词数量
- review_num 用户今日还需复习的单词数量
- word_id 英语单词id
- EN_word 英语单词
- CN_word 单词中文释义(错误的中文释义以作选择题用)
- wrong_CN_word 干扰选项(三个错误的中文释义以作选择题用)

如果请求失败，返回失败的原因  
示例1：
  
    {
    "ret": 1,
    "msg": "今日学习及复习已完毕"
    }
示例2：  

    {
    "ret": 1,
    "msg": ""
    }
ret 为 1 表示今日学习完毕  
ret 为 2 表示系统出错，"msg"返回出错信息

## 4.完成每日学习
### 请求信息
    POST  /api/done  HTTP/1.1
    Content-Type:   application/x-www-form-urlencoded
### 请求参数
http 请求消息 body 中 参数以 格式 x-www-form-urlencoded 存储  
需要携带如下参数 
 
- username  
用户名

### 响应信息
	HTTP/1.1 200 OK
	Content-Type: application/json
### 响应内容
http 响应消息 body 中， 数据以json格式存储  
如果登录成功，返回如下  

    {   
    "ret": 0
    }

如果注册失败，返回失败的原因，示例如下  

    {
    "ret": 1,
    "msg":  "用户名或者密码错误"
    }
  
ret 不为 0 表示注册失败，msg字段描述注册失败的原因

## 5.额外出题
### 请求信息
    POST  /api/more_qu  HTTP/1.1
    Content-Type:   application/x-www-form-urlencoded
### 请求参数
http 请求消息 body 中 参数以 格式 x-www-form-urlencoded 存储  
需要携带如下参数 
 
- username  
用户名
- qnum
额外出题数目

### 响应信息
	HTTP/1.1 200 OK
	Content-Type: application/json
### 响应内容
http 响应消息 body 中， 数据以json格式存储  
如果请求成功，返回示例如下  

    {   
	    "ret": 0,
		"learn_num":50,
		"review_num":50,
		"word_id":2,
		"EN_word":"abandon",
		"CN_word":"vt.丢弃，放弃，抛弃",
		"wrong_CN_word":{
							1:"书本"
							2:"电子计算机"
							3:"学习"
						}
    }
- learn_num 用户今日还需学习的单词数量
- review_num 用户今日还需复习的单词数量
- word_id 英语单词id
- EN_word 英语单词
- CN_word 单词中文释义(错误的中文释义以作选择题用)
- wrong_CN_word 干扰选项(三个错误的中文释义以作选择题用)

如果请求失败，返回失败的原因  
示例1：
  
    {
    "ret": 1,
    "msg": "今日学习及复习已完毕"
    }
示例2：  

    {
    "ret": 1,
    "msg": ""
    }
ret 为 1 表示今日学习完毕  
ret 为 2 表示系统出错，"msg"返回出错信息

## 英语发音
### 请求信息
	GET
	Request URL: https://dict.youdao.com/dictvoice?
	Content-Type: audio/mpeg
### 请求参数
- audio  
英语单词
- type  
1:英音  2：美音
### 示例
	https://dict.youdao.com/dictvoice?audio=word&type=2
	单词word的美式发音
## 单词搜索
### 请求信息
	GET
	Request URL:http://fanyi.youdao.com/openapi.do?type=data&doctype=jsonp&version=1.1&relatedUrl=http%3A%2F%2Ffanyi.youdao.com%2Fopenapi%3Fpath%3Dweb-mode%26mode%3Ddicter&keyfrom=test&key=null&callback=YoudaoDicter.Instance.update&translate=on
### 请求参数
- q  
英语或中文单词
### 响应信息
	Server:YDWS
	Date:
	Content-Type:application/javascript;charset=utf-8
	Content-Length:
	Connection:keep-alive
### 响应内容(示例）
	YoudaoDicter.Instance.update({
	    "translation": [
	        "词"
	    ],
	    "basic": {
	        "us-phonetic": "wɜːrd",
	        "phonetic": "wɜːd",
	        "uk-phonetic": "wɜːd",
	        "explains": [
	            "n. 字，词，单词；（某人说的）话，言语（words）；简短的交谈，谈话；命令，指示；消息，信息；诺言，承诺；口角，吵架（words）；（警告、建议、赞扬的）话，话语；歌词（words）；一个字（所说或所写的最小量）（a word）；（不同于行动的）言，言语；字（尤指16或32个字节的计算机数据基本单位）；《圣经》，福音（the Word）",
	            "v. 措辞，用词",
	            "int. <美> （表示接受或同意别人刚说的话）就是，说得对",
	            "【名】 （Word）（英）沃德（人名）"
	        ]
	    },
	    "query": "word",
	    "errorCode": 0,
	    "web": [
	        {
	            "value": [
	                "字",
	                "单词",
	                "及答案",
	                "词"
	            ],
	            "key": "Word"
	        },
	        {
	            "value": [
	                "总之",
	                "总而言之",
	                "简言之",
	                "一句话"
	            ],
	            "key": "in a word"
	        },
	        {
	            "value": [
	                "女欢女爱",
	                "第五季"
	            ],
	            "key": "The L Word"
	        }
	    ]
	});