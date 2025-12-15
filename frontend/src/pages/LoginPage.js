// ログインページコンポーネント
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import LoginForm from '../components/LoginForm';
import { useAuth } from '../context/AuthContext';
import './LoginPage.css';

const LoginPage = () => {
  const navigate = useNavigate();
  const { user, loading } = useAuth();

  // 既にログインしている場合はリダイレクト（Hooksは常に同じ順序で呼ばれる必要があるため、early returnの前に配置）
  useEffect(() => {
    if (user) {
      navigate('/');
    }
  }, [user, navigate]);

  // ローディング中の表示
  if (loading) {
    return (
      <div className="login-page">
        <div className="loading-container">
          <div className="loading-spinner">読み込み中...</div>
        </div>
      </div>
    );
  }

  // ログイン成功時の処理
  const handleLoginSuccess = () => {
    navigate('/');
  };

  return (
    <div className="login-page">
      <div className="login-page-header">
        <h1 className="login-page-title">呪術廻戦ポップアップショップ</h1>
        <p className="login-page-subtitle">予約カレンダー</p>
      </div>
      <LoginForm onLoginSuccess={handleLoginSuccess} />
    </div>
  );
};

export default LoginPage;

