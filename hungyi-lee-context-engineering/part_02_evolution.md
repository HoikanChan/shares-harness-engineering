# Part 02: 從 Prompt 到 Context Engineering

我們過去常聽到一個詞叫做 Prompt Engineering
也就是提示工程，很多人戲稱為「咒語」
在語言模型能力還沒那麼強的時候
你加一句 "Let's think step by step" 模型就突然變聰明了
但如果你有在關注最新的模型，你會發現這些咒語的效果正在減弱
因為今天的模型，你不叫它認真思考，它也會發揮全力
那「咒語」失效之後，我們接下來要面對的是什麼？
那就是 **Context Engineering (上下文工程)**
它不再只是改一句話，而是管理整個輸入給模型的「脈絡」

Context Engineering 更像是一張「施工藍圖」
它決定了在每一輪的對話中，模型應該看到什麼
我們可以把 Context 拆解成幾個組成要素：
1. **System Prompt**：規範角色的性格、底線，這部分現在越來越長
2. **User Input**：使用者的具體需求
3. **Dialogue History**：短期的對話紀錄
4. **Memory**：從長期記憶庫中檢索出來的相關資訊
5. **RAG (External Info)**：外部工具搜尋到的資料
6. **Tool Output**：工具執行的結果
7. **Reasoning**：模型內部的推理過程

這就是為什麼我們說 Context Engineering 是更有系統的設計
它要解決的是模型「活在當下」的問題
語言模型本質上是無狀態的 (Stateless)
它之所以能進行多輪對話，是因為我們在背後偷偷把之前的對話都傳回去了
而如何優雅地管理這些不斷增長的資訊，就是這堂課的核心
