# 概要

- wiki删除
- wiki编辑
- markdown编辑器
    - 添加、编辑
    - 预览
- 上传图片

# 详细

1. ### wiki删除

2. ### Wiki编辑

3. ### 应用markdown编辑器插件

    - 富文本编辑器，ckeditor

    - markdown编辑器，mdeditor

    - 项目中应用markdown编辑器

        - 添加和编辑页面中的textarea输入框 -> 转换为markdown编辑器

          ```
          - 应用css
          <link rel="stylesheet" href="{% static 'plugin/editor-md/css/editormd.min.css' %}">
          - 应用js
          <script src="{% static 'plugin/editor-md/editormd.min.js' %}"></script>
          ```

          官网下载插件，https://github.com/pandao/editor.md，直接download ZIP

      解压以后放到项目的静态文件夹中即可。

        ```
        1. textarea矿通过div包裹以便以后查找并转化成编辑器
        	<div id="editor">
        		{{ field }}
        	</div>
        2. 初始化编辑器
                function initEditorMd() {
                    // 第一个参数就是需要应用editor的标签id
                    editormd('editor', {
                        placeholder: "请输入内容",
                        height: 500,
                        path: "{% static 'plugin/editor-md/lib/' %}",
                    })
                }
        ```
        
        
    

