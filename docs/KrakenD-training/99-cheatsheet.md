# KrakenD 入門速查表

## 基本名詞速查

| 名詞 | 白話說明 | 常見位置 |
| --- | --- | --- |
| `krakend.json` | KrakenD 主要設定檔 | 專案根目錄或 `/etc/krakend/` |
| `version` | 設定檔格式版本 | root |
| `endpoint` | 對外提供給 client 呼叫的 API 路徑 | `endpoints[]` |
| `backend` | KrakenD 背後要呼叫的 upstream | `endpoints[].backend[]` |
| `host` | upstream 的 base URL | `backend[]` |
| `url_pattern` | upstream 的 path 與 query | `backend[]` |
| `encoding` | KrakenD 處理 backend 回應的方式 | `backend[]` |
| `extra_config` | 各種擴充能力的設定入口 | root、endpoint、backend |
| `group` | 聚合結果的分組名稱 | `backend[]` |
| `allow` | 只保留指定欄位 | `backend[]` |
| `deny` | 移除指定欄位 | `backend[]` |

## 常用指令

| 類型 | 指令 | 用途 |
| --- | --- | --- |
| 檢查 Docker | `docker --version` | 確認 Docker 可用 |
| 檢查設定 | `docker run --rm -it -v "${PWD}:/etc/krakend/" krakend check --config krakend.json` | 驗證 `krakend.json` |
| 啟動 Gateway | `docker run --rm -p 8080:8080 -v "${PWD}:/etc/krakend/" krakend run -d -c /etc/krakend/krakend.json` | 啟動 KrakenD |
| 健康檢查 | `curl http://localhost:8080/__health` | 確認 Gateway 存活 |
| 呼叫 endpoint | `curl http://localhost:8080/users/1` | 測試 API 回應 |

## 常見設定位置

| 想設定的能力 | 放置位置 | namespace 或欄位 |
| --- | --- | --- |
| 對外路由 | endpoint 層 | `endpoint`, `method` |
| upstream 位置 | backend 層 | `host`, `url_pattern` |
| 聚合分組 | backend 層 | `group` |
| 欄位白名單 | backend 層 | `allow` |
| 欄位黑名單 | backend 層 | `deny` |
| endpoint 限流 | endpoint 層 `extra_config` | `qos/ratelimit/router` |
| backend 限流 | backend 層 `extra_config` | `qos/ratelimit/proxy` |
| router 全域選項 | root 層 `extra_config` | `router` |
| CORS | root 層 `extra_config` | `security/cors` |

## 常見錯誤

| 訊息特徵 | 可能原因 | 處理 |
| --- | --- | --- |
| `invalid character` | JSON 格式錯誤 | 檢查逗號、引號、括號 |
| `connection refused` | KrakenD 沒啟動或 port 錯誤 | 確認容器狀態與 `port` |
| `404 page not found` | 呼叫的路徑不是已註冊 endpoint | 檢查 `endpoint` 路徑 |
| 設定沒有生效 | `extra_config` 放錯層級 | 對照 root、endpoint、backend 範圍 |
| 回應欄位不如預期 | `allow` 或 `deny` 設定錯 | 先移除欄位過濾，再逐步加回 |
| Docker 掛載失敗 | 執行位置或路徑語法錯誤 | 在 `krakend.json` 所在資料夾執行 |

## 排錯順序

1. 確認目前資料夾有 `krakend.json`。
2. 執行 `krakend check --config krakend.json`。
3. 確認 `endpoint` 路徑與實際 curl 路徑一致。
4. 確認 `host` 可以從你的環境連線。
5. 確認 `url_pattern` 是否正確帶入路徑參數。
6. 暫時移除 `allow`、`deny`、`extra_config`，先確認基本代理成功。
7. 一次只加回一種設定並重新驗證。

## 最小設定範本

```json
{
  "$schema": "https://www.krakend.io/schema/v2.13/krakend.json",
  "version": 3,
  "port": 8080,
  "endpoints": [
    {
      "endpoint": "/users/{id}",
      "method": "GET",
      "backend": [
        {
          "host": ["https://jsonplaceholder.typicode.com"],
          "url_pattern": "/users/{id}",
          "encoding": "json"
        }
      ]
    }
  ]
}
```
