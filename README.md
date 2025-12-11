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

### 3. 環境変数の設定

`.env`ファイルを作成し、以下の環境変数を設定してください：

```
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY=your-private-key
FIREBASE_CLIENT_EMAIL=your-client-email
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
CORS_ORIGINS=http://localhost:3000
```

**注意**: `FIREBASE_PRIVATE_KEY`は改行文字（`\n`）を含む場合があります。環境変数に設定する際は、`\\n`としてエスケープしてください。

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

- 環境変数が正しく設定されているか確認してください
- Firebase Consoleでサービスアカウントキーをダウンロードし、環境変数に設定してください
- デモモードで動作する場合は、環境変数が未設定でも動作します（実際のFirestoreは使用できません）

## テスト

```bash
pytest
```
