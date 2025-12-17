// Firebase設定と初期化（最小構成）
import { getApp, getApps, initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

// CRA では REACT_APP_* のみがフロントに埋め込まれるため、それだけを見る。
// ただし、環境によって `.env` が読み込めない/作れないことがあるため、
// `public/firebase-config.js` で window.__FIREBASE_CONFIG__ を定義した場合はそれを優先する。
const getWindowFirebaseConfig = () => {
  try {
    if (typeof window === 'undefined') return null;
    const cfg = window.__FIREBASE_CONFIG__;
    if (!cfg || typeof cfg !== 'object') return null;
    return cfg;
  } catch {
    return null;
  }
};

const getEnv = (key) => (typeof process !== 'undefined' ? process.env?.[key] : undefined);

const windowCfg = getWindowFirebaseConfig();

const firebaseConfig = {
  apiKey: windowCfg?.apiKey || getEnv('REACT_APP_FIREBASE_API_KEY'),
  authDomain: windowCfg?.authDomain || getEnv('REACT_APP_FIREBASE_AUTH_DOMAIN'),
  projectId: windowCfg?.projectId || getEnv('REACT_APP_FIREBASE_PROJECT_ID'),
  storageBucket: windowCfg?.storageBucket || getEnv('REACT_APP_FIREBASE_STORAGE_BUCKET'),
  messagingSenderId: windowCfg?.messagingSenderId || getEnv('REACT_APP_FIREBASE_MESSAGING_SENDER_ID'),
  appId: windowCfg?.appId || getEnv('REACT_APP_FIREBASE_APP_ID'),
};

// 最低限の必須項目だけ確認（厳しすぎるバリデーションはしない）
const isFirebaseConfigured = () =>
  !!(firebaseConfig.apiKey && firebaseConfig.authDomain && firebaseConfig.projectId && firebaseConfig.appId);

// 何が足りないかを特定（ユーザーが原因を追いやすくする）
const getMissingFirebaseKeys = () => {
  const required = ['apiKey', 'authDomain', 'projectId', 'appId'];
  return required.filter((k) => !firebaseConfig[k]);
};

// Firebaseアプリを初期化（HMR等で二重初期化しない）
let app = null;
let auth = null;
let initializationError = null;

if (isFirebaseConfigured()) {
  try {
    app = getApps().length ? getApp() : initializeApp(firebaseConfig);
    auth = getAuth(app);
  } catch (error) {
    initializationError = error;
    app = null;
    auth = null;
  }
} else {
  // `.env` が読み込まれていない/値が空のときに原因が分かるように出しておく（機密は出さない）
  const missing = getMissingFirebaseKeys();
  if (missing.length) {
    // eslint-disable-next-line no-console
    console.warn(
      '[Firebase] 設定が不足しています。missing=',
      missing,
      'source=',
      windowCfg ? 'public/firebase-config.js' : 'frontend/.env (REACT_APP_*)'
    );
  }
}

export { app, auth, isFirebaseConfigured, initializationError, getMissingFirebaseKeys };
export default app;
