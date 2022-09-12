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


4. ### 使用markdown进行预览

   ``` 
   
   1. 内容区域使用div标签包裹，并设置id
   <div id="previewMarkdown">
   	<textarea name="" id="" cols="30" rows="10">
   		{{ wiki_object.content }}
   	</textarea>
   </div>
   
   2.引入css，js
   <link rel="stylesheet" href="{% static 'plugin/editor-md/css/editormd.preview.min.css' %}">
   
   <script src="{% static 'plugin/editor-md/editormd.min.js' %}"></script>
   <script src="{% static 'plugin/editor-md/lib/marked.min.js' %}"></script>
   <script src="{% static 'plugin/editor-md/lib/prettify.min.js' %}"></script>
   <script src="{% static 'plugin/editor-md/lib/raphael.min.js' %}"></script>
   <script src="{% static 'plugin/editor-md/lib/underscore.min.js' %}"></script>
   <script src="{% static 'plugin/editor-md/lib/sequence-diagram.min.js' %}"></script>
   <script src="{% static 'plugin/editor-md/lib/flowchart.min.js' %}"></script>
   <script src="{% static 'plugin/editor-md/lib/jquery.flowchart.min.js' %}"></script>
   
   3.初始化
   function initPreviewMarkdown () {
   	editormd.markdownToHTML('previewMarkdown',{
   		htmlDebode: 'style,script,iframe',  // 防止script攻击等
   });
   }
   ```


5. ### 从本地上传图片，暂未实现
