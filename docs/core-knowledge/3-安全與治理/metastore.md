Metastore 是什麼？（以 Unity Catalog 的語境）

在 Unity Catalog 裡，metastore =「最上層的治理容器」。它做的事情可以用一句話記住：

把你所有資料資產的「中繼資料（metadata）」跟「權限（permissions）」集中管理起來。

更具體一點，Unity Catalog metastore 會登記與管理：
	•	資料資產的中繼資料：例如 tables、volumes、external locations、shares…等（這些都被視為 Unity Catalog 的 securable objects）。 ￼
	•	存取控制與治理：誰能看到/用哪些物件、誰能建立 catalog / share / recipient 等頂層能力，都是在 metastore 這個層級被授權與管控。 ￼
	•	命名空間的頂層根：Unity Catalog 的三層命名空間 catalog.schema.table 是在「某個 metastore」底下成立的。 ￼
	•	區域（region）邏輯：官方文件也明確提到通常「每個 region 需要一個 metastore」。 ￼

你可以把它想成：
	•	沒有 metastore，就沒有 Unity Catalog 的治理「根」。
	•	Catalog / Schema / Table 都是掛在某個 metastore 底下被管理的。

⸻

這題為什麼問 metastore？

因為 Delta Sharing 的 share 物件本身是「contained within a Unity Catalog metastore」，而且「能不能建立 share」是 metastore 層級的權限。 ￼

⸻

題目：誰能 create & manage Delta Shares？（選 2）

正確答案通常是：
	•	✅ A. Users with CREATE SHARE privilege for the metastore
因為 CREATE SHARE 是「metastore 可授權的 privilege」，而且官方建立 share 的條件之一就是需要這個 privilege。 ￼
	•	✅ B. Metastore admins
Metastore admin 預設就包含 CREATE SHARE 等 metastore 層級能力，並且可以管理/轉移 metastore 內物件的權限與所有權（包含 share）。 ￼

⸻

為什麼不是其他選項？
	•	❌ D. Users with MANAGE privilege for the metastore
在官方的「metastore 可用 privilege 列表」裡，metastore 並沒有 MANAGE 這個 privilege 類型；metastore 是用一組明確的 CREATE ... / USE ... / SET SHARE PERMISSION 等權限定義。 ￼
	•	⚠️ C. Workspace admins
Workspace admin 是否「預設」有 CREATE SHARE 取決於你的 workspace 是否屬於 自動啟用 Unity Catalog 的情境；文件有提到某些情況 workspace admins 會被自動授權 CREATE SHARE，但這不是 workspace admin 的普遍必然權限。考題通常不會用這種「情境限定」當正解。 ￼
	•	⚠️ E. Account admins
Account admin 可以建立/連結 metastore、指派 metastore admin、啟用 Delta Sharing 等「平台層級」能力；但「建立 share」仍然是 metastore 內的 CREATE SHARE 權限範疇，並非所有 account admin 都必然能直接 create share（除非同時具備 metastore admin 或被授權）。 ￼

⸻

如果你願意，我也可以用一張「治理層級對照表」幫你把 Account admin / Metastore admin / Workspace admin / Object owner 在 Unity Catalog 的權限邊界一次釐清，考試會更穩。