// マイページコンポーネント
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getUserReservations } from '../services/reservationService';
import { logout, deleteAccount } from '../services/authService';
import ReservationList from '../components/ReservationList';
import './MyPage.css';

const MyPage = () => {
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleting, setDeleting] = useState(false);

  // 認証チェック
  useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login');
    }
  }, [user, authLoading, navigate]);

  // 予約一覧を取得
  useEffect(() => {
    const fetchReservations = async () => {
      if (!user || !user.email) {
        setLoading(false);
        return;
      }

      setLoading(true);
      const result = await getUserReservations(user.email);
      if (result.success) {
        setReservations(result.data || []);
      } else {
        console.error('予約一覧の取得に失敗:', result.error);
        setReservations([]);
      }
      setLoading(false);
    };

    if (user) {
      fetchReservations();
    }
  }, [user]);

  // 予約キャンセル後の処理
  const handleReservationCancel = (reservationId) => {
    setReservations((prev) =>
      prev.filter((r) => r.reservation_id !== reservationId)
    );
  };

  // アカウント削除
  const handleDeleteAccount = async () => {
    setDeleting(true);
    try {
      const result = await deleteAccount();
      if (result.success) {
        await logout();
        navigate('/login');
      } else {
        alert(result.error || 'アカウントの削除に失敗しました');
      }
    } catch (error) {
      console.error('アカウント削除エラー:', error);
      alert('アカウントの削除に失敗しました: ' + error.message);
    } finally {
      setDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  // ログアウト
  const handleLogout = async () => {
    const result = await logout();
    if (result.success) {
      navigate('/login');
    }
  };

  // 前画面に戻る
  const handleGoBack = () => {
    // ブラウザの履歴を1つ戻る（履歴がない場合はホームに遷移）
    if (window.history.length > 1) {
      navigate(-1);
    } else {
      navigate('/');
    }
  };

  if (authLoading) {
    return (
      <div className="mypage">
        <div className="mypage-loading">読み込み中...</div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="mypage">
      <div className="mypage-header">
        <div className="mypage-header-left">
          <button
            type="button"
            className="back-button"
            onClick={handleGoBack}
            aria-label="前画面に戻る"
          >
            ← 戻る
          </button>
          <h1 className="mypage-title">マイページ</h1>
        </div>
        <button type="button" className="logout-button" onClick={handleLogout}>
          ログアウト
        </button>
      </div>

      <div className="mypage-content">
        <div className="user-info-section">
          <h2 className="section-title">ユーザー情報</h2>
          <div className="user-info">
            <div className="info-row">
              <span className="info-label">メールアドレス:</span>
              <span className="info-value">{user.email}</span>
            </div>
            <div className="info-row">
              <span className="info-label">ユーザーID:</span>
              <span className="info-value">{user.uid}</span>
            </div>
          </div>
        </div>

        <div className="reservations-section">
          <h2 className="section-title">予約一覧</h2>
          <ReservationList
            reservations={reservations}
            onCancel={handleReservationCancel}
            loading={loading}
          />
        </div>

        {/* アカウント削除セクション（スクロールしないと見えない位置） */}
        <div className="account-delete-section">
          <h2 className="section-title">アカウント設定</h2>
          <div className="delete-account-content">
            <p className="delete-warning">
              アカウントを削除すると、すべての予約情報が失われます。
              この操作は取り消せません。
            </p>
            {showDeleteConfirm ? (
              <div className="delete-confirm">
                <p className="delete-confirm-message">
                  本当にアカウントを削除しますか？
                </p>
                <div className="delete-confirm-buttons">
                  <button
                    type="button"
                    className="delete-confirm-button delete-button"
                    onClick={handleDeleteAccount}
                    disabled={deleting}
                  >
                    {deleting ? '削除中...' : '削除する'}
                  </button>
                  <button
                    type="button"
                    className="delete-confirm-button cancel-button"
                    onClick={() => setShowDeleteConfirm(false)}
                    disabled={deleting}
                  >
                    キャンセル
                  </button>
                </div>
              </div>
            ) : (
              <button
                type="button"
                className="delete-account-button"
                onClick={() => setShowDeleteConfirm(true)}
              >
                アカウントを削除
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MyPage;

