# バックエンド

FastAPIを使用したバックエンドAPIです。

## セットアップ

### 1. 仮想環境の作成

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (コマンドプロンプト):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. Firebase Admin SDKの設定

バックエンドでFirebase Admin SDKを使用するには、認証情報の設定が必要です。

**詳細な設定手順は `FIREBASE_ADMIN_SETUP.md` を参照してください。**

#### 簡単な設定方法（推奨）

1. **Firebaseコンソールでサービスアカウントキーを取得**
   - Firebaseコンソール → プロジェクトの設定 → サービスアカウント
   - 「新しい秘密鍵の生成」をクリックしてJSONファイルをダウンロード

2. **キーファイルを配置**
   - ダウンロードしたJSONファイルを `backend/` ディレクトリに配置
   - 例: `backend/firebase-service-account.json`

3. **環境変数を設定**
   - `backend/.env` ファイルを作成し、以下を追加：
   ```
   GOOGLE_APPLICATION_CREDENTIALS=firebase-service-account.json
   CORS_ORIGINS=http://localhost:3000
   ```

**重要**: サービスアカウントキーファイルは機密情報です。`.gitignore`に追加されていることを確認してください。

### 4. 開発サーバーの起動

```bash
uvicorn app.main:app --reload
```

または

```bash
python -m uvicorn app.main:app --reload
```

APIサーバーは `http://localhost:8000` で起動します。

## APIドキュメント

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## トラブルシューティング

### uvicornコマンドが見つからない場合

1. 仮想環境がアクティブになっているか確認してください
2. 依存関係がインストールされているか確認してください：
   ```bash
   pip list | findstr uvicorn
   ```
3. 仮想環境を再作成して、依存関係を再インストールしてください

### Firebase接続エラーの場合

**エラー: "Your default credentials were not found"**

このエラーは、Firebase Admin SDKの認証情報が設定されていない場合に発生します。

1. `backend/.env` ファイルが存在するか確認
2. `GOOGLE_APPLICATION_CREDENTIALS` 環境変数が正しく設定されているか確認
3. サービスアカウントキーファイルのパスが正しいか確認
4. 詳細は `FIREBASE_ADMIN_SETUP.md` を参照してください

**その他のエラー**

- 環境変数が正しく設定されているか確認してください
- Firebase Consoleでサービスアカウントキーをダウンロードし、正しく配置されているか確認してください
- サービスアカウントにFirestoreの読み書き権限があるか確認してください

## テスト

```bash
pytest
```
