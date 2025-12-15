// Firebase設定と初期化
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

// 環境変数からFirebase設定を取得
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
};

// Firebase設定が完全かチェック
const isFirebaseConfigured = () => {
  const hasAllRequiredFields = !!(
    firebaseConfig.apiKey &&
    firebaseConfig.authDomain &&
    firebaseConfig.projectId &&
    firebaseConfig.storageBucket &&
    firebaseConfig.messagingSenderId &&
    firebaseConfig.appId
  );
  
  const isValidConfig = !!(
    firebaseConfig.apiKey &&
    firebaseConfig.apiKey !== 'demo-api-key' &&
    firebaseConfig.apiKey.length > 20 && // APIキーは通常長い
    firebaseConfig.projectId &&
    firebaseConfig.projectId !== 'demo-project'
  );
  
  return hasAllRequiredFields && isValidConfig;
};

// Firebaseアプリを初期化（エラーハンドリング付き）
let app;
let auth;
let initializationError = null;

if (isFirebaseConfigured()) {
  try {
    // 設定値をログに出力（デバッグ用、本番では削除推奨）
    console.log('Firebase設定を読み込み中...', {
      apiKey: firebaseConfig.apiKey ? `${firebaseConfig.apiKey.substring(0, 10)}...` : '未設定',
      authDomain: firebaseConfig.authDomain,
      projectId: firebaseConfig.projectId,
    });
    
    app = initializeApp(firebaseConfig);
    auth = getAuth(app);
    console.log('Firebase初期化成功');
  } catch (error) {
    console.error('Firebase初期化エラー:', error);
    initializationError = error;
    auth = null;
  }
} else {
  const missingFields = [];
  if (!firebaseConfig.apiKey) missingFields.push('REACT_APP_FIREBASE_API_KEY');
  if (!firebaseConfig.authDomain) missingFields.push('REACT_APP_FIREBASE_AUTH_DOMAIN');
  if (!firebaseConfig.projectId) missingFields.push('REACT_APP_FIREBASE_PROJECT_ID');
  if (!firebaseConfig.storageBucket) missingFields.push('REACT_APP_FIREBASE_STORAGE_BUCKET');
  if (!firebaseConfig.messagingSenderId) missingFields.push('REACT_APP_FIREBASE_MESSAGING_SENDER_ID');
  if (!firebaseConfig.appId) missingFields.push('REACT_APP_FIREBASE_APP_ID');
  
  console.warn('Firebase設定が不完全です。以下の環境変数が設定されていません:', missingFields);
  console.warn('詳細は frontend/FIREBASE_SETUP.md を参照してください');
  auth = null;
}

export { auth, isFirebaseConfigured, initializationError };
export default app;
