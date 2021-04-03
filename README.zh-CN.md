## API 说明


##### 身份验证

###### 登录
端点: auth/token/

请求示范
```text
Body:
"username": "<用户名>"
"password": "<密码>"
```

返回示范
```text
{
"refresh":"<更新令牌>",
"access":"<访问令牌>",
"is_staff":false,
"first_name":"<名>",
"last_name":"<姓>",
"user_id":"<用户ID>"
}
```
###### 更新令牌
请求示范
```text
Body:
"refresh": "<更新令牌>"
```
返回示范
```text
{"access":"<请求令牌>"}
```

##### 资源API

###### 用户
端点: /api/user/

字段
| 字段              | 创建             | 更新              |
|------------------|------------------|------------------|
| user_id          | 不可更改          | 不可更改           |
| profile_pic      | 非必填            | 可选              |
| username         | 必填              | 不可更改          |
| password         | 必填              | 可选              |
| email            | 必填              | 可选              |
| first_name       | 非必填            | 非必填            |
| last_name        | 非必填            | 非必填            |
| is_staff         | 管理员可填        | 管理员可填         |
| is_superuser     | 管理员可填        | 管理员可填         |
| is_active        | 管理员可填        | 管理员可填         |
| date_joined      | 不可更改          | 不可更改          |
| groups           | 管理员可填        | 管理员可填         |
| user_permissions | 不可用            | 不可用            |


* 创建用户
    * 端点: /api/user/
    * 请求方式: POST
* 列举用户
    * 端点: /api/user/
    * 请求方式: GET
* 检索用户
    * 端点: /api/user/<用户ID>
    * 请求方式: GET
* 更新用户
    * 端点: /api/user/<user ID>
    * 请求方式: PUT
* 删除用户
    * 端点: /api/user/<user ID>
    * 请求方式: DELETE


###### 用户组别
端点: /api/group/

字段
| 字段              | 创建             | 更新              |        |
|------------------|------------------|------------------|--------|
| id               | NO CHANGE        | NO CHANGE        |        |
| name             | 管理员必填        | 管理员必填         | 唯一    |



* 创建用户组别
    * 端点: /api/group/
    * 请求方式: POST
* 列举用户组别
    * 端点: /api/group/
    * 请求方式: GET
* 检索用户组别
    * 端点: /api/group/<组别名>
    * 请求方式: GET
* 更新用户组别
    * 端点: /api/group/<组别名>
    * 请求方式: PUT
* 删除用户组别
    * 端点: /api/group/<组别名>
    * 请求方式: DELETE


###### 文章
Endpoint: /api/post/

字段
| 字段                 | 创建                 | 更新    |
|----------------------|---------------------|-----------|
| id                   | 不可更改             | 不可更改 |
| title                | 必填                 | 必填  |
| description          | 非必填               | 非必填     |
| body                 | 非必填               | 非必填     |
| video                | 非必填               | 非必填     |
| audio                | 非必填               | 非必填     |
| view                 | 不可更改             | 不可更改   |
| is_public            | 非必填  自动否定      | 非必填     |
| like                 | 不可更改             | 不可更改   |
| createdTimestamp     | 不可更改             | 不可更改   |
| lastUpdatedTimestamp | 不可更改             | 不可更改   |
| owner                | 不可更改             | 不可更改   |
| category             | 非必填               | 非必填     |

* 创建文章
    * 端点: /api/post/
    * 请求方式: POST
* 列举文章
    * 端点: /api/post/
    * 请求方式: GET
* 检索文章
    * 端点: /api/post/<id>
    * 请求方式: GET
* 更新文章
    * 端点: /api/post/<id>
    * 请求方式: PUT
* 删除文章
    * 端点: /api/post/<id>
    * 请求方式: DELETE
* 可选参数
    * author=<用户ID> - 包含
    * title=<标题> - 包含
    * category=<分类名> - 完全一致
    * order_by=<任意字段>
  
  
###### 分类
端点: /api/category/

字段
| 字段              | 创建             | 更新              |        |
|------------------|------------------|------------------|--------|
| name             | 管理员必填        | 管理员必填         | 唯一   |
| created-by       | 不可更改          | 不可更改           |        |



* 创建分类
    * 端点: /api/category/
    * 请求方式: POST
* 列举分类
    * 端点: /api/category/
    * 请求方式: GET
* 检索分类
    * 端点: /api/category/<name>
    * 请求方式: GET
* 更新分类
    * 端点: /api/category/<name>
    * 请求方式: PUT
* 删除分类
    * 端点: /api/category/<name>
    * 请求方式: DELETE
* 可选参数
    * parent=<类别名> - 获取所有子类别
    * parent=root - 获取所有根类别
  