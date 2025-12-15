// ログインフォームコンポーネント
import React, { useState } from 'react';
import { loginWithEmail, registerWithEmail, resetPassword } from '../services/authService';
import './LoginForm.css';

const LoginForm = ({ onLoginSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPasswordReset, setShowPasswordReset] = useState(false);

  // フォーム送信処理
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    setLoading(true);

    // クライアント側のバリデーション
    if (!email || !password) {
      setError('メールアドレスとパスワードを入力してください');
      setLoading(false);
      return;
    }

    if (!isLogin && password.length < 8) {
      setError('パスワードは8文字以上で入力してください');
      setLoading(false);
      return;
    }

    try {
      let result;
      if (isLogin) {
        // ログイン処理
        result = await loginWithEmail(email, password);
      } else {
        // 新規登録処理
        result = await registerWithEmail(email, password);
      }

      if (result.success) {
        setSuccessMessage(isLogin ? 'ログインに成功しました' : 'アカウントの作成に成功しました');
        setTimeout(() => {
          onLoginSuccess && onLoginSuccess(result.user);
        }, 1000);
      } else {
        setError(result.error || 'エラーが発生しました');
        setSuccessMessage('');
        // エラーの詳細をコンソールに出力（デバッグ用）
        if (result.errorCode) {
          console.error('認証エラーコード:', result.errorCode);
        }
      }
    } catch (err) {
      console.error('予期しないエラー:', err);
      setError('予期しないエラーが発生しました。コンソールを確認してください。');
      setSuccessMessage('');
    } finally {
      setLoading(false);
    }
  };

  // パスワードリセット処理
  const handlePasswordReset = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    setLoading(true);

    try {
      const result = await resetPassword(email);
      if (result.success) {
        setSuccessMessage('パスワードリセットメールを送信しました。メールをご確認ください。');
        setError('');
        setTimeout(() => {
          setShowPasswordReset(false);
          setSuccessMessage('');
        }, 5000);
      } else {
        setError(result.error || 'エラーが発生しました');
        setSuccessMessage('');
      }
    } catch (err) {
      setError('予期しないエラーが発生しました');
      setSuccessMessage('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-form-container">
      <div className="login-form">
        <h2 className="login-form-title">
          {isLogin ? 'ログイン' : '新規登録'}
        </h2>

        {error && <div className="error-message">{error}</div>}
        {successMessage && <div className="success-message">{successMessage}</div>}

        {showPasswordReset ? (
          <form onSubmit={handlePasswordReset}>
            <div className="form-group">
              <label htmlFor="reset-email">メールアドレス</label>
              <input
                id="reset-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="example@email.com"
                disabled={loading}
              />
            </div>
            <button
              type="submit"
              className="submit-button"
              disabled={loading}
            >
              {loading ? '送信中...' : 'リセットメールを送信'}
            </button>
            <div className="form-switch">
              <button
                type="button"
                className="switch-button"
                onClick={() => {
                  setShowPasswordReset(false);
                  setError('');
                  setSuccessMessage('');
                }}
                disabled={loading}
              >
                ログインに戻る
              </button>
            </div>
          </form>
        ) : (
          <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">メールアドレス</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="example@email.com"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">パスワード</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="8文字以上"
              minLength={8}
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            className="submit-button"
            disabled={loading}
          >
            {loading ? '処理中...' : isLogin ? 'ログイン' : '登録'}
          </button>

          <div className="form-switch">
            <button
              type="button"
              className="switch-button"
              onClick={() => {
                setIsLogin(!isLogin);
                setError('');
                setSuccessMessage('');
              }}
              disabled={loading}
            >
              {isLogin
                ? 'アカウントをお持ちでない方はこちら'
                : 'すでにアカウントをお持ちの方はこちら'}
            </button>
            {isLogin && (
              <button
                type="button"
                className="switch-button password-reset-button"
                onClick={() => {
                  setShowPasswordReset(true);
                  setError('');
                  setSuccessMessage('');
                }}
                disabled={loading}
              >
                パスワードを忘れた方はこちら
              </button>
            )}
          </div>
        </form>
        )}
      </div>
    </div>
  );
};

export default LoginForm;

