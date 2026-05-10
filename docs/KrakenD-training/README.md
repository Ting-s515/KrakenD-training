# KrakenD Lab 課程

本課程用「先跑起來、再理解設定」的方式帶學員認識 KrakenD。課程已包含 `docker compose` 環境、KrakenD 設定檔與範例 backend 程式碼，學員拿到 repo 後只要照步驟啟動環境即可。

## 課程設計主旨

這不是完整理論手冊。每個 Lab 都先讓你完成一個可驗證的小結果，再用該結果回頭解釋 KrakenD 的設定位置與責任邊界。

課程設計重點：

- 每個 Lab 都使用同一套可重複啟動的課程環境。
- 每個 Lab 都包含驗證方式。
- 先理解 `krakend.json` 的結構，再進入進階能力。
- 所有設定都以 KrakenD Community Edition 常見能力為主。

## 使用環境

本課程使用 Docker Compose 啟動 KrakenD 與課程用 mock backend，避免學員被本機安裝差異卡住。

環境確認：

```powershell
docker --version
docker compose version
```

在 repo 根目錄啟動課程環境：

```powershell
docker compose up -d
curl http://localhost:18000/__health
```

說明：根目錄 `.env` 固定課程使用的映像版本；`docker-compose.yaml` 定義 `krakend` 與 `mock-api` 兩個服務。

## 課程路線

1. [課程環境：Docker Compose 與範例服務](environment-setup.md)
2. [Lab 00：KrakenD 核心名詞導讀](00-krakend-core-concepts.md)
3. [Lab 01：建立第一個 KrakenD Gateway](01-first-gateway.md)
4. [Lab 02：聚合多個 Backend 並整理回應欄位](02-aggregation-and-shaping.md)
5. [Lab 03：替 Endpoint 與 Backend 加上限流](03-rate-limit.md)
6. [KrakenD 入門速查表](99-cheatsheet.md)

## 每個 Lab 的操作原則

- 先完成 [課程環境](environment-setup.md) 的啟動與驗證。
- Lab 主要修改 repo 根目錄的 `krakend.json`。
- 修改設定後先執行 `docker compose run --rm --no-deps krakend check --config /etc/krakend/krakend.json`。
- 設定驗證通過後執行 `docker compose restart krakend`。
- 範例 backend 程式碼在 repo 根目錄的 `mock-api/mock_api.py`，回應資料固定，方便比較每次練習結果。

## 完成課程後你應該能做到

- 看懂 KrakenD `version`、`endpoints`、`backend`、`extra_config` 的責任。
- 建立一個對外 endpoint，讓 KrakenD 轉送到 upstream backend。
- 用多個 backend 建立聚合 API。
- 用 `allow` 與 `deny` 控制回應欄位。
- 分辨 router rate limit 與 backend rate limit 的位置與用途。
- 在部署前用 `krakend check` 驗證設定。

## 課程環境檔案

| Path | 用途 |
| --- | --- |
| `..\..\.env` | 固定 Docker image 版本與 host port |
| `..\..\docker-compose.yaml` | 啟動 KrakenD 與 mock backend |
| `..\..\krakend.json` | 課程用 KrakenD 設定 |
| `..\..\mock-api\mock_api.py` | 課程用範例 backend 程式碼 |

## 參考依據

- KrakenD Configuration Structure：https://www.krakend.io/docs/configuration/structure/
- KrakenD Backend Configuration：https://www.krakend.io/docs/backends/
- KrakenD Sequential Proxying：https://www.krakend.io/docs/endpoints/sequential-proxy/
- KrakenD Rate Limiting API Gateway Endpoints：https://www.krakend.io/docs/endpoints/rate-limit/
- KrakenD Rate Limiting Backends：https://www.krakend.io/docs/backends/rate-limit/
- Docker Hub official `krakend` image：https://hub.docker.com/_/krakend/
- Docker Compose documentation：https://docs.docker.com/compose/
