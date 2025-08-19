# step1

```
项目需求： 需要用AutoGen框架实现一个能够根据用户输入的开发要求生成python代码，并且检查代码质量，再优化和修复代码的agents, agents在网页里面和用户进行交互。

参考资料 ：AutoGen框架文档 （https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html ）。
 
任务：使用context7查询context-engineering-intro 文档和相关参考资料 ，索引当前项目内已有的文件，以当前项目内的INITIAL.md和CLAUDE.md为模版，结合以上项目需求，生成新的针对本项目后续开发的INITIAL.md和CLAUDE.md（请使用中文）

```

# step2

```

/generate-prp INITIAL.md

```


# step3

```

/execute-prp PRPs/autogen-multi-agent-system.md 

```

# step4

```

python -m web.main

http://127.0.0.1:9000/static/index.html



分析INITIAL.md和CLAUDE.md以及 \PRPs\autogen-multi-agent-system.md 以便进行下一步的修改
```