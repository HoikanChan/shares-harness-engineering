# Harness Engineering 演讲大纲 v3

> **结构**:理论 36% + 实践 64%(约 4:6)
> **理论主线**:Prompt → Context → Harness 三阶段演进,Context Engineering 深挖作为 Harness 的地基
---

# 第一段:理论(9 张)

## S1 — 封面 + 开场钩子

**视觉**:封面 slide,大标题"Harness Engineering——突破单智能体天花板"

**口播要点**
- 今天先不从定义讲起,从一个大家很熟悉的失败场景讲起
- 当我们第一次把一个复杂需求丢给单个 Claude / Codex / Cursor session 时,结果往往是这样的:
  - 给它 20 分钟、花掉几美元 token,它能生成一个**看起来像那么回事**的骨架
  - 但仔细检查会发现:跑不起来、接口互相矛盾、边界条件没处理、安全漏洞随处可见
- 这不是单纯的"模型不够聪明",而是**认知架构不够稳**

**单智能体的两个天花板**
1. **上下文窗口侵蚀**
   - 对话历史越长,早期决策越容易被冲淡
   - 第 50 轮工具调用时做出的选择,可能已经和第 5 轮的架构决策冲突
   - 问题不是它没看过上下文,而是上下文里所有东西都在抢注意力
2. **自我评估失灵**
   - 同一个 agent 先写代码、再审查自己的代码,天然容易给出正面评价
   - 它很难对自己刚刚做出的决策保持批判距离

**开场结论**
- Harness 正是为了突破这两个瓶颈而存在
- 它不是一个 prompt 技巧,而是一种系统架构:用流程、工具、隔离、反馈和门禁,把一个会自己跑的模型变成可靠的软件工程劳动力

---

## S2 — 工程师的工作搬了三次家

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

## S3 — Context Engineering 深挖之一:放什么 + 核心挑战

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

**关键拆分**:Context 不是只有对话框里那一坨文本,它至少分两类:
- **存储里的 context**:代码、文档、spec、历史 PR、issue、日志、截图、数据库状态。它容量大、可持久化,但 agent 需要知道去哪里找
- **对话中的 context**:当前 session 真正塞进 context window 的内容。它访问最快,但最贵、最短命、最容易被污染

所以 Context Engineering 的核心不是"把信息都喂给模型",而是**设计一套取数机制**:
- 什么信息长期存在文件系统/知识库里
- 什么信息在任务开始时被检索进来
- 什么信息必须留在当前对话里
- 什么信息只应该被总结,不应该原文保留

这也是为什么 `CLAUDE.md`/`AGENTS.md` 不应该写成百科全书。它更像索引页:告诉 agent **这个项目的信息在哪里,遇到什么任务应该先读什么**。

---

## S4 — Context Engineering 深挖之二:核心手段 + 天花板

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

**Context 还有一个工程上绕不开的问题:压缩**
- 长任务跑到一半,context window 快满时,系统会开始总结、裁剪、压缩历史
- 压缩不是无损的。细节会丢,判断依据会变模糊,早期约束可能只剩一句摘要
- 这就是很多长 session 后半段开始"漂"的原因:agent 还在继续跑,但它拿到的已经不是原始任务现场

**Subagent 的价值在这里出现**
- Subagent 不是为了炫技,而是为了**隔离上下文**
- 主 agent 保留目标、计划和验收标准;子 agent 只拿一个边界清楚的小任务
- 子 agent 完成后返回摘要、diff、证据,主 agent 再整合
- 这样比一个超长 session 一路滚到底更稳:每个子任务的 context 更短、更干净,失败也更容易回滚

→ 这就是为什么我们需要从 Context Engineering 升级到 **Harness Engineering**

---

## S5 — Harness 登场:LLM 的操作系统

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

## S6 — Harness 框架:Plan → Generate → Evaluate

**视觉**:三角色工作流图:Planner 拆任务 → Generator 执行 → Evaluator 验收,旁边一条 Ralph Loop 回路

**口播要点**
- Harness 不是让模型"更努力",而是给模型安排一套标准工作流程
- Anthropic、DeepMind、OpenAI 的实践虽然细节不同,但核心都很像:
  1. **Plan**:先把人类需求拆成更小的任务,明确边界和成功标准
  2. **Generate**:让 agent 只执行当前切片,不要一次吞下整个项目
  3. **Evaluate**:用测试、工具、另一个 agent、或者人类 review 来验收

**为什么必须有 Evaluator?**
- LLM 是 autoregressive 生成:前面走错了,后面很容易沿着错误继续补
- 很多错误不是"不会",而是**覆水难收**:它生成到一半才发现不对,但当前输出已经被前文锁死
- Evaluator 的作用是把这个过程切断:停下来、检查、反馈、重来

**Ralph Loop**
```
Generate v1 → Evaluate → Feedback
        ↑                    ↓
        └────── Generate v2 ─┘
```
- Feedback 可以来自 LLM judge,也可以来自 compiler、test、lint、Playwright 截图
- 重点不是"让模型想更久",而是**让模型看到真实反馈后迭代**

**长任务里的 context 焦虑**
- Ralph Loop 跑久了也会把 context 撑爆
- 常见做法是每轮只保留摘要和关键证据,把完整日志放到文件系统
- 这说明 harness 不是固定模板,而是要根据模型能力、任务长度、反馈形态不断重配
---

## S7 — Agent 四种翻车 + 核心飞轮

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

## S8 — 业界共识:瓶颈在基础设施

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

## S9 ★ 7 阶段工作流框架(承上启下核心页)

**视觉**:**这是整场最重要的一张图**——7 阶段螺旋 + 反馈回路

```
        ┌──── Retrospective (6) ────┐
        │   回流:project.md/spec/   │
        │   CLAUDE.md/skill/judge   │
        ↑                           ↓
   Code Review (5)            Bootstrap (0)
   PR 机器人/架构债扫描       project.md/CLAUDE.md/MCP
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
- 上半场讲的三大支柱(认知/能力/流程)在这里都有对应位置——**Bootstrap 是认知入口,Verify 是反馈系统,settings/MCP 是能力边界**
- 每个阶段都有明确产出、明确判断到位的信号
- **关键不是这 7 个阶段本身,是中间的反馈回路**——复盘的产出回流到 Bootstrap 和 Design,让 `project.md` 更准、spec 更完整、judger 更严
- **这不是瀑布,是螺旋——harness 自己也在被 harness 优化**

**实践过渡**:
- 理论讲到这里,关键问题就变成:这些原则在真实工程里到底长什么样?
- 下面不讲抽象概念,按这张图一阶段一阶段拆
- 每个阶段都回答三个问题:**输入是什么、产出是什么、怎么判断它到位**

[喝口水,让大家缓一下]

---

# 第二段:我们的 Harness 实践(14 张)

按 S9 的 7 阶段框架,逐阶段对位讲落地。

---

## 阶段 0:Bootstrap(1 张)

### S10 — 阶段 0:Bootstrap:先让 agent 读懂项目

**视觉**:`openspec/project.md` 作为中心文档,周围连接"项目背景 / 技术栈 / 使用场景 / 部署形态 / 边界约束"

**口播要点**
- Bootstrap 不是"把环境装起来"这么简单
- 它更像给一个新同事做概要设计 onboarding:先让 agent 明白这个项目为什么存在、怎么运行、哪些地方不能乱动

**核心产物**:`openspec/project.md`
- **项目背景**:这个系统解决什么问题,主要用户是谁,为什么现在的设计是这样
- **技术栈**:前端、后端、数据层、任务队列、模型调用、测试框架分别是什么
- **使用场景**:用户如何进入系统,关键 workflow 是什么,哪些路径最重要
- **部署形态**:本地开发、测试环境、生产环境怎么跑,依赖哪些外部服务
- **架构边界**:哪些模块是稳定接口,哪些模块可以重构,哪些地方有历史债
- **操作入口**:常用命令、测试命令、eval 命令、日志位置、排障入口

**到位的信号**
- 新开一个 agent session,它读完 `project.md` 后,能用自己的话说明:
  - 这个项目的目标
  - 主要模块和数据流
  - 当前任务应该先看哪些文件
  - 什么行为算越界

**关键点**:`project.md` 不是一次性文档。每次复盘发现 agent 因为项目背景不清走偏,都要回流更新这里。

---

## 阶段 1:Alignment(2 张)

### S11 — 阶段 1:Alignment 是什么

**视觉**:7 阶段图,Alignment 高亮

**口播要点**
- 跟 agent 对齐**要做什么、为什么做、什么算完成**
- 三种实用模式:
  - **Grill Me**:让 agent 反向盘问你,逼出隐藏假设
  - **Superpower Brainstorm**:开放探索后收敛
  - **AskUserQuestion**:从最小 spec 开始访谈,再开新 session 执行
- **到位的信号**:能用**一句可执行的话**回答"完成是什么样"——`npm test passes`、`curl 返回 200`,不是"代码写得好"

### S12 — 我们的对齐实践

**视觉**:一段实际的 Grill Me 对话截图

**口播要点**
- 早期我们直接告诉 agent"去做 XXX"——后面踩坑章节会展开为什么这样不行
- 现在的做法:先 Grill Me 让 agent 把模糊点提出来,人解答完再进入 Design
- 心得:**这一步看起来慢,但比让 agent 跑歪了再回滚便宜得多**

---

## 阶段 2:Design — OpenSpec(2 张)

### S13 — 阶段 2:Design 是什么

**视觉**:7 阶段图,Design 高亮 + 三个关键原则卡片

**口播要点**
- 把对齐好的需求拆成 agent 能消化的颗粒度
- 三个关键原则:
  1. **SDD 工具**:OpenSpec / Spec-Kit / Kiro 之类
  2. **纵向切片优于横向分层**——agent 默认 DB→API→前端横向分,这会推迟端到端反馈;**强制按贯穿所有层的小功能切**
  3. **阶段化、带门禁的计划**——每阶段配可执行测试
- **spec 不冻结**:实现中的发现要回流到 spec

### S14 — OpenSpec:规格作为工作合同

**视觉**:`openspec/` 目录结构 + 工作流 (Proposal → Implementation → Archive)

**口播要点**
- 一句话:**规格文档作为 agent 的工作合同**
- OpenSpec 不只是几份 markdown,而是一个**命令驱动的规格状态机**

**四层文档架构**
```
openspec/
  project.md                         # 项目级背景:Bootstrap 的核心输入
  specs/<capability>/spec.md         # 长期能力规格:系统应该持续满足什么
  changes/<change-id>/proposal.md    # 本次变更:为什么做、做什么、不做什么
  changes/<change-id>/design.md      # 技术方案:关键设计和取舍
  changes/<change-id>/tasks.md       # 执行清单:可验证的小步任务
```

**命令触发阶段变化**
- `openspec init` → 生成/更新 `project.md`,进入 Bootstrap
- `openspec propose <change>` → 生成 `proposal.md / design.md / tasks.md`,进入 Design
- `openspec validate <change>` → 检查规格完整性、门禁和测试映射,进入 Verify
- `openspec archive <change>` → 把完成的 change 合并进长期 `specs/`,进入 Retrospective 回流

**三阶段工作流**
- **Proposal**:写清楚做什么、为什么、边界、成功标准,review 完再动代码
- **Implementation**:agent 以 proposal 为合同,按 tasks 小步实现,边实现边更新规格
- **Archive**:完成的规格 merge 进主规格库,成为项目知识
- 对 harness 的两大价值:
  - **解决 one-shotting**:spec 写明边界,agent 不再想一次做完
  - **跨会话记忆载体**:spec 在文件系统上,新 session 读 spec 立刻知道之前做到哪 → 正是 Anthropic 说的"**进度持久化在文件系统而非 context**"
---

## 阶段 3:Implement(1 张)

### S15 — 阶段 3:Implement

**视觉**:7 阶段图,Implement 高亮 + 四个实现技巧卡片

**口播要点**
- 让 agent 按 spec 落地,四个关键技巧:
  - **TDD**:测试先行,把"完成"变成可执行的
  - **Ralph Loop**:Anthropic 官方插件,适合"明确成功标准 + 需要多次试错"的场景(批量迁移、lint 清理、修一类 bug)
  - **Subagents / 并行 worktrees**:隔离 context,多线推进

- 回扣理论 S6 那句话:**永远不要让 agent 在你审查和批准书面计划之前写代码**

---

## 阶段 4:Verify — eval-loop(4 张,本场核心)

### S16 — 阶段 4:Verify 是什么 + 为什么需要 eval-loop

**视觉**:7 阶段图,Verify 高亮 + 问题描述

**口播要点**
- Verify 分两层:
  - **自动化层**:UT、E2E、Bench、Lint
  - **LLM-as-Judge 层**:评代码质量、spec 一致性、约定遵守
- **关键原则**:**用全新 context 的 agent 来 review**——Claude 不会偏袒它刚写的代码
- **Writer/Reviewer 模式比单 agent 自查可靠得多**(回扣 S6 的洞察:模型无法可靠评估自己的工作)
- 我们项目的特殊挑战:**LLM 生成的 DSL 质量怎么量化?**
  - 44 个 fixture,改一处不可能全人工检查
  - DSL 好坏不是二元的——组件对/字段全/格式对/布局清晰是四个独立维度

### S17 — eval-loop 架构

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

### S18 — Judge 的四个维度

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

### S19 — 真实数据迭代

**视觉**:6.4 → 7.8 的 delta 图 + 四维度变化柱状图

**口播要点**
- 起点 6.4/10,Judge 指出 `component_fit` 和 `format_quality` 最低
- Agent 读 task-bundle + 看截图 → 修源码 → verify → 7.8 (+1.4)
- `component_fit` 从最差变成进步最大的维度——**看到"卡片渲染了表格数据"这种视觉证据后,agent 能做正确修正**
- 这是 Generator-Evaluator 迭代的实际效果

---

## 阶段 5:Code Review(1 张)

### S20 — 阶段 5:Code Review + 架构债扫描

**视觉**:7 阶段图,Code Review 高亮

**口播要点**
- 合入前最后一道关
- 两层:
  - **PR 机器人**:CodeRabbit、Claude Code Review 自动 review 每个 PR
  - **定期架构债扫描**:不只看单 PR,做定时 `/techdebt` 命令——扫重复模式、违反约定、可抽象的地方
- **原则**:**任何"每天做不止一次"的事,都该变成 skill 或 command**

---

## 阶段 6:Retrospective + 反馈回路(2 张,杠杆最大)

### S21 — 阶段 6:Retrospective — 整个 loop 的复利引擎

**视觉**:7 阶段图,Retrospective 高亮 + 四个复盘问题卡片

**口播要点**
- **这是最被低估、杠杆最大的环节**
- 复盘要回答 4 个问题:
  1. agent 哪里走偏了?根因是 spec 不清、context 不够、还是缺约束?
  2. 哪些项目背景或架构边界没讲清?→ 更新 `openspec/project.md`
  3. 哪些 prompt/操作我们重复做了 2 次以上?→ **skill/command 候选**
  4. 哪些 review 反馈反复出现?→ 变成 lint 规则或 judger 评分项
- **沉淀去向**(按抽象层级递增):

| 类型 | 去处 |
|---|---|
| 项目背景、架构边界 | `openspec/project.md` |
| 能力规格、行为约束 | `openspec/specs/*/spec.md` |
| agent 操作规则、踩坑 | `CLAUDE.md` / `AGENTS.md` |
| 高频单步操作 | `.claude/commands/` (slash command) |
| 可复用工作流 | `.claude/skills/` (skill) |
| 必须发生的事 | hooks (pre-commit、stop 等) |
| 跨项目流程 | plugin |

### S22 — 反馈回路:Harness 优化 Harness

**视觉**:回到 S9 的螺旋图,这次重点高亮 Retrospective → Bootstrap / Design 这条回流箭头

**口播要点**(本场点题)
- 复盘产出**回流到 Bootstrap 和 Design**——`project.md` 更清楚、`specs/` 更完整、CLAUDE.md 更有针对性、judger 更严
- **这不是瀑布,是螺旋**
- **Harness Engineering 真正的复利:harness 自己也在被 harness 优化**
- 这就是为什么 OpenAI Codex 七人能写一百万行——不是模型多强,是 harness 飞轮转了多久

---

## S23 — 未来形态:从驱动 Agent 到监督 Agent

**视觉**:左边"人驱动 agent"的对话窗口,右边"项目看板 → 多个隔离 workspace → PR / 证据 / review"的控制平面

**口播要点**
- 如果 Harness 做得足够强,软件工程的工作方式会发生一次角色切换
- 今天很多人用 agent 的方式还是:**人不停地驱动大模型工作**
  - 给它任务
  - 看它跑
  - 发现跑偏再纠正
  - 继续喂下一步
- 但更成熟的形态应该是:**人监督 agent,而不是逐步驾驶 agent**

**前提是 harness 足够坚固**
- 项目背景清楚:`project.md` / `CLAUDE.md` 能让 agent 快速进入现场
- 任务边界清楚:issue / proposal / tasks 能定义完成标准
- 执行环境隔离:每个任务有自己的 workspace,失败不会污染主线
- 验证体系可靠:test / eval / judge / PR review 能给出证据
- 复盘能回流:失败会沉淀成规则、spec、skill、hook、judger

**Symphony 代表的方向**
- OpenAI Symphony 把 Linear 这类项目管理板变成 coding agents 的控制平面
- 每个 issue 可以触发一个隔离的 autonomous implementation run
- Agent 不是等人一步步喂 prompt,而是围绕任务状态、workspace、验证证据持续推进
- 人类的工作从"盯着一个 agent 写代码"上移到"管理工作流、审查证据、加固 harness"

**本场收束**
- Harness Engineering 本质上就是**基于大模型的软件工程**
- 当模型越来越强,真正稀缺的不是多写几句 prompt,而是:
  - 怎么定义任务边界
  - 怎么设计反馈回路
  - 怎么控制权限和风险
  - 怎么把失败沉淀成基础设施
- 未来一部分任务人确实不需要亲手做了,但这不等于工程师消失
- 工程师的重心会转向更上层:建设让 agent 可以可靠工作的 infrastructure

---

## 附录:关键参考资料

- 李宏毅:[Harness Engineering 课堂视频](https://www.youtube.com/watch?v=R6fZR_9kmIw)
- 李宏毅:[AI Agent (1/3): Context Engineering 基本概念解说](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2450s)
- OpenAI:[Harness Engineering: Leveraging Codex in an Agent-First World](https://openai.com/index/harness-engineering/)
- Anthropic:[Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Birgitta Böckeler:[Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
- LangChain:[The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
- OpenAI:[An open-source spec for Codex orchestration: Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/)
- OpenAI:[Symphony GitHub repo](https://github.com/openai/symphony)
- 项目代码:[HoikanChan/openui](https://github.com/HoikanChan/openui)
