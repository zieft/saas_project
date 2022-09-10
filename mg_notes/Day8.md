# 概要

- wiki表结构
- 快速开发
- 应用markdown组件
- 基于腾讯COS/ AWS S3上传

# 详细

#### 1 表结构设计

| id   | 标题 | 内容 | 项目id | 父id   | 深度 |
| ---- | ---- | ---- | ------ | ------ | ---- |
| 1    |      |      |        | 自关联 |      |
| 2    |      |      |        |        |      |
| 3    |      |      |        |        |      |

#### 2 快速开发

2.1 首页展示

- 左边目录，右边文档库，上面还有一栏放新建按钮

- 多级目录：

  ```
  模板渲染：
  	- 数据库中获取的数据要有层级的划分
  		model.Wiki.object.filter(project_id=2)
  		将数据构造
  		[
  			{
  				id:1
  				title:'第一篇文章'
  				children: [
  					{'id':xx, "title": xx}
  				]
  			}
  		]
  	- 页面显示，循环显示（不知道有多少层）
  		递归
  缺点：
  	- 写代码费劲
  	- 效率低
  ```

  ```
  后端 + 前端完成ajax+ID选择器
  	- 打开页面之后：立刻发送ajax请求获取所有的文档标题信息。
  	- 后台：获取所有的文章信息，直接返回给前端
  		models.Wiki.object.filter(project_id=2).values_list("id", 'title', 'parent_id')
  		
  		[
  			{'id':1, 'title':'第一篇文章', parent_id: None},
  			{'id':2, 'title':'第二篇文章', parent_id: None},
  			{'id':3, 'title':'第三篇文章', parent_id: None},
  			{'id':4, 'title':'第三篇文章的子级', parent_id: 3},
  			{'id':5, 'title':'第一篇文章的子级', parent_id: 1},
  		]
  	- ajax的回调函数success中获取到res.data，并循环
      	$.each(res.data, function(index, item){
      		if(item.parent_id){
      		
      		}else{
      		
      		}
      	})
      	
     	- 循环结果示例：
     		<ul>
     			<li id='1'>第一篇文章</li>
     				<ul>
     					<li id='5'>第一篇文章的子级</li>
     				</ul>
     			<li id='2'>第二篇文章</li>
     			<li id='3'>第三篇文章</li>
     			   	<ul>
     					<li id='4'>第三篇文章的子级</li>
     				</ul>
     		</ul>
  ```

  ![](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20220909193212109.png)

![image-20220909212441711](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20220909212441711.png)

2.2 添加文章，左边目录不变，右边变成编辑器

- 功能实现，但是有bug：父级文章中展示了包括其他项目的父文章,已修复

2.3 预览文章（编辑，删除，新建按钮）

2.4 修改文章

2.5 删除文章