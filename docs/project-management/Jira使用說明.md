# 📘 Jira 使用說明：Epic / Story / Task / Sub-task

## 📌 文章簡介

本篇文章旨在說明 Jira 中不同 **Issue 類型（Epic、Story、Task、Sub-task）** 的用途與適用情境，並提供清楚的分類邏輯與範例，幫助團隊建立一致的任務拆解與追蹤方式。

對於第一次接觸這些名詞的讀者，可以簡單理解為：

- **Epic**：一個大型目標或專案主題，像是一個「章節」。
- **Story**：代表使用者可感知的功能需求，可驗收與 demo。
- **Task**：技術性或支援性的工作，通常不是使用者導向。
- **Sub-task**：Story 或 Task 內部的具體步驟或小任務。

本文特別針對 **「不同專案共用同一 Epic」** 的情境進行說明，是針對多人協作與大型專案管理時的實用參考。

## 🏗️ Jira 階層結構

Jira 的常見階層如下：

```text
Epic
├── Story 1（具體可交付的功能）
│   ├── Sub-task 1.1（完成該功能的步驟）
│   └── Sub-task 1.2
├── Story 2
│   └── Sub-task 2.1
├── Task 1（技術性/支援性工作）
│   ├── Sub-task T1.1 （拆解後的具體工作項）
│   └── Sub-task T1.2
```

> 📌 **注意：**
>
> - Story 與 Task 屬於同一層級
> - Sub-task 必須隸屬於某個 Story 或 Task
> - Epic 為頂層主題（目前專案僅允許一個）

## 📋 Jira 任務類型對照表

| 類型       | 用途說明 | 適合範例 | 是否可拆成 Sub-task |
|------------|----------|----------|----------------------|
| **Epic**   | 一個大目標或專案主題 | 整個 API 專案、年度重構計畫 | ❌ |
| **Story**  | 使用者導向的功能需求，可驗收、可 demo | 查詢報表、上傳附件 | ✅ |
| **Task**   | 技術性、支援性或跨 Story 的任務 | 架 staging 環境、資料庫設計 | ✅ |
| **Sub-task** | Story 或 Task 下的小任務 | API 撰寫、文件整理 | ❌ |

## 🎯 Story、Task 與 Sub-task 的判斷邏輯

| 判斷問題 | 判斷條件 | 對應類型 |
|----------|----------|----------|
| 這個工作是否對應某個使用者功能？ | ✅ 有 → Story ❌ 沒有 → Task | Story / Task |
| 這件事能不能 demo 給業主看？ | ✅ 能 demo → Story ❌ 不能 demo → Task | Story / Task |
| 這項工作是「為了完成一個功能」還是「為了支援整個專案」？ | ✅ 單一功能 → Sub-task ✅ 整個專案 → Task | Sub-task / Task |
| 是否具有可交付與可驗收的成果？ | ✅ 有 → Story ❌ 沒有 → Task（通常需附文件或成果圖） | Story / Task |

## 🧩 常見工作類型歸類

| 工作項目                    | 建議類型 |
|-----------------------------|----------|
| 使用者可以查詢資料           | Story    |
| 開發查詢 API               | Sub-task（屬於 Story） |
| 設計整體系統架構             | Task     |
| 畫系統流程圖               | Sub-task（屬於設計 Task） |
| 搭建 staging 環境           | Task     |
| 整理需求文件（含與 PM 討論） | Task     |
| 定義資料欄位或規格書         | Sub-task 或 Task |
| 自動化測試框架建置           | Task     |
| 撰寫 API 文件               | Sub-task 或 Task |
| 上傳功能頁面 UI             | Sub-task（屬於 Story） |

## 🛠️ 額外小技巧（讓任務管理更清晰）

- 🔖 **命名建議**：Task 前面可加前綴，如 `[設計]`、`[環境]`、`[需求]`，讓大家一看就知道屬性。
- 🏷️ **使用 Labels or Components**：可以標記模組、子專案、系統名稱。
- 🔗 **善用 Issue Link**：可以建立「blocks / is blocked by / relates to」等關係，補足層級不足。

## 📌 使用範例（針對內部 API 開發）

```text
Epic：新一代用戶資料平台

├── Task：[需求] 使用者查詢 API 分析
│   ├── Sub-task：使用情境訪談
│   ├── Sub-task：欄位規劃
│   └── Sub-task：API Spec 撰寫
├── Task：[設計] 系統架構規劃
│   ├── Sub-task：模組切分
│   └── Sub-task：資料流設計
├── Story：使用者可以查詢個人資料
│   ├── Sub-task：實作後端 API
│   ├── Sub-task：前端畫面整合
│   └── Sub-task：單元測試與驗收
├── Task：[環境] 部署到 Staging
│   ├── Sub-task：建立環境設定
│   └── Sub-task：服務驗證
```
