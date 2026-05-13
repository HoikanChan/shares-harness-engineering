# Part 03: AI Agent 的構成與演進

所以我們今天學到是說
同樣的一個模型
你其實多加幾行指令
它的能力可能會有非常大的不同
所以今天當你發現你的 AI Agent
它的表現不如人意的時候
我們要改變它什麼地方呢
我們來回想一下
AI Agent 是由什麼東西組成的
AI Agent 裡面其實有兩個成分
一個成分就是 Large Language Model
它需要去呼叫一個 Large Language Model
這個 Large Language Model
它可以是 Claude
可以是 Gemini
可以是 GPT
它可能在雲端
也可能在地端
但除了 Large Language Model 以外
其實還有一系列的一堆程式
是在支援這個 AI Agent
去呼叫 Large Language Model
有一大堆的框架
讓這個 AI Agent
可以呼叫 Large Language Model
包括 OpenClaw
或 Claude
或者是 Cursor
還有更多各式各樣
如雨後春筍般出現的 AI Agent
做的都是這樣的事情
所以一個 AI Agent 裡面
其實有兩部分
一部分是 Large Language Model
另外一部分就是其他的東西
過去那些其他的東西
沒有好的名字
現在這些其他的東西
有了一個共同的名字
叫做 Harness
如果你不認識這個英文單字的話
它的意思是馬具
如果你覺得叫馬具不夠好聽的話
也許很多人會把 Harness 直接翻成駕馭
現在打造 Harness 這件事情
叫做 Harness Engineering
翻成中文
很多人會翻成駕馭工程
那這個 Harness 這個詞彙有很常用嗎
它真的非常常被使用
比如說如果你是 Claude 的訂閱用戶的話
你可能在清明連假的時間
收到了這樣一封信
那個 Claude 告訴你說
以後這個 Claude 的訂閱帳號
不再支援第三方的 Harness
舉例來說 OpenClaw
你知道 OpenClaw 就是一種 Harness
那如果不知道這是什麼意思的同學呢
也許可以再稍微解釋一下
其實一般你在使用這個大型語言模型的時候
有兩種付費的方式
一種是用多少付多少
你就是呼叫它的 API
然後你給它多少 Token
它吐出多少 Token
那就算你多少錢
那其實還有另外一種付費方式
是吃到飽的方式
你可以去訂閱一個帳號
你可以做訂閱
那你就是付一個月費
那照理說你付了那個月費之後
在那個月裡面
你是可以無限次數地呼叫語言模型
那過去呢
語言模型的服務商覺得
給你月費制是沒有問題的
要讓你吃到飽是沒有問題的
你畢竟是個人類
你能夠輸入多少指令呢
但現在有了 OpenClaw 這種神器
它可以有心跳機制
可以每隔幾分鐘就送一次指令
所以這些服務商就覺得吃不消了
所以他們覺得
所以像 Claude 就決定說
以後像 OpenClaw 這種
Harness 不可以再去接 Claude 的語言模型
你不可以在這個 OpenClaw 上面
去接 Claude 的語言模型
我說這一段
只是想要告訴大家說
OpenClaw
現在大家認知
它是一種 Harness
如果你現在是用 OpenClaw 來呼叫 Claude 的話
你就要付額外的錢了
如果你不想要這樣做的話
等一下告訴你有什麼樣
其他的簡單的處理方法
所以一個 AI Agent
還有兩部分
一個是語言模型
一個是它的 Harness
所以如果你要強化
AI Agent 的能力
讓它變成
你想要的樣子
也許一方面
你可以去改你的語言模型
你可以自己訓練一個
更好的模型
你可以微調一個
現成的模型
那怎麼訓練語言模型
怎麼微調一個
現成的模型
在過去的課程裡面
已經講得非常多了
在這門機器學習
導論這門課第七講
完整地講了一個大型語言模型
是怎麼被訓練出來的
第八講講說怎麼微調
怎麼調整一個現成模型的參數
這部分大家可以再回去
自己先預習一下
從我們本週開始的作業
是跟微調模型有關的
所以這些內容對你應該是蠻有幫助的
但是另外一方面
這個 AI Agent
還有非常重要的一部分
就是它的 Harness
所以打造一個更好的 Harness
同時你也能夠強化
AI Agent 的能力
讓它變成你要的樣子
打造 Harness 這件事情
現在是一個很熱門的主題
各大公司的 blog
都一直在講說
他們是怎麼打造他們的 Harness
比如說去年 11 月
Anthropic 就發了一篇文章
講說他們有什麼樣有效的 Harness
可以讓 agent 長時間的運作
OpenAI 在 2 月的時候
也發表了一篇文章
叫做 Harness 工程
在三月的時候
Anthropic 又發了另外一篇文章
叫 Harness Design
所以現在 Harness Engineering
或 Harness Design
變成一個非常熱門的詞彙
象徵的意涵就是
AI 是一匹馬
它有很強大的力量
但是你要駕馭它
你還是需要一些馬具
你需要馬鞍
你需要韁繩
那這些馬鞍韁繩
就是 Harness
好，那像這樣子熱門的詞彙
我們過去也看過很多
今天當人們想要認真
做一件事情的時候
就在某個詞彙後面
加上 engineer，告訴你說
我們準備要在意這件事了
所以過去先有 Prompt Engineer
後來又有 Context Engineer
現在有 Harness Engineer
那這三者有什麼樣的差異呢
其實這三者有非常多重疊的地方
但是它們想要強調的核心價值
是有不同的
所謂 Prompt Engineering 的意思就是
我們都知道 Large Language Model
就是在做文字接龍
所以你給它不同的輸入
它接出來的東西就不一樣
過去語言模型的能力比較弱
所以你往往同樣的問題
換一個問法
它給你的答案可能會天差地遠
所以那時候就有很多人在研究
怎麼樣下 prompt
可以改變模型的輸出
那最知名的強化語言模型能力的咒語
就是 think step by step
那其實我在 2024 年的課程
就已經有講過說
像這種咒語啊
未來會越來越沒有用
因為怎麼可以叫模型
think step by step
才 think step by step 呢
今天沒有叫你 think step by step
也要給我好好地思考
所以現在這些模型
就算你沒有強調叫它思考
它其實也會發揮它的全力
也會認真思考
有沒有這些咒語的差異呢
其實就越來越小
好，那咒語越來越沒有用以後
人們發現這些語言模型的極限
也許來自於有一些資訊
它就是不知道
所以今天它之所以
沒有給你正確的答案
不是它能力不行
而是今天在做文字接龍的時候
根據這個 prompt
就是沒有足夠的資訊
接出正確的答案
為了讓語言模型
有足夠的資訊
可以接龍接出正確的答案
所以就有了
Context Engineering 的概念
所以會想像說
我們今天要給語言模型的資訊
有很多語言模型
要解一個任務
需要非常多的資訊
然後你有一個
Context Engineering 的系統
它會尋找合適的 context
組成 prompt
然後丟給 Large Language Model
所以你也許也可以說
Context Engineering
是一個更有系統的
自動化的
做 Prompt Engineering 的方式
