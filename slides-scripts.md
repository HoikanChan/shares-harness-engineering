# Harness Engineering 演讲大纲 v3

> **结构**:理论 36% + 实践 64%(约 4:6)
> **理论主线**:Prompt → Context → Harness 三阶段演进,Context Engineering 深挖作为 Harness 的地基
---

# 第一段:理论(10 张)

## S1 — 封面 + 开场钩子

**视觉**:封面 slide,大标题"Harness Engineering——怎么驾驭一匹会自己跑的马"
// todo
改为用这案例
单智能体的天花板
当我们第一次把一个复杂需求丢给单个 Claude 实例时，结果往往令人失望。给它 20 分钟、花费 $9，它也许能生成一个"看起来像那么回事"的骨架。但仔细检查你会发现：不能运行，API 接口互相矛盾，安全漏洞随处可见。这不是模型能力的问题，而是认知架构的问题。

Anthropic 工程团队的研究指出了两个持久的失败模式：

上下文窗口的侵蚀：随着对话历史不断膨胀，模型对早期决策的记忆开始模糊。它在第 50 轮对话中做出的选择，可能与第 5 轮的架构决策完全矛盾。我们在实践中观察到，当一个 Generator Agent 的执行超过 40 轮工具调用时，代码风格的一致性会显著下降。

自我评估的失灵：模型天然倾向于对自己的输出给予正面评价。当你让同一个 Claude 实例先写代码再审查代码，它几乎总是说"代码质量良好"。这不是幻觉，而是一种更深层的认知偏差——它很难对自己刚刚做出的决策保持批判距离。

Harness 正是为了突破这两个瓶颈而存在。它不是一个 Prompt 技巧，而是一种系统架构

---

## S3 — 工程师的工作搬了三次家

**视觉**:三阶段演进图(时间轴 2022 → 2026)

**口播要点**(理论主线起点,慢一点讲)
- 要理解 Harness 为什么现在突然这么热,得先看这几年 AI 工程实践的演变。AI 工程师的工作,在三个阶段里搬了三次家

- **第一阶段:Prompt Engineering(2022-2024)**
  - 那时候模型很笨,但听话。工程师的工作是雕一条指令,找到那个"完美的 prompt"
  - 模型对措辞极其敏感,一个词的增删,输出质量天差地别
  - 每个人笔记本里都存着几百条精心调校的 prompt

- **第二阶段:Context Engineering(2025)**
  - 模型变强了,agent 能用工具了
  - Karpathy 的比喻:**LLM 是 CPU,context window 是 RAM,而你是负责载入正确信息的操作系统**
  - 工程师的工作从"怎么说"变成了**"给它看什么"**

- **第三阶段:Harness Engineering(2026)**
  - 模型现在可以自己跑了
  - 工程师的工作从"管信息"变成了**"搭笼子"**——让 AI 在里面安全地跑

- [停顿]**关键澄清**:这三个阶段不是替代关系,是包含关系。Harness 把前两代都吸收进来了。Prompt 和 Context 没有死,它们被升职了,变成更大系统里的子模块

- LangChain 的极简公式:**Agent = Model + Harness**

---

## S4 — Context Engineering 深挖之一:放什么 + 核心挑战

**视觉**:左边一个 Context Window 容器图,五类内容塞在里面 | 右边三个挑战的图标

**口播要点**
- 在进入 Harness 之前,先把 Context Engineering 讲透——**它是理解 Harness 的地基**

**Context window 里能放什么?**
- **指令**(Instructions):agent 怎么行事的规则,CLAUDE.md 里的内容
- **工具**(Tools):agent 能调用什么——bash、文件读写、浏览器、MCP server
- **记忆**(Memory):过去做过什么、学到了什么,文件或 git log
- **状态**(State):当前任务进行到哪一步
- **历史**(History):这个 session 里的对话记录

这五类东西,**都在抢同一个有限的 context window**。

**三个核心挑战**:
1. **窗口有限**——稀缺资源,全塞进去模型会一视同仁或完全迷失
2. **信息腐烂**——经典研究"Lost in the Middle":模型对开头和结尾敏感,中间容易忘
3. **跨会话记忆丢失**——最痛的。Agent 没有天生跨会话记忆,每次新 session 启动对上次一无所知,**像一个项目组全是轮班工程师**

// todo： 这段参考@hungyi-lee-harness-engineering 加入context分为存储里的，和对话中的

---

## S5 — Context Engineering 深挖之二:核心手段 + 天花板

**视觉**:上半 — 一份"好 AGENTS.md vs 坏 AGENTS.md"对比 | 下半 — 一个红色"天花板"图标 + 问题清单

**口播要点**

**核心原则**:**好的指令档应该像地图,不是六法全书**
- OpenAI blog 特别提醒:指令档不能写成六法全书,那会占掉模型大部分 context window
- 更好的做法:提供精简入口点,然后**"教"agent 根据当前任务按需检索更多上下文**
- Mitchell Hashimoto 的 Ghostty 项目 AGENTS.md:**每一行都对应一个历史失败案例**——不是大而全规范手册,是**避坑指南**,每条规则都有来历

**关键概念**:文档必须是**活的反馈循环,不是静态制品**

**但 Context Engineering 有一个致命盲点——它只管单一 agent 的视角**:
- 多个 agent 协作?Context Engineering 帮不了你
- Agent 完成工作后验证结果?帮不了你
- Agent 犯错时自动回滚?帮不了你

**更深的问题**:就算给了 agent 完美的 context,**你也无法阻止它在对的 context 里做出错的判断**

→ 这就是为什么我们需要从 Context Engineering 升级到 **Harness Engineering**

// todo： 这段参考@hungyi-lee-harness-engineering 加入压缩的问题，subagent的好处的

---

## S6 — Harness 登场:LLM 的操作系统

**视觉**:冯·诺依曼架构对位图(LLM=CPU,Context=RAM,文件系统=Disk,Tools=Drivers,Harness=OS)

**口播要点**
- Harness 这个词来自马具——缰绳、马鞍、嚼子那一整套
- **马有再强的力气,没有马具就只是一匹野马**
- 以前不需要马具是因为马跑不快;现在模型足够强了,能自己跑、自己做决定、自己用工具——**这就是问题的开始**

**更精准的比喻——我们重新发明了冯·诺依曼架构**:
- 原始 LLM = CPU
- Context window = RAM(快速但有限)
- 外部文件系统 = 磁盘存储
- 工具 = 设备驱动
- **Harness = 操作系统**

操作系统让 CPU 能安全、可靠、高效运行;Harness 让 LLM 能安全、可靠、高效完成任务

**为什么 2026 年 Harness 突然热起来**:
- 2 月 OpenAI 发《Harness Engineering: Leveraging Codex in an Agent-First World》
- 3 月 Anthropic 发《Harness Design》
- Martin Fowler 专文介绍
- **两家龙头一前一后,风向很明显**

---

## S7 — Harness 框架
// todo： 这段参考6. **[Part 06: 標準工作流程 (SOP)](./part_06_workflow.md)** (00:38:24 - 00:45:24)
   - 大廠實踐：規劃 (Plan) -> 生成 (Generate) -> 評估 (Evaluate)。
   - 解決「覆水難收」：使用 Evaluator 阻止模型在錯誤路徑上不斷生成（Autoregressive Mistake）。
   - **Ralph Loop**: 循環生成、獲取 Feedback 並修正。
   - 上下文焦慮：Claude Sonnet 的情緒化表現及其解決方案。
---

## S8 — Agent 四种翻车 + 核心飞轮

**视觉**:左四宫格(四种翻车) | 右一个闭环飞轮图

**口播要点**

**四种典型翻车**(Anthropic 工程师总结):
1. **One-shotting**:一个 session 想做完所有事 → context 耗尽 → 半成品
2. **过早宣布胜利**:看到部分进展就说做完了
3. **过早 mark done**:写完代码就标 done,没做端到端验证
4. **环境启动困难**:每次新 session 花大量 token 弄清怎么跑项目

加一句危险特性:**agent 极擅长模式复制**——代码库里有什么模式就忠实复制并放大,**包括坏模式和架构漂移**。不加约束的 agent 会以惊人速度积累技术债

**核心飞轮**:
```
Agent 犯错 → 人类归因 → 补 harness(文档/约束/验证) → 下次同类问题更少
```

Mitchell Hashimoto 的定义:
> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent will not make that mistake again in the future."

**每次翻车不是损失,是投资**——在 AGENTS.md 多写一条规则、eval 多加一个测试、权限多加一道门,都是让飞轮转得更稳

---

## S9 — 业界共识:瓶颈在基础设施

**视觉**:四组数据卡片

**口播要点**
- **OpenAI Codex 团队**:七人,零人工代码,一百万行——关键不是模型多强,是花了多少时间打磨 harness
- **LangChain 实验**:同模型换 harness,Grok Code Fast 1 从 6.7% → 68.3%,排名 30 → 5
- **Manus**:六个月同模型重写五次 harness,每次提升都**大于换模型**
- **五个独立团队同一结论**:
  > "The bottleneck is infrastructure, not intelligence."

理论核心一句话:
> **"瓶颈不在模型智能,在基础设施。"**

Harness 不是 prompt trick,不是调参——它是**工程纪律**,一套围绕 agent 设计约束机制、反馈回路、工作流控制的系统工程实践。

→ 那 Harness 落地时具体长什么样?下一张图给出框架。

---

## S10 ★ 7 阶段工作流框架 + 项目背景过渡(承上启下核心页)

**视觉**:**这是整场最重要的一张图**——7 阶段螺旋 + 反馈回路

```
        ┌──── Retrospective (6) ────┐
        │   沉淀:CLAUDE.md/skill/   │
        │   command/hook/plugin     │
        ↑                           ↓
   Code Review (5)            Bootstrap (0)
   PR 机器人/架构债扫描       环境/CLAUDE.md/MCP/settings
        ↑                           ↓
   Verify (4)                  Alignment (1)
   自动化 + LLM-Judge          Grill Me / AskUserQuestion
   (Writer/Reviewer 模式)
        ↑                           ↓
   Implement (3) ←──────────── Design (2)
   TDD / Ralph Loop /          OpenSpec / 纵向切片 /
   Subagents / 小步快跑        阶段化门禁
```

**口播要点**(这一页要慢、要重)
- 这是把 Harness Engineering 落地的完整工作流,**7 个阶段 + 1 个反馈回路**
- 上半场讲的三大支柱(认知/能力/流程)在这里都有对应位置——**Bootstrap 是认知,Verify 是流程,settings.json 是能力边界**
- 每个阶段都有明确产出、明确判断到位的信号
- **关键不是这 7 个阶段本身,是中间的反馈回路**——复盘的产出回流到 Bootstrap,让 CLAUDE.md 更全、skill 库更厚、judger 更严
- **这不是瀑布,是螺旋——harness 自己也在被 harness 优化**

**项目背景过渡**:
- 我们做的是 **OpenUI**:Generative UI 框架,LLM 流式生成 UI DSL → 实时渲染 React,比 JSON 方案 token 效率高 52%
- 项目的特殊性:**模型的输出本身就是产品**——harness 对我们不只是开发效率,是产品质量的直接保障
- 下面按这张图,一阶段一阶段讲我们怎么落地

[喝口水,让大家缓一下]

---

# 第二段:我们的 Harness 实践(17 张)

按 S10 的 7 阶段框架,逐阶段对位讲落地。

---

## 阶段 0:Bootstrap(1 张)

# todo: 改为对清楚项目背景，技术栈，使用场景，部署形态等等
---

## 阶段 1:Alignment(2 张)

### S14 — 阶段 1:Alignment 是什么

**视觉**:7 阶段图,Alignment 高亮

**口播要点**
- 跟 agent 对齐**要做什么、为什么做、什么算完成**
- 三种实用模式:
  - **Grill Me**:让 agent 反向盘问你,逼出隐藏假设
  - **Superpower Brainstorm**:开放探索后收敛
  - **AskUserQuestion**:从最小 spec 开始访谈,再开新 session 执行
- **到位的信号**:能用**一句可执行的话**回答"完成是什么样"——`npm test passes`、`curl 返回 200`,不是"代码写得好"

### S15 — 我们的对齐实践

**视觉**:一段实际的 Grill Me 对话截图

**口播要点**
- 早期我们直接告诉 agent"去做 XXX"——后面踩坑章节会展开为什么这样不行
- 现在的做法:先 Grill Me 让 agent 把模糊点提出来,人解答完再进入 Design
- 心得:**这一步看起来慢,但比让 agent 跑歪了再回滚便宜得多**

---

## 阶段 2:Design — OpenSpec(2 张)

### S16 — 阶段 2:Design 是什么

**视觉**:7 阶段图,Design 高亮 + 三个关键原则卡片

**口播要点**
- 把对齐好的需求拆成 agent 能消化的颗粒度
- 三个关键原则:
  1. **SDD 工具**:OpenSpec / Spec-Kit / Kiro 之类
  2. **纵向切片优于横向分层**——agent 默认 DB→API→前端横向分,这会推迟端到端反馈;**强制按贯穿所有层的小功能切**
  3. **阶段化、带门禁的计划**——每阶段配可执行测试
- **spec 不冻结**:实现中的发现要回流到 spec

### S17 — OpenSpec:规格作为工作合同

**视觉**:`openspec/` 目录结构 + 工作流 (Proposal → Implementation → Archive)

**口播要点**
- 一句话:**规格文档作为 agent 的工作合同**
- 三阶段工作流:
  - **Proposal**:写 proposal.md(做什么、为什么、边界、成功标准),review 完再动代码
  - **Implementation**:agent 以 proposal 为合同,边实现边更新规格
  - **Archive**:完成的规格 merge 进主规格库,成为项目知识
- 对 harness 的两大价值:
  - **解决 one-shotting**:spec 写明边界,agent 不再想一次做完
  - **跨会话记忆载体**:spec 在文件系统上,新 session 读 spec 立刻知道之前做到哪 → 正是 Anthropic 说的"**进度持久化在文件系统而非 context**"
// todo: 加上openspec 文档架构
---

## 阶段 3:Implement(1 张)

### S18 — 阶段 3:Implement

**视觉**:7 阶段图,Implement 高亮 + 四个实现技巧卡片

**口播要点**
- 让 agent 按 spec 落地,四个关键技巧:
  - **TDD**:测试先行,把"完成"变成可执行的
  - **Ralph Loop**:Anthropic 官方插件,适合"明确成功标准 + 需要多次试错"的场景(批量迁移、lint 清理、修一类 bug)
  - **Subagents / 并行 worktrees**:隔离 context,多线推进

- 回扣理论 S7 那句话:**永远不要让 agent 在你审查和批准书面计划之前写代码**

---

## 阶段 4:Verify — eval-loop(4 张,本场核心)

### S19 — 阶段 4:Verify 是什么 + 为什么需要 eval-loop

**视觉**:7 阶段图,Verify 高亮 + 问题描述

**口播要点**
- Verify 分两层:
  - **自动化层**:UT、E2E、Bench、Lint
  - **LLM-as-Judge 层**:评代码质量、spec 一致性、约定遵守
- **关键原则**:**用全新 context 的 agent 来 review**——Claude 不会偏袒它刚写的代码
- **Writer/Reviewer 模式比单 agent 自查可靠得多**(回扣 S7 的洞察:模型无法可靠评估自己的工作)
- 我们项目的特殊挑战:**LLM 生成的 DSL 质量怎么量化?**
  - 44 个 fixture,改一处不可能全人工检查
  - DSL 好坏不是二元的——组件对/字段全/格式对/布局清晰是四个独立维度

### S20 — eval-loop 架构

**视觉**:完整 pipeline 流程图

```
pnpm eval start
  ├─ 1. LLM 重新生成 DSL 快照
  ├─ 2. Playwright 启动 headless Chromium 渲染 + 截图
  ├─ 3. LLM-as-Judge 四维打分
  └─ 4. 输出 task-bundle
        ├─ summary.md
        ├─ screenshots/
        └─ adapters/claude-code.md(给 agent 的自包含 prompt)

      ↓ agent 读 bundle,修源码

pnpm eval verify <run-id>
  → 重跑全套 + delta report
  → Score: 6.4 → 7.8 (+1.4) ✅
```

**口播要点**
- 关键设计:**agent 能"看到"自己生成的 UI 截图再去改**
- 不是只给数字分数,是给 Playwright 截图——这是**视觉反馈闭环**
- 这正是 Generator-Evaluator 迭代的具体实现

### S21 — Judge 的四个维度

**视觉**:四维度表格

| 维度 | 衡量什么 | 对应的 agent 翻车 |
|---|---|---|
| component_fit | 组件类型对吗? | 数据是表格,选了卡片 |
| data_completeness | 字段全吗? | 关键字段被省略 |
| format_quality | 格式对吗? | 时间戳原样输出 |
| layout_coherence | 布局清晰吗? | 层级混乱、密度失控 |

**口播要点**
- 每个维度都对应一种真实的翻车类型
- **Human Corrections 机制**:`corrections.json` 让人工修正 feed 回 judge,保持自动评分和人类判断对齐
- 这就是 harness 飞轮的具体实现:**修正不是一次性口头反馈,是系统化沉淀**

### S22 — 真实数据迭代

**视觉**:6.4 → 7.8 的 delta 图 + 四维度变化柱状图

**口播要点**
- 起点 6.4/10,Judge 指出 `component_fit` 和 `format_quality` 最低
- Agent 读 task-bundle + 看截图 → 修源码 → verify → 7.8 (+1.4)
- `component_fit` 从最差变成进步最大的维度——**看到"卡片渲染了表格数据"这种视觉证据后,agent 能做正确修正**
- 这是 Generator-Evaluator 迭代的实际效果

---

## 阶段 5:Code Review(1 张)

### S23 — 阶段 5:Code Review + 架构债扫描

**视觉**:7 阶段图,Code Review 高亮

**口播要点**
- 合入前最后一道关
- 两层:
  - **PR 机器人**:CodeRabbit、Claude Code Review 自动 review 每个 PR
  - **定期架构债扫描**:不只看单 PR,做定时 `/techdebt` 命令——扫重复模式、违反约定、可抽象的地方
- **原则**:**任何"每天做不止一次"的事,都该变成 skill 或 command**

---

## 阶段 6:Retrospective + 反馈回路(2 张,杠杆最大)

### S24 — 阶段 6:Retrospective — 整个 loop 的复利引擎

**视觉**:7 阶段图,Retrospective 高亮 + 四个复盘问题卡片

**口播要点**
- **这是最被低估、杠杆最大的环节**
- 复盘要回答 4 个问题:
  1. agent 哪里走偏了?根因是 spec 不清、context 不够、还是缺约束?
  2. 哪些 prompt/操作我们重复做了 2 次以上?→ **skill 候选**
  3. 哪些坑是这个 codebase 特有的?→ 进 `CLAUDE.md`/`AGENTS.md`
  4. 哪些 review 反馈反复出现?→ 变成 lint 规则或 judger 评分项
- **沉淀去向**(按抽象层级递增):

| 类型 | 去处 |
|---|---|
| 项目约定、踩坑 | `CLAUDE.md` / `AGENTS.md` |
| 高频单步操作 | `.claude/commands/` (slash command) |
| 可复用工作流 | `.claude/skills/` (skill) |
| 必须发生的事 | hooks (pre-commit、stop 等) |
| 跨项目流程 | plugin |

### S25 — 反馈回路:Harness 优化 Harness

**视觉**:回到 S10 的螺旋图,这次重点高亮 Retrospective → Bootstrap 这条回流箭头

**口播要点**(本场点题)
- 复盘产出**回流到 Bootstrap**——CLAUDE.md 更全、skill 库更厚、judger 更严、Ralph Loop 的 completion criteria 写得更准
- **这不是瀑布,是螺旋**
- **Harness Engineering 真正的复利:harness 自己也在被 harness 优化**
- 这就是为什么 OpenAI Codex 七人能写一百万行——不是模型多强,是 harness 飞轮转了多久

---

## S28 — 
// todo: harness engineering 本质上就是基于大模型的软件工程，讲讲未来形态的long-horizon agent 和这个项目https://github.com/openai/symphony

---

## 附录:关键参考资料

- 李宏毅:[Harness Engineering 课堂视频](https://www.youtube.com/watch?v=R6fZR_9kmIw)
- 李宏毅:[AI Agent (1/3): Context Engineering 基本概念解说](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2450s)
- OpenAI:[Harness Engineering: Leveraging Codex in an Agent-First World](https://openai.com/index/harness-engineering/)
- Anthropic:[Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Birgitta Böckeler:[Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
- LangChain:[The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
- 项目代码:[HoikanChan/openui](https://github.com/HoikanChan/openui)