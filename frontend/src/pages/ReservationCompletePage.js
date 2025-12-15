// 予約完了画面コンポーネント
import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getReservation } from '../services/reservationService';
import './ReservationCompletePage.css';

const ReservationCompletePage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { user } = useAuth();
  
  const [reservation, setReservation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const reservationId = searchParams.get('reservation_id');

  // 認証チェック
  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  // 予約詳細を取得
  useEffect(() => {
    const fetchReservation = async () => {
      if (!reservationId) {
        setError('予約IDが指定されていません');
        setLoading(false);
        return;
      }

      setLoading(true);
      const result = await getReservation(reservationId);
      
      if (result.success) {
        setReservation(result.data);
      } else {
        setError(result.error || '予約情報の取得に失敗しました');
      }
      setLoading(false);
    };

    if (user && reservationId) {
      fetchReservation();
    }
  }, [reservationId, user]);

  if (loading) {
    return (
      <div className="reservation-complete-page">
        <div className="loading-container">読み込み中...</div>
      </div>
    );
  }

  if (error || !reservation) {
    return (
      <div className="reservation-complete-page">
        <div className="error-container">
          <h2>エラー</h2>
          <p>{error || '予約情報が見つかりませんでした'}</p>
          <button
            type="button"
            className="back-button"
            onClick={() => navigate('/calendar')}
          >
            カレンダーに戻る
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="reservation-complete-page">
      <div className="complete-content">
        <div className="success-icon">✓</div>
        <h1 className="complete-title">予約が完了しました</h1>
        <p className="complete-message">
          予約確認メールを送信しました。メールをご確認ください。
        </p>

        <div className="reservation-info-card">
          <h2 className="info-card-title">予約情報</h2>
          
          <div className="info-item highlight">
            <span className="info-label">予約番号</span>
            <span className="info-value reservation-number">
              {reservation.reservation_number}
            </span>
          </div>

          <div className="info-item">
            <span className="info-label">来店日</span>
            <span className="info-value">
              {new Date(reservation.visit_date).toLocaleDateString('ja-JP', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                weekday: 'long',
              })}
            </span>
          </div>

          <div className="info-item">
            <span className="info-label">来店時間</span>
            <span className="info-value">{reservation.visit_time}</span>
          </div>

          <div className="info-item">
            <span className="info-label">お名前</span>
            <span className="info-value">{reservation.user_name}</span>
          </div>

          {reservation.products && reservation.products.length > 0 && (
            <div className="info-item">
              <span className="info-label">商品</span>
              <span className="info-value">
                {reservation.products.map((p, idx) => (
                  <span key={idx}>
                    {p.product_id} × {p.quantity}
                    {idx < reservation.products.length - 1 && ', '}
                  </span>
                ))}
              </span>
            </div>
          )}

          <div className="info-item">
            <span className="info-label">ステータス</span>
            <span className="info-value status-confirmed">
              {reservation.status === 'confirmed' ? '予約確定' : reservation.status}
            </span>
          </div>
        </div>

        <div className="complete-actions">
          <button
            type="button"
            className="action-button primary-button"
            onClick={() => navigate('/mypage')}
          >
            マイページで確認
          </button>
          <button
            type="button"
            className="action-button secondary-button"
            onClick={() => navigate('/calendar')}
          >
            新しい予約をする
          </button>
        </div>

        <div className="complete-note">
          <p>※ 予約番号は大切に保管してください</p>
          <p>※ 来店日の前日までキャンセル可能です</p>
        </div>
      </div>
    </div>
  );
};

export default ReservationCompletePage;



