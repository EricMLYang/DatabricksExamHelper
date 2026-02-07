# Unity Catalog MANAGE 權限 速記

## 一句話
**MANAGE = 權限管理委派**，但不自動擁有所有權限；可自行授權取得需要的權限。

---

## MANAGE 能做什麼（更精準）
- ✅ view & manage privileges（GRANT/REVOKE）
- ✅ transfer ownership
- ✅ drop / rename / edit（依物件支援範圍）

> MANAGE 類似 ownership 的管理能力，但不等於自動擁有所有 privilege。

---

## 考試用安全句型
- **MANAGE 不會自動包含資料存取權限**（如 SELECT）
- **但可自行授權**（因此實務上可取得存取能力）

---

## Catalog 權限管理的關鍵條件
要管理 catalog 的 privileges，通常需要：
- **catalog owner** / **metastore admin**
- 或同時擁有 **MANAGE + USE CATALOG**

常見做法：
```sql
GRANT USE CATALOG ON CATALOG hr_catalog TO hr_team;
GRANT MANAGE ON CATALOG hr_catalog TO hr_team;
```

---

## MANAGE vs ALL PRIVILEGES vs OWNERSHIP
| 權限 | 說明 |
|---|---|
| **MANAGE** | 可管理/授權/轉移 ownership/刪除/改名（依物件），但不自動包含所有權限 |
| **ALL PRIVILEGES** | 不含 MANAGE（避免 privilege escalation） |
| **OWNERSHIP** | 完整控制（含管理、授權、轉移 ownership） |

---

## 口訣
```
MANAGE = 管理權限，但不是全部權限
ALL PRIVILEGES ≠ MANAGE
Owner 才是全控
```
