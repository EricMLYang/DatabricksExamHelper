7.數據共享 (5%): [數據共享與聯邦 (5%)]

4.數據共享與聯邦（Data Sharing and Federation，5%）

探討在不同系統或團隊之間分享資料。

包括 Databricks 工作區彼此之間，以及與外部系統共享資料的技術。

評估是否懂得利用 Delta Sharing 等機制，安全地提供資料，同時保持對資料的控制。

涉及「資料聯邦」的概念，即在多系統間聯合查詢或統一管理資料。

範圍：

涵蓋 Databricks 的 Delta Sharing 功能和 Lakehouse Federation 等主題。

Delta Sharing 分為兩種模式：

Databricks-to-Databricks (D2D) 資料分享

對外部平台的開放分享 (D2O)

如何設定一個 Delta 分享，使某個資料表可以被另一個工作區存取，或被外部使用者（無需 Databricks 環境）讀取。

Lakehouse Federation，例如如何將不同資料來源（可能是多雲或異質系統）的資料在 Databricks 統一起來查詢，同時遵守治理規範。

題目重點在安全、治理完善的前提下實現資料的可分享與跨系統整合。

需要的知識：

理解 Delta Sharing 的基本原理與設定方式，例如建立分享（Share）、寫入者與讀者的權限控制，以及分享資料時的協議（Delta Sharing 使用的開放協議）。

瞭解透過 Unity Catalog 來管理分享的資料集，確保只有授權對象才能讀取分享的資料。

Federation，要知道 Unity Catalog 能夠聯邦查詢外部系統的哪些種類資料源，以及設定這類聯邦連接時需要的權限和設定（如在 Unity Catalog 中建立 External Location 或外部資料庫物件）。

準備方式：

閱讀 官方文件 Delta Sharing 章節，理解設定流程：包括在提供方工作區中啟用分享、生成共享連結或令牌，並在接收方透過共享連結設定外部表讀取 Delta 資料的步驟。

實際演練在兩個 Databricks 工作區之間分享一個 Delta Lake 資料表。

對於 Federation，了解 Databricks Unity Catalog 最近推出的聯邦查詢功能（例如查詢外部資料庫或資料湖的資料），並了解其限制。

考試注意事項：

安全性和操作步驟。

例如，「如何在不導出資料檔案的情況下，讓外部合作夥伴及時存取你的Lakehouse資料」

正確答案應該涉及 Delta Sharing，而不是叫你把資料導出到第三方存儲。

也可能問 Delta Sharing 的授權架構，例如只能讀的共享如何設定。

對於 Federation，若題目提到將外部資料納管至 Unity Catalog，要聯想到 External Location、External Table 等概念。