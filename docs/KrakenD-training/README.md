# KrakenD Lab 課程

本課程用「先跑起來、再理解設定」的方式帶學員認識 KrakenD。學員會從最小可執行 Gateway 開始，逐步練習 endpoint、backend、資料聚合、欄位整理與限流設定。

## 課程設計主旨

這不是完整理論手冊。每個 Lab 都先讓你完成一個可驗證的小結果，再用該結果回頭解釋 KrakenD 的設定位置與責任邊界。

課程設計重點：

- 每個 Lab 都能單獨操作。
- 每個 Lab 都包含驗證方式。
- 先理解 `krakend.json` 的結構，再進入進階能力。
- 所有設定都以 KrakenD Community Edition 常見能力為主。

## 使用環境

建議使用 Docker 執行 KrakenD，避免學員被本機安裝差異卡住。

環境確認：

```powershell
docker --version
curl --version
```

KrakenD 官方 Docker 映像可用以下方式啟動健康檢查端點：

```powershell
docker run --rm -p 8080:8080 -v "${PWD}:/etc/krakend/" krakend
curl http://localhost:8080/__health
```

說明：官方映像預設會執行 `run`，並從掛載到 `/etc/krakend/` 的目錄讀取設定。正式環境不建議依賴浮動版本，課堂為了降低上手門檻才使用 `krakend` 映像名稱。

## 課程路線

1. [Lab 00：KrakenD 核心名詞導讀](00-krakend-core-concepts.md)
2. [Lab 01：建立第一個 KrakenD Gateway](01-first-gateway.md)
3. [Lab 02：聚合多個 Backend 並整理回應欄位](02-aggregation-and-shaping.md)
4. [Lab 03：替 Endpoint 與 Backend 加上限流](03-rate-limit.md)
5. [KrakenD 入門速查表](99-cheatsheet.md)

## 每個 Lab 的操作原則

- 每個 Lab 建議使用新的空資料夾操作，避免舊的 `krakend.json` 影響結果。
- 修改設定後先執行 `krakend check`，再啟動 Gateway。
- 若使用 Windows PowerShell，範例中的 `${PWD}` 可直接使用。
- 若使用 Git Bash 或 Linux shell，路徑掛載語法可能需要改成 `$PWD:/etc/krakend/`。
- Lab 中的公開測試 API 只用於學習，正式專案應改成公司內部服務或可控測試服務。

## 完成課程後你應該能做到

- 看懂 KrakenD `version`、`endpoints`、`backend`、`extra_config` 的責任。
- 建立一個對外 endpoint，讓 KrakenD 轉送到 upstream backend。
- 用多個 backend 建立聚合 API。
- 用 `allow` 與 `deny` 控制回應欄位。
- 分辨 router rate limit 與 backend rate limit 的位置與用途。
- 在部署前用 `krakend check` 驗證設定。

## 參考依據

- KrakenD Configuration Structure：https://www.krakend.io/docs/configuration/structure/
- KrakenD Backend Configuration：https://www.krakend.io/docs/backends/
- KrakenD Sequential Proxying：https://www.krakend.io/docs/endpoints/sequential-proxy/
- KrakenD Rate Limiting API Gateway Endpoints：https://www.krakend.io/docs/endpoints/rate-limit/
- KrakenD Rate Limiting Backends：https://www.krakend.io/docs/backends/rate-limit/
- Docker Hub official `krakend` image：https://hub.docker.com/_/krakend/
