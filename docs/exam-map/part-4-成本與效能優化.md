4. 成本與效能優化 (13%): [成本與性能優化 (13%)]

6.成本與性能優化（Cost & Performance Optimisation，13%）

考核優化資源使用與提升系統性能的能力。

就是如何用較低的成本，讓資料處理管道跑得更快、更順。

包括瞭解各種優化功能，以及在架構上作出明智的設計來避免浪費資源。

範圍：

涵蓋資料存儲和查詢的多種優化技巧。

瞭解使用 Unity Catalog 管理表能簡化維護並降低操作負擔

掌握 Delta Lake 的優化功能，

如 刪除向量（Deletion Vectors）， Liquid Clustering，以及這些技術如何改善小檔案過多或資料傾斜等問題

考題也會涉及查詢性能提升方法，包括 資料略過（Data Skipping）、檔案裁剪（File Pruning）如何在併行讀取時加速，以及何時應該使用 Z-Order 或分區等技巧。

另一重點是串流表的限制與改進：例如使用 Change Data Feed (CDF) 來解決串流表的一些限制，提高低延遲處理的能力

監控與調校查詢也是範圍之一，如使用 查詢分析工具找出執行瓶頸（例如資料傾斜、不良Join策略）

需要的知識：

熟悉 Delta Lake 優化相關指令與概念，例如 OPTIMIZE 如何併合小檔案、ZORDER BY 如何重新排序資料以提升篩選效率。

了解 Liquid Clustering 概念，Delta Lake 新推出的功能，用於自動動態地整理資料分佈，較傳統分區更省力，同時保有查詢效率

知道何時該採用分區 (Partitioning) 或 Z-Ordering，以及 Z-Order 與 Liquid Clustering 的比較（例如 Liquid Clustering 可以視為自動且細粒度的分區，減少人工調整）。

理解 Deletion Vectors 用於標記被刪除的資料而不立即重寫檔案，從而改善寫入小檔案過多的情況。

了解 Spark 查詢的常見瓶頸，例如 Shuffle 過多會導致延遲，如何透過調整並行度或避免過大的join來改善。

成本方面，應知曉 叢集設定對成本的影響：如自動終止閒置叢集、選擇適當的節點類型，以及在可能情況下使用 Databricks Serverless 或 光載波（Photon） 引擎來兼顧效能與成本。

準備方式：

在一個測試環境中實驗 Delta Lake 優化功能。

比如，建立一個包含數千小檔案的 Delta 資料夾，執行 OPTIMIZE 前後對比查詢速度。

試用 Z-Ordering：在一個大型資料表上對常查詢的欄位做 ZORDER，觀察檔案裁剪效果

研究 Liquid Clustering 的設定和效果（可透過 Databricks 官方博客或說明取得模擬）。

練習使用 Spark 的 EXPLAIN 或 Query Profile 來解析查詢計畫，找出是否有 Shuffle 或 Broadcast 提示，並思考如何改寫程式碼優化。

也嘗試調整叢集的大小和類型，觀察在成本與速度上的折衷。

考試注意事項：

題目可能以場景敘述，例如：「某分析查詢非常慢」或「管道成本高昂」，然後詢問最佳改進措施。要能針對不同原因給出相應優化：如果是小檔案過多，想到 OPTIMIZE；如果是查詢沒有利用分區，想到需要分區欄位或 ZORDER；如果是即時串流延遲，可能答案涉及使用 CDF 或提高Trigger頻率等。注意 Delta Lake 新舊功能的術語：選項中可能出現Liquid Clustering、Deletion Vectors等較新概念，須知其作用。對成本優化，也留意資源自動化管理（如自動縮放、叢集關閉）是否是選項之一。