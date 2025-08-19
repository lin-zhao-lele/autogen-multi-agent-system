## FEATURE:

- 使用AutoGen框架实现一个多智能体系统，能够根据用户输入的开发要求生成Python代码
- 实现代码质量检查功能，确保生成的代码符合PEP8规范和项目标准
- 实现代码优化和自动修复功能，提升代码质量和性能
- 构建一个基于网页的用户交互界面，让用户可以与智能体进行交互
- 智能体应包括：
  - 需求分析智能体：理解用户需求并制定开发计划
  - 代码生成智能体：根据需求生成Python代码
  - 代码审查智能体：检查代码质量并提出改进建议
  - 代码优化智能体：优化代码性能和可读性
  - 测试智能体：为生成的代码创建测试用例

## EXAMPLES:

- 参考项目中的`use-cases/pydantic-ai/examples/`目录结构来组织代码
- 参考`use-cases/mcp-server/examples/`中的TypeScript实现来理解智能体交互模式
- 查看AutoGen官方示例：https://github.com/microsoft/autogen/tree/main/python/samples

## DOCUMENTATION:

- AutoGen框架官方文档：https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html
- AutoGen GitHub仓库：https://github.com/microsoft/autogen
- FastAPI文档（用于构建Web界面）：https://fastapi.tiangolo.com/
- Pytest文档（用于测试）：https://docs.pytest.org/

## OTHER CONSIDERATIONS:

- 使用Python作为主要开发语言
- 遵循项目中CLAUDE.md定义的代码规范和结构
- 确保所有智能体能够正确处理错误和异常情况
- 实现日志记录功能，便于调试和监控
- 考虑使用虚拟环境管理项目依赖
- 注意API密钥和敏感信息的安全存储