# 概要

- 在页面上显示项目
- 星标项目
- 添加项目：颜色选择
- 项目切换 & 项目管理菜单处置
- wiki管理

# 详细

## 1. 展示项目

1.1 获取数据(GETqi)

``` 
1. 从数据库中获取两个部分数据
		我创建的所有项目：已星标、未星标
		我参与的所有项目：已星标、未星标
2. 循环两个列表，提取所有已星标的项目

得到三个列表：星标、创建、参与
```

1.2 处理样式

## 2. 星标项目

2.1 添加星标

```
我创建的项目：project的star设为True即可。
我参与的项目：projectuser的star设为True即可。
```

2.2 去除星标

```
判断项目是不是我创建的：
如果是
	我创建的项目：project的star设为False即可。
	我参与的项目：projectuser的star设为False即可。
```

## 3. 颜色选择

3.1 部分样式应用BootStrap

3.2 定制ModelForm的插件

```python
class ProjectModelForm(BootStrapForm, forms.ModelForm):
    
    class Meta:
        model = models.Model
        fields = '__all__'
        
        widgets = {
            'desc': forms.Textarea, 
            'color': ColorRadioSelect(attrs={'class': 'color-radio'})
        }
```

3.3 项目颜色选择器

## 4. 切换菜单

```
1. 从数据库获取
	我创建的
	我参与的
2. 循环显示
3. 当前页面需要显示 / 其他页面也需要显示[使用inclusion_tag实现]
```

## 5.项目管理

进入项目后，导航条显示更多功能按钮

进入项目后的路由规划

```
/manage/项目id/功能/zi'gong'negn

/manage/项目id/dashboard
/manage/项目id/issues
/manage/项目id/statistics
/manage/项目id/file
/manage/项目id/wiki
/manage/项目id/setting
```

##### 5.1 进入项目在导航条展示功能菜单

条件：进入项目后

5.1.1 如何判定是否进入项目？

```
1.判断url是否是manage开头的
2.选择的项目（project_id）是不是我创建的or我参与的
```

解决办法：【使用中间件】

##### 5.1.2 显示菜单栏

给中间件中的request.tracer增加新成员变量project，验证是不是我的合法项目（我创建的or我参与的）并将通过的项目object保存在tracer中。在前端就可以通过判断
request.tracer.project 来判断改是否已经进入项目。

##### 5.1.3 默认选中菜单

利用inclusiontag，动态改变<li>标签的class属性。

# 总结

1. 项目实现思路
2. 星标、取消星标
3. inclusion_tag实现项目切换
4. 项目菜单
    1. 中间件 process_view
    2. inclusion_tag
    3. 菜单选中状态
    4. 路由分发
        1. include("some.url")
        2. include([some, url])
5. 颜色选择： 源码 + 扩展 【不求甚解】