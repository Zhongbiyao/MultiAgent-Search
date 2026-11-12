
---

# 🤖 基于多 Agent 协作的行业与公司研究助手

> **项目简介**：一个基于 LangChain 框架构建的智能投研助手。通过编排“外部检索、财务数据库、私有知识库”三大专业子 Agent，打破信息孤岛，实现从“一句话指令”到“多源信息交叉验证”再到“全自动输出行研报告（Markdown/PDF）”的完整闭环。

## 📍 1. 项目背景与痛点

在行业研究与公司初筛场景中，分析师通常面临三个痛点：
1. **信息搜集耗时**：需要在巨潮资讯、财经媒体中大海捞针，耗费数小时。
2. **数据整合繁琐**：新闻资讯（非结构化）与财报数据（结构化）分离，需要人工比对。
3. **输出格式不统一**：难以严格遵循机构内部的“行研 SOP”输出标准报告。

本项目旨在打造一个**数字实习生**，将繁琐的信息搬运、SQL 查询与框架套用自动化，让分析师将精力集中在最终的价值判断上。

## 🎥 2. 演示与效果预览

> *(这里留给你插入视频和截图)*
> *   **📺 视频演示**：*(建议用 ScreenToGif 或 B站录制一段 2 分钟的视频，展示：输入指令 ➔ 观察左侧 Agent 思考与工具调用日志 ➔ 右侧文件面板刷出并下载报告)*
[![行业研究助手演示demo](这里填你的封面图片链接)](https://www.bilibili.com/video/BV1VeWX6PEWf/?vd_source=9f68ea1d0f97b2bcf7ee99aca55df09e)

> *   **📸 界面截图**：
>     *(插入图 1：左侧展示 Agent 按顺序调用了 `internet_search`、`execute_sql_query` 和 `create_ask_delete`)*
>     *(插入图 2：右侧文件面板生成了漂亮的 PDF 报告)*

## ✨ 3. 核心功能

*   🌐 **联网情报收集**：接入 Tavily Search，基于 5 个不同维度（公司/行业/竞品/资本/风险）进行多轮搜索，并自动标注信息来源可信度。
*   🗄️ **精准财务查询 (Text-to-SQL)**：封装 MySQL 查询工具，Agent 可自主探查表结构（`list_sql_tables`）并执行 SQL，获取精确到小数点的营收与利润数据。
*   📚 **私有框架对齐**：接入 RAGFlow SDK，Agent 能够动态创建会话查询企业内部行研 SOP，并严格按 SOP 结构组织报告。
*   ⚖️ **冲突事实交叉验证**：主 Agent 具备交叉比对纪律。若新闻检索（定性）与财报数据（定量）存在冲突（如“新闻唱多但净利下滑”），系统会并列呈现双方来源。
*   📄 **全流程文档生成**：支持 Markdown 生成，并调用底层 Word 引擎自动转换为标准排版的 PDF。

## 🏗️ 4. 系统架构设计

*(💡 强烈建议你在 Draw.io 画一个简单的架构图贴在这里)*

系统采用 **“1 个主控 Agent + 3 个异构子 Agent + 1 套文档生成工具链”** 的架构：

*   **主 Agent (Orchestrator)**：负责需求拆解、任务分发、冲突信息校验，并调度文件生成工具。
*   **子 Agent 1 - 公开信息检索**：使用 `tavily_tool` 获取外部市场情报。
*   **子 Agent 2 - 财务数据助手**：使用 `db_tools` 直连 MySQL 执行 SQL。
*   **子 Agent 3 - 研究框架助手**：使用 `ragflow_tools` 调用 RAGFlow 知识库。
*   **工具链**：`markdown_tools` 与 `pdf_tools` 负责文件的本地落盘与格式转换。

## 🛠️ 5. 技术栈

*   **大模型**：例如 DeepSeek-V3 / GPT-4o
*   **Agent 编排**：LangChain (Tool Calling, Prompt Engineering)
*   **数据交互**：MySQL (PyMySQL)、Tavily Search API
*   **知识库**：RAGFlow SDK
*   **Web 交互**：FastAPI + WebSocket（提供流式日志与实时文件状态刷新）
*   **前端**：原生 HTML/JS/CSS（支持暗黑模式与 Markdown 实时预览）

## 🧠 6. 核心设计取舍与难点攻克


1.  **难点：大模型“偷懒”只输出文字，不调用工具生成文件。**
    *   **解法**：在 Prompt 中设定【强制指令】，将“文件生成”与“文字反馈”的触发条件严格隔离。同时，在 `markdown_tools` 中重写了底层的路径清洗逻辑（`resolve_path`），强制文件写入 `session_dir`，避免大模型生成绝对路径导致的安全风险。
2.  **难点：多源信息存在幻觉或冲突。**
    *   **解法**：一是在子 Agent 层面引入“反幻觉纪律”（如查不到必须明说，不许瞎猜）；二是在主 Agent 层面设定了事实核查机制，强制对齐多源信息。
3.  **难点：LLM 不按企业内部标准生成报告。**
    *   **解法**：引入 RAG Agent 作为“框架指导者”，在生成报告前，先向 RAGFlow 询问 SOP 结构。Prompt 强制要求“必须严格按照研究框架助手提供的结构组织正文”。
4.  **难点：网络请求不稳定导致 Agent 中断。**
    *   **解法**：在 `tavily_tool` 外部封装了 `retry_with_backoff`（指数退避重试），保证网络抖动时的鲁棒性。

## 🚀 7. 快速开始

1.  **环境准备**：Python 3.10+，确保本地或云端有可用的 MySQL 服务。
2.  **安装依赖**：
    ```bash
    pip install -r requirements.txt
    ```
3.  **配置环境变量**：复制 `.env.example` 并重命名为 `.env`，填入相关密钥：
    ```env
    TAVILY_API_KEY=你的Tavily密钥
    MYSQL_HOST=localhost
    MYSQL_USER=root
    MYSQL_PASSWORD=你的数据库密码
    MYSQL_DATABASE=finance_db
    RAGFLOW_API_KEY=你的RAGFlow密钥
    RAGFLOW_BASE_URL=你的RAGFlow地址
    ```
4.  **初始化财务数据**：运行 `python init_mysql.py` 自动建表并导入测试财务数据。
5.  **启动服务**：运行主程序（例如 `python main.py`），在浏览器访问 `http://localhost:8000`。

## 🔮 8. 未来迭代方向

*   **引入 Critic Agent (独立评审员)**：将事实核查从主 Agent 剥离，使用独立的模型对子 Agent 返回的数据进行“打分”，低于阈值自动回退重试。
*   **增加记忆机制 (Memory)**：支持多轮对话上下文，例如用户接着问“把刚才报告里的风险部分展开说说”。
*   **支持 MCP 协议**：将现有工具重构为 MCP Server，实现与更多本地开发环境（如 Cursor/Claude Desktop）的无缝集成。

---
