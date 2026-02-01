# Delta Sharing（Chapter 14）— 我的快速筆記彙整

## 1) 核心目的：不要再做資料複製/匯出
- 傳統做法：定期把 Delta table 匯出成另一份資料（JSON/Parquet/SFTP/email…）→ 會產生多份 truth、同步脆弱、成本高（ingress/egress + 重跑）
- Delta Sharing：讓接收者「直接讀來源的 live data / snapshot」，避免管理大量 export job 與狀態

---

## 2) 三個角色：Provider / Share / Recipient
### Provider（資料提供方）
- 擁有資料資產（schemas/tables/views…），負責建立分享與權限邊界

### Share（分享單位）
- Share 是「邏輯發布單位」：把可共享的資料資產組成一組
- 結構通常是樹狀：Share → Schemas → Tables/Views
- 重點：Share **不是把資料送出去**，而是定義「哪些資產可被讀」

### Recipient（接收者）
- Recipient 是一個 principal（可代表 user / team / BU / system）
- 用 **recipient profile file（JSON）** 取得存取資訊：
  - `endpoint`：Delta Sharing server URL（可能含 prefix/domain routing）
  - `bearerToken`：存取 token
  - `expirationTime`（可選）：到期時間
- 限制：不支援「群組內個別使用者」的細粒度權限差異；要差異化就要發不同 recipient profile

---

## 3) Delta Sharing Server（Sharing Service）在做什麼
- Sharing service 是實作 Delta Sharing Protocol 的服務（可為 Databricks 託管或 OSS reference implementation）
- 主要責任：
  1. Authenticate / Authorize：用 bearer token 驗證與授權
  2. Metadata broker：回傳 schema/table/view 的 metadata（含 properties、schema）
  3. Snapshot file access：提供讀取某個 table snapshot/version 所需的 **presigned file access**

---

## 4) REST API：底層協議的操作方式（通常由 client 封裝）
- REST 是 protocol 層的操作接口（多數情境用 client，不會手打 API）
- 常見 introspection API：
  - List shares：`GET {prefix}/shares`
  - Get share：`GET {prefix}/shares/{share}`
  - List schemas：`GET {prefix}/shares/{share}/schemas`
  - List tables：`GET {prefix}/shares/{share}/schemas/{schema}/tables`
  - List all tables：`GET {prefix}/shares/{share}/all-tables`
- 所有 API 都需要：
  - Header：`Authorization: Bearer {token}`
- Pagination：`maxResults` + `pageToken/nextPageToken`

---

## 5) Client 使用方式（Spark / SQL / 其他 connector）
### Spark / PySpark（概念）
- 安裝/引入 delta-sharing client（Python 套件 + Spark JAR）
- 用 profile file + `#<share>.<schema>.<table>` 組成 table_url
- 讀取方式像一般 DataFrameReader，只是 format 變成 `deltaSharing`

### Spark SQL extension（概念）
- 可用 SQL 建表指向 remote share table：
  - `CREATE TABLE ... USING deltaSharing LOCATION '<profile>#share.schema.table';`
- 後續就像查一般表：`SELECT * FROM ...`

### Streaming（概念）
- `readStream.format("deltaSharing") ...` 可讀 shared table 的增量版本（搭配 startingVersion 等）

---

## 6) 安全重點（我需要記住）
- bearer token 應該有到期與輪替（長效 token 是安全反模式）
- 建議提供 re-auth API/流程，讓外部 recipient 可重新取得 profile/token

---

## 7) 一句話總結（我自己的理解版）
Delta Sharing 用「Share（發佈清單）+ Recipient（token/profile）+ Sharing server（REST + metadata + presigned snapshot access）」讓外部或跨雲的計算平台能直接讀來源 Delta table，避免資料複製造成的同步、成本與多版本 truth 問題。