# Mini-Blog

一个用于微服务架构演示的mini blog系统，前端界面提供List样式的博客展示，后台架构主要为四部分

## 环境配置
    运行:python ./setting.py
## SSOService 提供登录注册的接口
    运行方式:python ./sso.py 4444端口
### 1. 接口概述

接口名称 | URL | Http Method
------ | ---- | ----
[登录] | /sso/login | POST
[注册] | /sso/regist | POST
[注销] | /sso/logout | GET
[获取用户信息] | /sso/getInfo | GET

### 2. 接口详情
- 注册
    - 路径:/sso/regist
    - 请求参数：
        
        form-data
        {
            'username':'用户名'
            'passwd':'密码'
        }
    
    - 返回参数：

        json
        {
            'code':0,
            'msg':''
        }
        
    - 错误说明
        
        错误码 | 说明
        ---- | -----
        0   | 成功
        401 | 用户已经注册
        500 | 服务器或者数据库错误

- 登录
    - 路径:/sso/login
    - 请求参数：
        
        form-data
        {
            'username':'用户名'
            'passwd':'密码'
        }
    
    - 返回参数：

        json
        {
            'code':0,
            'msg':''
        }
    - 错误说明
        
        错误码 | 说明
        ---- | -----
        0   | 成功
        404 | 密码错误
        500 | 服务器或者数据库错误

- 注销
    - 路径:/sso/logout
    - 请求参数：null   
    - 返回参数：

        json
        {
            'code':0,
            'msg':''
        }
    - 错误说明
        
        错误码 | 说明
        ---- | -----
        0   | 成功
        403 | 用户还未登录

- 获取用户信息
    - 路径:/sso/getInfo
    - 请求参数：null   
    - 返回参数：

        json
        {
            'code':0,
            'msg':'',
            'username':'username'
        }
    - 错误说明
        
        错误码 | 说明
        ---- | -----
        0   | 成功
        403 | 用户还未登录


## BlogService 提供支持Blog条目的增删查改的接口
    运行方式:python ./blog.py  5555端口
### 1. 接口概述

接口名称 | URL | Http Method
------ | ---- | ----
[查询所有Blog条目](#blogTotal_search) | /blog/total | GET
[查询个人Blog条目](#blog_search) | /blog/user | GET
[修改某个Blog详情](#blog_modify) | /blog/modify | POST
[删除某个Blog](#blog_delete) | /blog/delete | POST
[增加一条Blog](#blog_add) | /blog/add | POST

### 2. 接口详情
- 查询所有Blog条目
  - 路径：/blog/total
  - 请求参数：NULL
  - 返回值: json

           {
				"code": 0,
				"msg": null,
				data: {
				    "datacount": 10, #博客条数
                    "data": [
					{
						"blogid": 1,  # 主键
                        "author": "作者",
						"title": "标题",
                        "content": "博客正文",
                        "comment_num": 100, #此条blog的评论数
                        "date": 时间
					}
                    , ...]
				}
			}
    - 错误说明:

        错误码 | 说明
        ---- | -----
        0 | 成功
        400 | 请求连接错误
        500 | 服务器或者数据库错误

- 查询个人Blog条目
  - 路径：/blog/user
  - 请求参数：NULL
  - 返回值: json

           {
				"code": 0,
				"msg": null,
				data: {
				    "datacount": 10, #博客条数
                    "data": [
					{
						"blogid": 1,  # 主键
                        "author": "作者",
						"title": "标题",
                        "content": "博客正文",
                        "comment_num": 100, #此条blog的评论数
                        "date": 时间
					}
                    , ...]
				}
			}
    - 错误说明:

        错误码 | 说明
        ---- | -----
        0 | 成功
        400 | 请求连接错误
        500 | 服务器或者数据库错误

- 修改某条blog情况
  - 路径：/blog/modify
  - 请求参数：
            
            form-data
            {
                "blogid": 1,  # 主键
				"title": "标题",
                "content": "博客正文",
            }
  - 返回值: 

            json{
				"code": 0,
				"msg": null
			}
    - 错误说明:

        错误码 | 说明
        ---- | -----
        0 | 成功
        403 | 请求修改的blog不存在(id错误)
        400 | 请求连接错误
        500 | 服务器或者数据库错误

- 删除某条blog
  - 路径：/blog/delete
  - 请求参数：
            
            form-data
            {
                "blogid": 1,  # 主键
            }
  - 返回值: 

            json{
				"code": 0,
				"msg": null
			}
    - 错误说明:

        错误码 | 说明
        ---- | -----
        0 | 成功
        403 | 请求删除的blog不存在(id错误)
        400 | 请求连接错误
        500 | 服务器或者数据库错误

- 增加一条Blog条目
  - 路径：/blog/add
  - 请求参数：

            form-data
            {
                "title": "标题",
                "content": "博客正文",
            }

  - 返回值: json

           {
				"code": 0,
				"msg": null
		   }
    - 错误说明:

        错误码 | 说明
        ---- | -----
        0 | 成功
        400 | 请求连接错误
        500 | 服务器或者数据库错误
                        

## CommentService 提供每条Blog条目的简单评论的接口(主要是增加评论)
    运行方式:python ./comment.py  6666端口
接口名称 | URL | Http Method
------ | ---- | ----
查询某个blog的评论 | /comment/search | POST
增加一条评论 | /comment/add | POST

### 查询某条Blog的评论
- 路径: /comment/search
- 请求参数:

        form-data
        {
            "blogid":1
        } 

- 返回结果:

        json{
            "code": 0,
            "msg": null，
            "datacount": 10 #评论的总数目
            "data": [
                {
                    "blogid": 1,
                    "commentid": 2, #评论的主键
                    "author": "评论的用户",
                    "content": "评论的内容",
                    "date":日期
                
                }
                ,……
            ]
        }
- 错误说明:

    错误码 | 说明
    ---- | -----
    0 | 成功
    400 | 请求连接错误
    500 | 服务器或者数据库错误

### 增加一条评论
- 路径: /comment/add
- 请求参数:

        form-data
        {
            "blogid": 1 #对应的blogid
            "content": "内容",
        } 

- 返回结果:

        json
        {
            "code": 0,
            "msg": null
        }
- 错误说明:

    错误码 | 说明
    ---- | -----
    0 | 成功
    400 | 请求连接错误
    500 | 服务器或者数据库错误


## RankService 提供按照Blog评论数排序的排行榜的接口
    运行方式:python ./rank.py  7777端口
接口名称 | URL | Http Method
------ | ---- | ----
查询按照评论数排序 | /rank | GET

### 查询按照评论数排序
 - 路径: /rank/
 - 请求参数:NULL
 - 返回结果:
 
        json{
            "code": 0,
            "msg": null，
            "datacount": 10 #blog的总数目
            "data": [
                {
                    "blogid": 1,
                    "author": "评论的用户",
                    "title": "博客标题"
                }
                ,……
            ]
        }
 - 错误说明:

    错误码 | 说明
     ---- | -----
    0 | 成功
    400 | 请求连接错误
    500 | 服务器或者数据库错误

