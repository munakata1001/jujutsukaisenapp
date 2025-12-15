# 接続エラーの解決方法

## エラーの内容

```
Failed to load resource: net::ERR_CONNECTION_REFUSED
:8000/api/products:1 Failed to load resource: net::ERR_CONNECTION_REFUSED
TypeError: Failed to fetch
```

## エラーの意味

このエラーは、**フロントエンドがバックエンドAPIサーバー（http://localhost:8000）に接続できない**ことを示しています。

`ERR_CONNECTION_REFUSED`は、以下のいずれかの状態を意味します：

1. **バックエンドサーバーが起動していない**
2. **バックエンドサーバーが別のポートで実行されている**
3. **ファイアウォールやセキュリティソフトが接続をブロックしている**

## 解決方法

### ステップ1: バックエンドサーバーが起動しているか確認

**新しいターミナル（コマンドプロンプト）を開いて**、以下を実行：

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

または、既に実行中の場合は以下を確認：

```bash
# Windowsの場合
netstat -ano | findstr :8000

# 実行中であれば、プロセスIDが表示されます
```

### ステップ2: バックエンドサーバーの起動を確認

バックエンドサーバーが正常に起動している場合、以下のようなメッセージが表示されます：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### ステップ3: ブラウザで直接APIにアクセスして確認

バックエンドサーバーが起動したら、ブラウザで以下にアクセス：

```
http://localhost:8000/
```

正常であれば、以下のJSONが表示されます：

```json
{"message": "呪術廻戦ポップアップショップ予約API"}
```

または、ヘルスチェック：

```
http://localhost:8000/api/health
```

正常であれば：

```json
{"status": "ok"}
```

### ステップ4: フロントエンドを再起動

バックエンドサーバーが起動した後、フロントエンドを再読み込み（F5キー）してください。

## トラブルシューティング

### 問題1: ポート8000が既に使用されている

**エラーメッセージ例**:
```
Error: [Errno 10048] 通常は各ソケット アドレス (プロトコル/ネットワーク アドレス/ポート) は一度しか使用できません。
```

**解決方法**:
1. 別のポートを使用する：

```bash
python -m uvicorn app.main:app --reload --port 8001
```

2. フロントエンドの環境変数を変更：

`frontend/.env`ファイルを作成または編集：

```env
REACT_APP_API_BASE_URL=http://localhost:8001
REACT_APP_API_URL=http://localhost:8001
```

3. フロントエンドを再起動

### 問題2: ファイアウォールが接続をブロックしている

**確認事項**:
1. Windowsファイアウォールの設定を確認
2. セキュリティソフトがポート8000をブロックしていないか確認

**解決方法**:
- Windowsファイアウォールでポート8000を許可する
- セキュリティソフトの設定を確認

### 問題3: バックエンドサーバーがエラーで起動しない

**確認事項**:
- ターミナルでエラーメッセージを確認
- 前回のエラー（Firebase認証エラーなど）が解決されているか確認

**解決方法**:
- `backend/FIREBASE_AUTH_FIX.md`を参照してFirebase設定を確認
- エラーメッセージに基づいて対処

### 問題4: フロントエンドとバックエンドが別のマシンで実行されている

**解決方法**:
1. バックエンドの起動時に `--host 0.0.0.0` を指定（既に含まれています）

2. フロントエンドの環境変数を変更：

`frontend/.env`:

```env
REACT_APP_API_BASE_URL=http://バックエンドのIPアドレス:8000
REACT_APP_API_URL=http://バックエンドのIPアドレス:8000
```

## 確認チェックリスト

- [ ] バックエンドサーバーが起動している
- [ ] `http://localhost:8000/`にブラウザでアクセスできる
- [ ] エラーメッセージがない（ターミナルを確認）
- [ ] ポート8000が使用可能
- [ ] ファイアウォールが接続を許可している
- [ ] フロントエンドが正しいAPI URLを使用している

## 正常な動作状態

### バックエンド（ターミナル1）

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### フロントエンド（ターミナル2）

```bash
cd frontend
npm start
```

ブラウザで `http://localhost:3000` にアクセスすると、エラーなく動作します。

## まとめ

- **このエラーは、バックエンドサーバーが起動していないことを示しています**
- **新しいターミナルでバックエンドサーバーを起動してください**
- **`http://localhost:8000/`にアクセスして、サーバーが正常に動作しているか確認してください**

