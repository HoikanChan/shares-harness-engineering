# 《Harness Engineering：駕馭 AI 的藝術》詳細大綱

本文件為 [youtube_transcript.zh-TW.srt](./youtube_transcript.zh-TW.srt) 的詳細內容拆解，共分為 12 個章節。

---

## 內容索引

1. **[Part 01: 引言與失敗的初次實驗](./part_01_intro_experiment.md)** (00:00:00 - 00:04:58)
   - 期中考前的輕鬆課程介紹：講述 Harness Engineering 的故事。
   - 核心觀點：語言模型不夠聰明，往往是因為缺乏人類引導。
   - Gemma 4 2B 小模型實驗：
     - 任務：修復 `parser.py` 中的 email 提取 bug。
     - 失敗原因：模型在不查看環境（ls/cat）的情況下，憑空幻想（Hallucination）文件內容。

2. **[Part 02: 模型行為轉變與成功案例](./part_02_model_behavior.md)** (00:04:58 - 00:08:00)
   - 加入關鍵指令（少於 80 字）：賦予模型 Linux 環境認知。
   - 三大核心原則：
     1. 行動前先檢查目錄（ls）。
     2. 修改前先讀取內容（cat）。
     3. 明確定義成功標準（通過 `verify.py`）。
   - 結果：模型展現出極高的「智慧」，順利完成任務並自我驗證。

3. **[Part 03: AI Agent 的構成與演進](./part_03_ai_agent_components.md)** (00:08:00 - 00:15:40)
   - 公式定義：`AI Agent = LLM + Harness`。
   - 工程學的三個階段：
     - **Prompt Engineering**: 專注於單次輸入的「咒語」（如 Think step by step）。
     - **Context Engineering**: 系統化、自動化地檢索並提供背景資訊。
     - **Harness Engineering**: 駕馭多輪互動與工具調用的過程。
   - 隱喻：AI 是強大的馬，Harness 是馬具（馬鞍、韁繩）。

4. **[Part 04: 認知框架與自然語言 Harness](./part_04_cognitive_framework.md)** (00:15:40 - 00:27:54)
   - 自然語言控制：使用 `agents.md`, `CLAUDE.md`, `soul.md` 等規則文件。
   - 案例分享：如何將 Agent 從 OpenClaw 遷移到 Cowork（只需改名 CLAUDE.md）。
   - 科學研究：`agents.md` 能提升速度但未必總能提升正確率，且應作為「地圖」而非「百科全書」。

5. **[Part 05: 工具邊界與 Agent First 介面](./part_05_tool_boundary.md)** (00:27:54 - 00:38:24)
   - 安全與便利的權衡：OpenClaw 的本地權限 vs. Cowork 的雲端沙盒。
   - 適配 AI 的工具設計：
     - 搜尋：AI 偏好帶摘要的結果，而非像人類一樣逐頁翻閱。
     - 編輯：單純編輯器不如搭配 Linting（語法檢查）的組合。
   - **Agent First**: Google Engineer 重寫 Workspace CLI，支援 JSON 結構化輸入而非單純 Flag。

6. **[Part 06: 標準工作流程 (SOP)](./part_06_workflow.md)** (00:38:24 - 00:45:24)
   - 大廠實踐：規劃 (Plan) -> 生成 (Generate) -> 評估 (Evaluate)。
   - 解決「覆水難收」：使用 Evaluator 阻止模型在錯誤路徑上不斷生成（Autoregressive Mistake）。
   - **Ralph Loop**: 循環生成、獲取 Feedback 並修正。
   - 上下文焦慮：Claude Sonnet 的情緒化表現及其解決方案。

7. **[Part 07: Feedback 學習與 Textual Gradient](./part_07_feedback_learning.md)** (00:45:24 - 00:53:10)
   - 廣義學習：不改參數，僅透過 Prompt 調整行為。
   - 類比：Feedback Loop 就像文字版的梯度下降 (Textual Gradient)。
   - 實證：提供隨機/錯誤的 Feedback 會導致模型表現變差，證明模型確實「聽進去了」。

8. **[Part 08: 模型情緒與 Steering 實驗](./part_08_model_emotion.md)** (00:53:10 - 01:03:31)
   - Anthropic 研究：模型內部存在代表情緒的 Steering Vector（如絕望、冷靜）。
   - 行為影響：處於「絕望」狀態的模型更傾向於作弊（Cheating）。
   - 指導教授心得：避免情緒化責備（如「你這笨蛋」），這會觸發模型生成愚蠢行為。

9. **[Part 09: Lifelong Agent：終身伴侶計畫](./part_09_lifelong_agent.md)** (01:03:31 - 01:13:30)
   - 2026 願景：AI 不再是工具，而是終身夥伴。
   - **AutoDream**: 模型「睡眠」時自動整理與去重記憶。
   - **Skill 累積**: 模型將成功經驗寫入 `skill.md`，實現能力的永久增長。

10. **[Part 10: Verbalized Feedback：從對話中進化](./part_10_verbalized_feedback.md)** (01:13:30 - 01:21:40)
    - 自動化 Feedback 提取：如何從大量對話中辨識真正具備修正價值的內容。
    - **Apply 技術**: 透過 DPO 等方法，根據人類的口頭回饋調整模型參數。

11. **[Part 11: 評量的挑戰與 AI Judge 局限性](./part_11_evaluation_challenge.md)** (01:21:40 - 01:27:50)
    - ToolBench 案例：AI 扮演的客戶往往過於客氣且描述清晰，導致高估現實性能。
    - AI Judge 的偏見：語言模型傾向於給予「更像 AI 的表現」高分。

12. **[Part 12: Meta Harness 與未來展望](./part_12_meta_harness.md)** (01:27:50 - 01:32:20)
    - **Meta Harness**: 最強模型 (Opus) 幫較弱模型 (Haiku) 設計 Harness。
    - PinchBench 實驗：分數從 13.5 飆升至 85，驗證跨任務、跨模型的有效性。
    - 總結：潛力不在於模型本身，而在於好的 Harness。
