# 《Context Engineering：AI Agent 背後的關鍵技術》詳細大綱

本文件為 [AI Agent (1/3)：核心技術 Context Engineering 基本概念解說](https://www.youtube.com/watch?v=urwDLyNa9FU) 的內容拆解，共分為 12 個章節。

---

## 內容索引

1. **[Part 01: 引言與 AI Agent 的基本定義](./part_01_intro.md)** (00:00:00 - 00:08:00)
   - 課程大綱：Context Engineering、Agent 互動、工作衝擊。
   - 核心公式：Goal -> Action -> Observation 的循環。
   - AI Agent 的定義：從「給予指令」到「給予目標」。

2. **[Part 02: 從 Prompt 到 Context Engineering](./part_02_evolution.md)** (00:08:00 - 00:16:00)
   - 演進過程：Prompt Engineering (咒語) -> Context Engineering (施工藍圖)。
   - 為什麼咒語逐漸失效？模型能力的內化與全力思考。
   - Context 的七大組成要素。

3. **[Part 03: 記憶管理的核心模組](./part_03_memory_modules.md)** (00:16:00 - 00:24:00)
   - 模組化記憶：Read (檢索)、Write (判斷)、Reflection (反思)。
   - 解決「活在當下」的問題：模型本身是無狀態的 (Stateless)。

4. **[Part 04: 工具呼叫與 Function Calling](./part_04_tool_use.md)** (00:24:00 - 00:32:00)
   - AI 如何使用工具：輸出結構化文字 (JSON) 並轉譯為行動。
   - 判斷力：模型如何處理內部知識與外部資訊的衝突。

5. **[Part 05: 上下文視窗與「超憶症」比喻](./part_05_hyperthymesia.md)** (00:32:00 - 00:40:00)
   - Context Window 的限制與算力成本。
   - 超憶症隱喻：過多無效細節反而阻礙決策與抽象思考。

6. **[Part 06: 主動壓縮與 Subagent 隔離](./part_06_proactive_compression.md)** (00:40:00 - 00:48:00)
   - 讓模型主動判斷何時壓縮。
   - Subagent 作為壓縮手段：隱藏繁瑣細節，僅回傳最終結果。

7. **[Part 07: Context Collapse 與 ACON 論文](./part_07_acon_paper.md)** (00:48:00 - 00:56:00)
   - 壓縮的代價：Context Collapse（關鍵指令的遺失）。
   - ACON 技術：利用反饋機制優化摘要品質。

8. **[Part 08: 強化學習優化摘要 (SUPO)](./part_08_supo_paper.md)** (00:56:00 - 01:04:00)
   - 當沒有標準答案時：利用 RL 訓練摘要模型。
   - 讓模型在解題過程中學會「挑選重點」。

9. **[Part 09: 觀察遮蓋 (Observation Masking)](./part_09_masking.md)** (01:04:00 - 01:12:00)
   - Token 分佈分析：Observation 佔據了 84% 的流量。
   - 透過佔位符與過濾技術減少 Token 消耗。

10. **[Part 10: Multi-Agent 與 Context 隔離](./part_10_multi_agent.md)** (01:12:00 - 01:20:00)
    - 解決單一 Agent 的過載問題。
    - 透過分工實現資訊隔離，保持主模型的 Context 乾淨。

11. **[Part 11: 評量的挑戰與 AI Judge 偏見](./part_11_evaluation.md)** (01:20:00 - 01:28:00)
    - ToolBench 案例：AI 客戶過於客氣導致性能高估。
    - AI Judge 的偏見：傾向給予「更像 AI 的表現」高分。

12. **[Part 12: 總結與未來展望](./part_12_conclusion.md)** (01:28:00 - 01:32:20)
    - Context Engineering 就是新的開發範式。
    - 展望：AI 不再是工具，而是具備長期演進能力的夥伴。
