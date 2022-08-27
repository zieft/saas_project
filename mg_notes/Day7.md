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

