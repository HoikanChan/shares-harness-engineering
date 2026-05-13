# Harness Engineering 演讲稿

> **受众**：团队内部工程师（熟悉 LLM）  
> **时长**：40-60 分钟  
> **结构**：两段式 — 理论脉络 + 我们的实践  
> `[方括号]` = 演讲者提示，不需要念出来

---

## 🎯 开场

---

### S1 — 封面

[打开第一张 slide，停顿两秒，扫视全场]

大家好。今天分享的主题是 Harness Engineering——怎么驾驭一匹会自己跑的马。

开始之前，我想先问大家一个问题。

你有没有遇到过这样的情况：你让一个 AI agent 去干活，结果隔天早上来看——它不只完成了你让它做的事，还"顺便"重构了三个你没让它碰的模块，引入了一个循环依赖，然后在凌晨三点自信满满地把自己的 PR merge 进去了。

CI 亮一排红灯。Slack 炸了。Tech lead 在群里 @all。

这不是段子。这是 AI agent 从实验工具进化到生产系统后，每天都在上演的真实场景。

那问题到底出在哪里？是模型不够聪明吗？

今天我想给你一个不同的答案。

---

### S2 — 钩子：Gemma 3 2B 实验

[切到实验对比 slide]

这是李宏毅老师最近在课堂上做的一个实验。

他用 Google 开源的小模型 Gemma 3 2B，布置了一个任务：修复 `parser.py` 里的 bug，让它能正确从文字里抓出 email。文件就放在模型旁边，可以通过 bash 指令读取。

**第一次，没有额外引导。**

模型的反应是——它直接幻想了一段自己以为 `parser.py` 该有的内容，验证了自己的幻想，然后告诉李宏毅："做完了。"

什么文件都没打开，什么 bug 都没修，但它说它完成了。

**然后李宏毅只多给了 80 个字的引导。**

内容很简单，不到三条原则：
- 动手前先 `ls`，看看手边有什么
- 要改的文件先 `cat` 打开看看
- 完成的标准要达到具体的 criteria

同一个模型，同一道题。

第二次：`ls` → `cat` → 改文件 → 跑测试 → 成功交差。

李宏毅给学生下了一个结论，也是今天整个分享的核心命题——

> **"有时候语言模型不是不够聪明，它只是缺乏人类的引导。"**

OpenAI 工程师 Ryan Lopopolo 说过一句话：

> **"Agents aren't hard; the Harness is hard."**

那个引导机制，那个让 agent 能稳定跑的系统，就是我们今天要讲的：**Harness Engineering**。

---

## 第一段：理论脉络

---

### Chapter 1 — 工程师的工作搬了三次家

---

### S3 — 三阶段一张图

[切到三阶段演进图]

要理解 Harness Engineering 为什么现在突然这么热，得先看这几年 AI 工程实践的演变。

AI 工程师的工作，在三个阶段里搬了三次家。

**第一阶段：Prompt Engineering，大概 2022 到 2024 年。**

那时候模型很笨，但听话。工程师的工作是什么？雕一条指令，找到那个"完美的 prompt"。模型对措辞极其敏感，一个词的增删，输出质量天差地别。每个人的笔记本里都存着几百条精心调校的 prompt。

**第二阶段：Context Engineering，2025 年。**

模型变强了，agent 能用工具了。Karpathy 有一个很好的比喻：LLM 是 CPU，context window 是 RAM，而你是负责载入正确信息的操作系统。工程师的工作从"怎么说"变成了"给它看什么"。

**第三阶段：Harness Engineering，2026 年。**

模型现在可以自己跑了。工程师的工作从"管信息"，变成了"搭笼子"——让 AI 在里面安全地跑。

[停顿一下]

注意：这三个阶段不是替代关系，是包含关系。Harness Engineering 把前两代都吸收进来了。Prompt 和 Context 没有死，它们被升职了，变成更大系统里的子模块。

---

### S4 — 为什么现在到了 Harness 时代

LangChain 有一个极简公式：

> **Agent = Model + Harness**

模型是马，Harness 是马具——缰绳、马鞍、嚼子。马有再强的力气，没有马具就只是一匹野马。

以前我们不需要马具，因为马跑不快，走几步就停了。

现在模型足够强了，它能自己跑，能自己做决定，能自己用工具——这就是问题的开始。你必须开始认真思考：怎么让它跑得准、跑得稳、跑在正确的方向上。

这就是为什么 2026 年 Harness Engineering 突然热起来。2 月 OpenAI 发了《Harness Engineering: Leveraging Codex in an Agent-First World》；3 月 Anthropic 发了《Harness Design》；Martin Fowler 也专文介绍。两家龙头一前一后，风向很明显。

---

### Chapter 2 — Context Engineering 深挖

---

### S5 — Context 里放什么

[切到 context 分类 slide]

在进入 Harness 之前，我们先把 Context Engineering 讲透，因为它是理解 Harness 的地基。

Context window 里能放什么？大致可以分成几类：

- **指令**（Instructions）：你希望 agent 怎么行事的规则，CLAUDE.md 里的内容
- **工具**（Tools）：agent 能调用什么——bash、文件读写、浏览器、MCP server
- **记忆**（Memory）：过去做过什么、学到了什么，可以是文件、可以是 git log
- **状态**（State）：当前任务进行到哪一步了
- **历史**（History）：这个 session 里的对话记录

这五类东西，都在抢同一个有限的 context window。

---

### S6 — Context 的核心挑战

Context 管理有三个核心挑战：

**第一，窗口有限。** Context window 是稀缺资源。你把所有东西都塞进去，模型会把重要的和不重要的一视同仁，或者完全迷失。

**第二，信息腐烂。** 有一个经典研究叫"Lost in the Middle"——模型对放在 prompt 开头和结尾的信息更敏感，中间的信息容易被"遗忘"。Context 越长，信息越容易腐烂。

**第三，跨会话记忆丢失。** 这是最痛的。Agent 没有天生的跨会话记忆——每次新会话启动，它对上次做了什么一无所知。就像一个项目组全是轮班工程师，每个人上岗时对之前的进展一脸懵。

---

### S7 — Context 管理的核心手段

面对这些挑战，工程师们总结出来的核心原则是：

**好的指令档应该像地图，不是六法全书。**

OpenAI 在他们的 blog 里特别提醒：指令档不能写成六法全书，那会占掉模型大部分的 context window，反而让它什么都做不好。更好的做法是提供一个精简的入口点，然后"教" agent 根据当前任务按需检索和拉取更多的上下文。

Mitchell Hashimoto 的 Ghostty 项目 AGENTS.md 里每一行都对应一个历史 agent 失败案例。这份文件不是"大而全的规范手册"，而是一部"避坑指南"——每条规则都有来历。

这就引出了一个关键概念：**文档必须是活的反馈循环，不是静态制品。**

---

### S8 — Context Engineering 的天花板

Context Engineering 是巨大的进步——但它有一个致命盲点：**它只管单一 agent 的视角。**

当你需要多个 agent 协作、需要在 agent 完成工作后验证结果、需要在 agent 犯错时自动回滚——Context Engineering 帮不了你。

更深的问题是：就算你给了 agent 完美的 context，你也无法阻止它在对的 context 里做出错的判断。

这就是为什么我们需要从 Context Engineering 升级到 Harness Engineering。

---

### Chapter 3 — Harness Engineering 核心

---

### S9 — Harness 是什么

[切到马具图]

Harness 这个词来自马具——缰绳、马鞍、嚼子，那一整套。

马有再强的力气，没有马具就只是一匹野马。Harness Engineering 不是去削弱 AI 的能力，而是为它打造一套黄金缰绳，让它跑得又快又稳。

有一个更精准的比喻：**我们重新发明了冯·诺依曼架构。**

原始 LLM 是 CPU；context window 是 RAM，快速但有限；外部文件系统是磁盘存储；工具是设备驱动；而 Harness，就是操作系统。

操作系统让 CPU 能安全、可靠、高效地运行。Harness 让 LLM 能安全、可靠、高效地完成任务。

---

### S10 — 认知框架：AGENTS.md / CLAUDE.md

[切到 AGENTS.md 示例 slide]

李宏毅把"搭笼子"的具体手段拆成三块。第一块是**控制认知框架**——用人类语言写规则，塞进 AI 的 prompt。

Thoughtworks 的 Böckeler 把 Harness 的机制分为两类：
- **Guides（前馈控制）**：在 agent 行动前介入，告诉它规则是什么
- **Sensors（反馈控制）**：在 agent 行动后介入，观察结果并产生修正信号

AGENTS.md 就是最基础的 Guide。

**但怎么写是关键。**

好的 AGENTS.md 应该像地图，告诉 agent"想知道什么去哪里找"。而且每一行都应该有来历——

[切到 OpenClaw CLAUDE.md 对比截图]

**OpenClaw 的 CLAUDE.md 就是一个很好的例子。**

OpenClaw 是李宏毅老师的 AI 助手"小金"运行的框架。它的 CLAUDE.md 有一个特点：里面每一条规则，都对应一个历史上 agent 犯过的错。

比如那条规则："完成任务前必须先 `ls` 确认文件存在。" 这条规则的背后，就是 Gemma 实验里那次翻车——agent 幻想了一个不存在的文件，以为自己改了，其实什么都没做。

[对比两种写法]

**坏的写法**：密密麻麻几百行，把所有规范全塞进去。Agent 在回应里开始大量引用规则，而不是做事。Context 被规则文档占满。

**好的写法**：精简、有来历、每条规则背后都有一个真实的翻车故事。这份文件是随着 agent 每次犯错慢慢长出来的，不是一次写完的。

这就是"活的反馈循环"：agent 犯错 → 人类归因 → 补进 AGENTS.md → 下次 agent 不再犯同样的错。

---

### S11 — 能力边界：工具权限控制

[切到 OpenClaw vs Cowork 对比 slide]

第二块：**控制能力边界**——用工具限制 agent 能做什么。

李宏毅用两个实际产品做了对比：

**OpenClaw（本地版 Claude Code）**：跑在你的电脑上，改文件、操控浏览器、执行任意 shell command 都能做。功能强，风险高——给了 agent 一把万能钥匙。

**Cowork（云端沙盒）**：跑在隔离的沙盒里，每次要访问本地文件都需要人类授权。安全，但有摩擦。

**便利性 vs 安全性的权衡，是 Harness 设计的第一道选择题。**

更精细的做法是按任务阶段动态控制权限。Anthropic 的实践：
- Research 阶段：只允许 `read_file`，不允许 `write_file`
- Implementation 阶段：允许写，但限定在指定目录
- Verification 阶段：只允许跑测试，不允许修改源代码

这种"状态机式的权限控制"，让 agent 在每个阶段只能做该做的事，大大降低了意外损坏的风险。

---

### S12 — 行为流程：Generator-Evaluator 迭代

[切到流程图 slide]

第三块：**控制行为流程**——规范 agent 怎么做事。

Anthropic 的经典设计是把 agent 角色拆成三个：

- **Planner**：把任务拆解为可执行的子任务列表
- **Generator**：一次只实现一个 feature，增量开发
- **Evaluator**：验证结果，产生反馈

这背后有一个核心洞察：**模型无法可靠地评估自己的工作。**

让同一个 agent 又生成又评估，等于让学生自己批自己的卷子。把生成和评估拆开，是行为流程设计里最重要的决策。

Cloudflare 的工程师 Boris Tane 说：

> "永远不要让 agent 在你审查和批准书面计划之前写代码。规划与执行的分离，是我做的最重要的一件事。"

---

### S13 — Agent 四种翻车姿势

[切到翻车 slide]

Anthropic 工程师总结了四种典型翻车：

**翻车一：One-shotting。** Agent 想在一个 session 里把所有功能做完。结果 context window 耗尽，留下一堆没有文档的半成品代码，下一个 session 启动时只能猜测之前发生了什么。

**翻车二：过早宣布胜利。** 部分功能完成后，agent 环顾四周，看到已有进展就直接宣布任务完成——即使还有大量功能未实现。

**翻车三：过早 mark done。** Agent 写完代码就标记"完成"，却没做端到端测试。单元测试通过了，不代表功能真正可用。

**翻车四：环境启动困难。** 每次新 session 启动，agent 需要花大量 token 弄清楚如何运行应用，而不是把时间花在实际开发上。

还有一个危险特性：**agent 非常擅长模式复制**。代码库里有什么模式，它就忠实地复制并放大——包括坏模式和架构漂移。不加约束的 agent 会以惊人的速度积累技术债务。

---

### S14 — 核心飞轮

[切到飞轮图]

把前面三块加起来，Harness Engineering 的核心工作方式是一个飞轮：

**Agent 犯错 → 人类归因 → 补 harness（文档/约束/验证） → 下次同类问题更少**

这个飞轮一直转，harness 就一直变好。

Mitchell Hashimoto 对 Harness Engineering 的定义：

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent will not make that mistake again in the future."

每次翻车不是损失，是投资。你在 AGENTS.md 里多写一条规则，在 eval 里多加一个测试，在权限控制里多加一道门——这些都是在让飞轮转得更稳。

---

### S15 — 业界参照

[切到业界案例 slide]

来看几个数字，感受一下这个方向的重量。

**OpenAI Codex 团队：七人，零行人工代码，一百万行。**
从一个空 repo 开始，所有代码全部由 Codex agent 生成。人类工程师在整个过程中没有手写过一行代码。关键不是模型有多强，而是他们花了多少时间打磨 harness。

**LangChain 的实验：同模型，换 harness，排名从第 30 跳到第 5。**
仅仅改变 harness 的工具格式，Grok Code Fast 1 的成绩从 6.7% 跳到 68.3%。

**五个独立团队，同一个结论：**
> "The bottleneck is infrastructure, not intelligence."

**Manus：六个月内用同一个模型重写了五次 Harness。** 每次重写带来的效能提升，都比换模型大得多。

这是目前业界最核心的共识：**瓶颈不在模型智能，在基础设施。**

---

### S16 — 理论段收尾

[停顿，扫视全场]

好，理论部分讲到这里。

总结一句话：

> **"瓶颈不在模型智能，在基础设施。"**

Harness 不是 prompt trick，不是调参。它是工程纪律——一套围绕 agent 设计约束机制、反馈回路、工作流控制的系统工程实践。

下半场，我来讲讲我们是怎么在自己项目里落地这套东西的。

[稍微停一下，喝口水，让大家缓一缓]

---

## 第二段：我们的 Harness 实践

---

### 项目背景（过渡）

[切到 OpenUI 介绍 slide]

先用一句话交代项目背景。

我们做的是 **OpenUI**——一个 Generative UI 框架，核心是让 LLM 流式生成 UI DSL，然后实时渲染成 React 组件。比 JSON 方案 token 效率高 52%。

这个项目的特殊性在于：**模型的输出本身就是我们的产品**。这就意味着 harness 对我们不只是开发效率的问题，而是产品质量的直接保障。

下面我会讲三层实践——认知框架、OpenSpec、和我们的 eval-loop。

---

### Chapter 4 — 认知框架层

---

### S17 — 多工具指令体系

[切到目录结构 slide]

第一块：认知框架。

我们的代码库里有三个目录：`.claude/`、`.codex/`、`.cursor/`。

这不是冗余——这是三套不同 agent 工具的指令配置，服务于同一个 harness 目标。

现实考量是：不同的 agent 工具有不同的指令格式。Claude Code 用 `CLAUDE.md`，Codex 有自己的配置格式，Cursor 有 `.cursorrules`。

我们的做法是维护一个**共同的核心约定**——项目架构、命名规范、关键禁止事项——然后翻译成三份工具特定的格式。

好处：不管团队成员用哪个工具，agent 拿到的约束是一致的。

---

### S18 — Agent Skill as Superpower

[切到 skills/openui/ 目录 slide]

第二个实践：`skills/openui/`——我们给 agent 装的"超能力"。

普通的 AGENTS.md 告诉 agent"规则是什么"。Skills 更进一步——**它给 agent 装上理解特定领域的专项能力**。

OpenUI 的 Agent Skill 里包含：
- **OpenUI Lang 语法**：DSL 的完整语法说明，agent 生成 DSL 时有明确的规范参照
- **组件体系**：内置组件的 props、用途、适用场景
- **如何调试 malformed 输出**：当模型输出的 DSL 解析失败时，常见错误类型和修复模式

为什么做成 skill 而不是直接塞进 AGENTS.md？

**Progressive disclosure（渐进式披露）**。不是每个任务都需要知道完整的 DSL 语法，只有在生成 UI 相关任务时才需要加载。Skill 按需加载，避免无关信息占用 context。

安装方式很简单：
```bash
npx skills add thesysdev/openui --skill openui
```

任何接入我们项目的 AI 工具，安装了这个 skill，就自动获得了理解 OpenUI Lang 的能力——这就是我说的"Superpower"。

---

### S19 — OpenSpec：规格作为工作合同

[切到 openspec/ 目录结构 slide]

第三个实践，也是我觉得最有意思的：**OpenSpec**。

用一句话概括：**规格文档作为 agent 的工作合同**。

工作流是这样的：

```
Proposal → Implementation → Archive
    ↓             ↓              ↓
proposal.md  →  写代码  →  merge 规格
```

**Proposal 阶段**：先用自然语言写一份 proposal.md，描述要做什么、为什么做、边界在哪、成功标准是什么。这份文档要在动代码之前写好、review 好。

**Implementation 阶段**：agent 以 proposal.md 作为工作合同，边实现边更新规格。

**Archive 阶段**：把已完成的规格 merge 进主规格库，成为项目知识的一部分。

这个流程对 harness 有两个重要价值：

**第一，解决 one-shotting 问题。** Agent 有了 spec 作为约束，就不会想一次把所有东西都做完。Spec 里明确写了这个 feature 的边界，它就在边界内工作。

**第二，跨会话记忆载体。** Spec 文件存在文件系统上，不在 context window 里。下一个 session 启动时，agent 读取 spec，立刻知道之前做了什么、现在处于什么状态。这正是 Anthropic 说的"进度持久化在文件系统上，而非 context window 中"。

---

### Chapter 5 — 行为流程层：Eval-Loop

---

### S20 — 为什么需要 eval-loop

[切到问题描述 slide]

现在进入最核心的部分。

我们的产品核心是让 LLM 生成 OpenUI DSL，然后渲染成 UI 组件。

有一个根本性的问题：**LLM 生成的 DSL 质量怎么量化？**

DSL 输出的好坏不是二元的。同样是生成一个数据表格，有的 DSL 选了正确的组件、所有字段都展示了、日期格式也对；有的 DSL 把表格数据放到了卡片里、只展示了一半字段、时间戳原样输出。

这两种输出，基础的 unit test 都能通过，但视觉质量差距很大。

我们有 44 个 fixture，每次改一个地方，不可能全部人工看一遍。

我们需要一个**自动化的 evaluator**，能持续衡量生成质量，并且驱动 agent 迭代改进。

---

### S21 — Eval-loop 架构

[切到架构图 slide]

这是我们实现的 eval-loop：

```
pnpm eval start
  │
  ├─ 1. LLM 重新生成 DSL 快照（regen snapshots）
  │
  ├─ 2. Playwright 启动 headless Chromium
  │     渲染每个 fixture，截图 .preview-shell
  │
  ├─ 3. LLM-as-judge 对每个 fixture 打分
  │     四个维度，每维度 0-3 分，加上总分 0-10
  │
  └─ 4. 输出 task-bundle
        ├─ summary.md（总分、最差的 fixture、failing patterns）
        ├─ screenshots/（Playwright 截图）
        └─ adapters/claude-code.md（给 agent 的自包含 prompt）

      ↓ agent 读 task-bundle，修源码

pnpm eval verify <run-id>
  → 重跑全套 + 重新打分 + delta report
  → Score: 6.4 → 7.8 (+1.4) ✅
```

这里有一个关键的设计决策：**agent 能"看到"自己生成的 UI 截图再去改**。

我们不只是给 agent 一堆数字分数，我们给它看 Playwright 截图——它生成的 DSL 渲染出来长什么样。这是一个**视觉反馈闭环**，让 agent 能在更接近真实用户体验的层面上做判断。

这正对应李宏毅老师讲的第三块——行为流程控制，我们的 eval-loop 就是 generator-evaluator 迭代的具体实现。

---

### S22 — Judge 的四个维度

[切到评分维度表]

Judge 的评分维度设计，对应了我们在实践中发现的最常见的 agent 翻车类型：

| 维度 | 衡量什么 | 对应的 agent 翻车 |
|---|---|---|
| **component_fit** | 组件类型选对了吗？ | 数据是表格，agent 选了卡片 |
| **data_completeness** | 字段展示完整吗？ | 关键字段被省略，用户看不到 |
| **format_quality** | 日期/数字格式对吗？ | 时间戳原样输出成 Unix timestamp |
| **layout_coherence** | 布局逻辑清晰吗？ | 层级混乱，信息密度失控 |

还有一个有意思的设计：**Human Corrections**。

你可以往 run workspace 里放一份 `corrections.json`，指定某个 fixture 的某个维度你觉得打分有偏差。Judge 会把你的 correction 纳入校准，让自动评分和人类判断保持对齐。

这就是 harness 飞轮的具体实现：人类对评分的修正，被系统化地 feed 回 judge，而不是一次性的口头反馈。

---

### S23 — 真实数据

[切到数据 slide]

来看一次真实的迭代。

**起点：整体评分 6.4/10**

Judge 告诉我们主要问题：
- `component_fit` 是最低分——很多场景下 agent 选错了组件类型
- `format_quality` 次之——日期和数字格式不一致
- 两个反复出现的 failing pattern

**Agent 看到 task-bundle，读了 summary.md 和截图，修了源码。**

**跑 verify：Score 6.4 → 7.8，+1.4，SUCCESS**

`component_fit` 从最差变成了进步最大的维度——agent 在看到"截图里用了卡片但数据应该是表格"这类视觉证据后，能做出正确的修正判断。

这就是 generator-evaluator 迭代的实际效果：有了可见的反馈，agent 能自我改进。

---

### Chapter 6 — 踩过的坑

---

### S24 — 三个最贵的坑

[切到踩坑 slide]

好，来讲我们实际踩过的坑。

**坑一：AGENTS.md 写太长，agent 反而乱跑。**

早期我们的 CLAUDE.md 把所有架构规则、命名规范、禁止事项全塞进去，几百行。结果 agent 的 context 被规则文档占满，回应里大量引用规则，做实际任务的空间反而少了。

修复：把 CLAUDE.md 瘦身为"指路地图"，详细规则拆到各自的 skill 文件里，按需加载。这是认知框架没做好——规则太多等于没有规则。

**坑二：eval-loop 没有退出条件，agent 无限重试。**

第一版没有设上限，让 agent 一直改到分数够为止。遇到某些结构性问题——不是调 prompt 能解决的，比如某个组件的渲染逻辑有 bug——agent 进入了"改→分数没变→继续改"的无止境循环。

修复：加了 `stalled` 状态检测——三次连续迭代没有提升，自动标记为需要人工介入。行为流程里必须有明确的退出条件。

**坑三：spec 写得太抽象，agent 无法执行。**

早期用 OpenSpec 写的 proposal 倾向于高层描述——"实现一个更好的表格组件"。结果 agent 交付的东西和我们脑子里想的差很远。

修复：proposal 里必须包含可测试的验收标准——"传入日期数据时，所有日期列必须使用 `FormatDate` 组件，格式为 YYYY-MM-DD"。有了可测试的标准，agent 才能自己验证自己有没有做好。

---

### S25 — 如果重来会怎么做

[切到反思 slide]

如果现在重新来，有三件事我会从第一天就做：

**第一：先建 eval，再建 feature。**

我们是先把框架做了一段时间，再补 eval-loop 的。早期有很多质量问题，等 eval 建好了才发现。如果从第一个 fixture 就有 judge 打分，很多问题能更早发现、更便宜地修复。

**第二：把 AGENTS.md 当代码来维护。**

早期当文档写了就不太管。结果很快就"腐烂"了，过时的规则、矛盾的规则开始积累。现在：每次 agent 翻车，归因完就更新 AGENTS.md，然后 commit，有 PR 记录。文档和代码用同一套变更管理流程。

**第三：Planner 和 Executor 从一开始就分开。**

我们花了一段时间才习惯"先写 spec，再让 agent 实现"这个工作流。早期经常直接告诉 agent "去做 XXX"，没有书面的 proposal。结果 agent 经常做出"技术上没错但方向偏了"的东西。

那句话太对了：**永远不要让 agent 在你审查和批准书面计划之前写代码。**

---

## 结尾

---

### S26 — 把话筒还给房间

[切到最后一张 slide，走到台前]

好，今天的内容到这里。

最后一句话——

> **"模型不是不够聪明，是我们还没搭好笼子。Harness 不是 prompt trick，是工程纪律。"**

我们给 agent 装上 skill，给它 spec 作为工作合同，给它 eval-loop 作为反馈回路——这些加在一起，就是我们在 OpenUI 上实践的 harness。它还在演化，肯定还有很多坑没踩完。

我想听听大家的想法——

**问题一：你们现在用 agent 最大的卡点在哪？是认知框架没写清楚、能力边界没限制，还是行为流程里缺了一个 evaluator？**

**问题二：我们团队的 harness 建设下一步应该重点投在哪？**

[开放 Q&A，让大家讨论]

---

## 附录：关键参考资料

- 李宏毅：[Harness Engineering 课堂视频](https://www.youtube.com/watch?v=R6fZR_9kmIw)
- 李宏毅：[AI Agent (1/3): Context Engineering 基本概念解说](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2450s)
- OpenAI：[Harness Engineering: Leveraging Codex in an Agent-First World](https://openai.com/index/harness-engineering/)
- Anthropic：[Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Birgitta Böckeler (Martin Fowler's site)：[Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
- LangChain：[The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
- 项目代码：[HoikanChan/openui](https://github.com/HoikanChan/openui)
