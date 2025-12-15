// Firebaseエラーメッセージを日本語に変換するユーティリティ
export const getErrorMessage = (errorCode) => {
  const errorMessages = {
    'auth/email-already-in-use': 'このメールアドレスは既に使用されています',
    'auth/invalid-email': 'メールアドレスの形式が正しくありません',
    'auth/operation-not-allowed': 'この操作は許可されていません。Firebase Consoleでメール/パスワード認証を有効にしてください',
    'auth/weak-password': 'パスワードが弱すぎます。8文字以上で設定してください',
    'auth/user-disabled': 'このアカウントは無効化されています',
    'auth/user-not-found': 'メールアドレスまたはパスワードが正しくありません',
    'auth/wrong-password': 'メールアドレスまたはパスワードが正しくありません',
    'auth/invalid-credential': 'メールアドレスまたはパスワードが正しくありません',
    'auth/too-many-requests': 'リクエストが多すぎます。しばらくしてから再度お試しください',
    'auth/network-request-failed': 'ネットワークエラーが発生しました。接続を確認してください',
    'auth/popup-closed-by-user': 'ログインがキャンセルされました',
    'auth/cancelled-popup-request': 'ログインがキャンセルされました',
    'auth/invalid-api-key': 'Firebase APIキーが無効です。設定を確認してください',
    'auth/app-not-authorized': 'Firebaseアプリが認証されていません。設定を確認してください',
    'auth/configuration-not-found': 'Firebase設定が見つかりません。.envファイルにFirebase設定を追加し、開発サーバーを再起動してください。詳細はFIREBASE_SETUP.mdを参照してください。',
    'auth/requires-recent-login': 'セキュリティのため、再度ログインしてからアカウントを削除してください',
  };

  return errorMessages[errorCode] || `エラーが発生しました（${errorCode || '不明なエラー'}）。もう一度お試しください`;
};

