## 问题管理

### 设计表结构

功能+原型图

![image-20230328112936863](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20230328112936863.png)

![image-20230328112922531](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20230328112922531.png)

![](C:\Users\zieft\AppData\Roaming\Typora\typora-user-images\image-20230328105234204.png)

| ID   | 标题 | 内容 | 问题类型（外键） | 模块（外键） | 状态（下拉选择） | 优先级（下拉选择） | 指派给（FK） | 关注者（多对多） | 开始、结束时间 | 模式 | 父问题 |
| ---- | ---- | ---- | ---------------- | ------------ | ---------------- | ------------------ | ------------ | ---------------- | -------------- | ---- | ------ |
|      |      |      |                  |              |                  |                    |              |                  |                |      |        |
|      |      |      |                  |              |                  |                    |              |                  |                |      |        |
|      |      |      |                  |              |                  |                    |              |                  |                |      |        |

| ID   | 问题类型 |
| ---- | -------- |
| 1    | Bug      |
| 2    | 功能     |
| 3    | 任务     |

| ID   | 模块   |
| ---- | ------ |
| 1    | 第一期 |
| 2    | 第二期 |
| 3    | 第三期 |

## 新建问题

#### 模态对话框

- 显示对话框
- 显示供用户填写的biao'da

前端插件：

- bootstrap-datepicker

```
css
js
js找到标签处理
```

- bootstrap-select

```
css
js
ModelForm中添加属性
```

## 问题列表