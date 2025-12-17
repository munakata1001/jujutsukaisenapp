// 認証関連のサービス関数
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  sendPasswordResetEmail,
  deleteUser,
} from 'firebase/auth';
import { auth, getMissingFirebaseKeys, isFirebaseConfigured, initializationError } from '../utils/firebase';
import { getErrorMessage } from '../utils/errorMessages';

// Firebaseが初期化されていない場合のエラーチェック
const checkAuthAvailable = () => {
  if (!auth) {
    if (initializationError) {
      console.error('Firebase初期化エラーの詳細:', initializationError);
      throw new Error('FIREBASE_INITIALIZATION_FAILED');
    }
    if (!isFirebaseConfigured()) {
      throw new Error('FIREBASE_NOT_CONFIGURED');
    }
    throw new Error('FIREBASE_NOT_INITIALIZED');
  }
};

// メールアドレスとパスワードでログイン
export const loginWithEmail = async (email, password) => {
  try {
    checkAuthAvailable();
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    return { success: true, user: userCredential.user };
  } catch (error) {
    if (error.message === 'FIREBASE_NOT_CONFIGURED') {
      const missing = getMissingFirebaseKeys?.() || [];
      return { 
        success: false, 
        error:
          missing.length > 0
            ? `Firebase設定が不完全です（不足: ${missing.join(', ')}）。frontend/.env（REACT_APP_FIREBASE_*）または public/firebase-config.js にFirebase設定を追加してください。`
            : 'Firebase設定が不完全です。.envファイルにFirebase設定を追加してください。'
      };
    }
    if (error.message === 'FIREBASE_NOT_INITIALIZED') {
      return { 
        success: false, 
        error: 'Firebaseの初期化に失敗しました。設定を確認してください。' 
      };
    }
    const errorMessage = getErrorMessage(error.code);
    return { success: false, error: errorMessage, errorCode: error.code };
  }
};

// 新規ユーザー登録
export const registerWithEmail = async (email, password) => {
  try {
    checkAuthAvailable();
    
    // パスワードのバリデーション
    if (!password || password.length < 8) {
      return { 
        success: false, 
        error: 'パスワードは8文字以上で入力してください。' 
      };
    }
    
    // メールアドレスのバリデーション
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return { 
        success: false, 
        error: 'メールアドレスの形式が正しくありません。' 
      };
    }
    
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    return { success: true, user: userCredential.user };
  } catch (error) {
    if (error.message === 'FIREBASE_NOT_CONFIGURED') {
      return { 
        success: false, 
        error: 'Firebase設定が不完全です。.envファイルにFirebase設定を追加し、開発サーバーを再起動してください。手順は frontend/firebase.env.txt を参照してください。' 
      };
    }
    if (error.message === 'FIREBASE_INITIALIZATION_FAILED') {
      return { 
        success: false, 
        error: 'Firebaseの初期化に失敗しました。設定を確認してください。コンソールにエラー詳細が表示されています。' 
      };
    }
    if (error.message === 'FIREBASE_NOT_INITIALIZED') {
      return { 
        success: false, 
        error: 'Firebaseの初期化に失敗しました。設定を確認してください。' 
      };
    }
    
    // Firebaseエラーの詳細をログに出力
    console.error('Firebase認証エラー:', error);
    console.error('エラーコード:', error.code);
    console.error('エラーメッセージ:', error.message);
    
    const errorMessage = getErrorMessage(error.code);
    return { success: false, error: errorMessage, errorCode: error.code };
  }
};

// パスワードリセットメールを送信
export const resetPassword = async (email) => {
  try {
    await sendPasswordResetEmail(auth, email);
    return { success: true };
  } catch (error) {
    const errorMessage = getErrorMessage(error.code);
    return { success: false, error: errorMessage, errorCode: error.code };
  }
};

// ログアウト
export const logout = async () => {
  try {
    await signOut(auth);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
};

// アカウント削除
export const deleteAccount = async () => {
  try {
    checkAuthAvailable();
    if (!auth.currentUser) {
      return { success: false, error: 'ログインしていません' };
    }
    await deleteUser(auth.currentUser);
    return { success: true };
  } catch (error) {
    console.error('アカウント削除エラー:', error);
    const errorMessage = getErrorMessage(error.code);
    return { success: false, error: errorMessage, errorCode: error.code };
  }
};

// 認証状態の変更を監視
export const onAuthStateChange = (callback) => {
  if (!auth) {
    // Firebaseが初期化されていない場合は、nullをコールバックに渡す
    callback(null);
    return () => {}; // 空のunsubscribe関数を返す
  }
  return onAuthStateChanged(auth, callback);
};

