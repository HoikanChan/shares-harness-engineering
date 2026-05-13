# Part 06: 標準工作流程 (SOP)

那接下來我們來講
用標準工作流程來控制行為
那今天這些大公司的 blog 都講了很多
他們怎麼訂這些 AI 員工的標準工作流程
比如說在 Anthropic 的這個 harness design 這邊 paper 裡面
他們就特別提到說
他們的工作流程是規劃、生成然後評估
當人類提供個指令的時候
這個 AI 先扮演一個 planner
那這個 planner 的工作
是把人類的指令
拆解成一些比較小的項目
那每一個小的項目
再去交給一個 generator 來執行
那 generator 執行完之後呢
會去丟給一個 evaluator
那 evaluator 去 evaluate generator
做得怎麼樣
因為今天很多時候呢
AI 它不一定能夠生成出正確的結果
但是它能夠檢查
自己產生的結果
是不是正確的
其實很多時候人類也是啊
今天假設叫你
從頭到尾寫一個程式
回頭都不能再改
你要完全沒有語法錯誤
其實也不一定能夠做得到
尤其是假設
你不能從頭再改的情況下
今天 AI agent 在輸出的時候
它就是一路
autoregressive 生成下去
就算前面有錯
它也沒辦法回頭再改
在這種情況下
它是非常容易犯錯的
所以很多時候
它就算知道自己犯錯
但是因為
它就是 autoregressive 的生成
所以它覆水難收
只能夠不斷地錯下去
所以這個時候
需要有一個 evaluator
那這個其實 evaluator
背後呼叫模型
甚至可能就是同一個
但是來檢查 generator 有沒有犯錯
讓 generator 可以停下來
審視自己的錯誤
那另外在他們這邊 blog 裡面
還提到了一個有趣的工作流程是
他們不完全是讓 generator
在做完工作以後
evaluator 再來評價
因為他們怕 generator 做完之後
跟 evaluator 做的想像的不一樣
這樣 generator 還要重做太麻煩了
所以他們讓 generator 跟 evaluator
在開始工作之前
就先訂好一個 contract
這一開始 generator 會提供個提案給 evaluator
看 evaluator 接不接受
evaluator 接受這個提案之後
generator 才開始工作
這樣確保 generator 做的事情
跟最後 evaluator 審查的標準
會是比較一致的
那他們就會把不同的小項目
都用 generator 跟 evaluator
兩者合作的方式來完成
這樣就可以讓 AI
共同完成一個大的項目
那這個就是用標準工作流程
來控制行為的一個例子
當然這並不代表
這一定是最好的工作流程
但是今天規劃、生成、評估
這樣子三個 agent
共同合作的模式
好像是今天非常常看到的一種模式
那這邊又舉另外一個例子
這個例子是來自 DeepMind 的 blog
那他們就分享說呢
他們怎麼打造 AI 的科學家
那他們的 AI 科學家的工作流程
其實跟剛才我講的
Anthropic 的工作流程
其實也非常像
他們裡面有一個 generator
有一個 verifier
這個 verifier 就是前頁投影片的 evaluator
所以有一個任務進來
generator 先做一些
想一些可能的 solution
然後交給 verifier
如果 verifier 覺得說
這些 solution 都太爛了
它就回去叫 generator 從頭開始做
如果它覺得這些 solution 還好
它會再呼叫另外一個模組
會再進入另外一個工作流程
叫做 revisor
就只是微調原有的方案而已
所以看起來先做事
然後再驗證
是一個非常常見的工作流程
那在這個 Anthropic 跟 OpenAI 的 blog 裡面
都提到了一個東西叫做 Ralph Loop
Ralph 是辛普森家族裡面一個角色的名字
然後這個角色
它的特色就是橫衝直撞
就一路向前
所以這邊 Ralph Loop 的意思就是
讓語言模型不斷地做下去
然後有錯再改
所以你給語言模型一個任務
然後它先產生第一個版本的輸出
但這邊重點是語言模型的輸出
需要得到回饋
也就是剛才的 generator 跟 evaluator 的概念
所以你把語言模型的輸出
丟給某一個負責做 evaluation 的 module
讓它產生 feedback
那這個 evaluation 的 module
不一定要是一個語言模型
它可以甚至就是一個 compiler
或者是一個可以執行程式碼的工具
把程式碼真的執行了
看看得到什麼樣的
error message
那這個 error message
就是給 Language Model 的 feedback
好 那這個 feedback 呢
再丟給語言模型
然後呢
語言模型就再產生
第二個版本的程式碼
然後第二個版本程式碼
再被 evaluate
得到第二個版本的 feedback
這樣的過程呢
就反覆持續下去
直到語言模型做對為止
那這個就是 Ralph Loop
那這樣 Ralph Loop 的好處是說
對語言模型來講啊
產生東西是非常快的
所以你不用吝惜語言模型
把一件事情重做
因為對它來說
重做一件事情
產生一段程式
是一件容易的事情
但是如果有時候用 Ralph Loop
一路產生 feedback
產生 feedback 下去
很快就會到達
語言模型 context window 的上限
所以另外一個常見的
使用的操作方法
所以在 Ralph Loop 裡面
一個常見的手法就是
每次語言模型產生
一個輸出
一次 feedback 之後
把這些輸出跟 feedback 做摘要
然後在下一輪開始的時候
就只使用上一輪摘要的內容
而不把全部的內容
都丟到下一輪裡面去
所以 LLM 就可以節省
它的 context window
比較有可能產生成功的結果
不過其實不同的語言模型
適合不同的 harness
在 Anthropic 的 blog 裡面
他們就有提到說
這個需要 summary
再進入下一個回合的
這樣子的 harness
這樣子的工作流程
比較適合 Claude Sonnet
因為他們說 Claude Sonnet
有上下文焦慮
那這是一個很擬人化的講法
他們說 Sonnet 這個模型
當它發現
它的 context window
快用盡的時候
它就展現出一種焦慮的情緒
它就開始發瘋
事情亂做
想要盡快結束手上的工作
所以你需要用這樣子的工作流程
來確保它現在的輸入
不會太接近它的 context window
但是後來 Claude 有了比較強的模型
就是 Opus
他們就說如果是 Opus 的話
他們就可以把上面這種工作流程丟掉
可以一路忙下去
一路做下去
所以其實 harness
並不是一個固定不變的東西
它其實需要根據你的語言模型
來重新設計
所以你不應該說
我有一個萬用的 harness
它對所有語言模型都是能夠派上用場的
它應該是一個可以拆解組裝的東西
隨著語言模型的能力改變
你可以拿掉不同的部件
或者是裝上額外的部件
