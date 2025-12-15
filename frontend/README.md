# フロントエンド

Reactを使用したフロントエンドアプリケーションです。

## セットアップ

```bash
npm install
```

## 環境変数

`.env`ファイルを作成し、以下の環境変数を設定してください：

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_FIREBASE_API_KEY=your-firebase-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
REACT_APP_FIREBASE_APP_ID=your-app-id
```

## 開発サーバーの起動

```bash
npm start
```

開発サーバーは `http://localhost:3000` で起動します。

## ビルド

```bash
npm run build
```

## テスト

```bash
npm test
```

