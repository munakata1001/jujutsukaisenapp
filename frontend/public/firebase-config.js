// Firebase設定フォールバック（`.env` が使えない環境向け）
//
// 使い方:
// 1) Firebase Console > プロジェクト設定 > 全般 > マイアプリ（Web） > SDK の設定と構成（構成）
// 2) 下記の値を埋める
// 3) `npm start` を再起動する
//
// 注意:
// - これはフロント（ブラウザ）に配信されます（秘密情報は入れないでください）
// - Firebase Web SDK の設定値（apiKey など）は「公開して良い」想定の値です
// - `.env` の REACT_APP_FIREBASE_* が読める場合は `.env` が優先されます
//
// eslint-disable-next-line no-underscore-dangle
window.__FIREBASE_CONFIG__ = {
  apiKey: '',
  authDomain: '',
  projectId: 'jujutukaisenapp2',
  appId: '',
  // 任意
  storageBucket: '',
  messagingSenderId: '',
};

