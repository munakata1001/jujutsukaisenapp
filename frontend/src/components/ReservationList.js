// 予約一覧コンポーネント
import React, { useState } from 'react';
import { cancelReservation } from '../services/reservationService';
import './ReservationList.css';

const ReservationList = ({ reservations, onCancel, loading }) => {
  const [cancellingId, setCancellingId] = useState(null);

  // 予約をキャンセル
  const handleCancel = async (reservationId) => {
    if (!window.confirm('この予約をキャンセルしますか？')) {
      return;
    }

    setCancellingId(reservationId);
    const result = await cancelReservation(reservationId);
    setCancellingId(null);

    if (result.success) {
      onCancel && onCancel(reservationId);
    } else {
      alert(result.error || 'キャンセルに失敗しました');
    }
  };

  // ステータスに応じた表示
  const getStatusLabel = (status) => {
    const statusMap = {
      pending: '予約待ち',
      confirmed: '予約確定',
      cancelled: 'キャンセル済み',
      completed: '来店済み',
    };
    return statusMap[status] || status;
  };

  // ステータスに応じたクラス名
  const getStatusClass = (status) => {
    const classMap = {
      pending: 'status-pending',
      confirmed: 'status-confirmed',
      cancelled: 'status-cancelled',
      completed: 'status-completed',
    };
    return classMap[status] || '';
  };

  // キャンセル可能かチェック
  const canCancel = (reservation) => {
    if (reservation.status === 'cancelled' || reservation.status === 'completed') {
      return false;
    }
    // 来店日の前日までキャンセル可能
    const visitDate = new Date(reservation.visit_date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    visitDate.setHours(0, 0, 0, 0);
    const daysUntilVisit = Math.floor((visitDate - today) / (1000 * 60 * 60 * 24));
    return daysUntilVisit >= 1;
  };

  if (loading) {
    return <div className="reservation-list-loading">読み込み中...</div>;
  }

  if (!reservations || reservations.length === 0) {
    return (
      <div className="reservation-list-empty">
        <p>予約がありません</p>
      </div>
    );
  }

  return (
    <div className="reservation-list">
      {reservations.map((reservation) => (
        <div key={reservation.reservation_id} className="reservation-item">
          <div className="reservation-header">
            <div className="reservation-number">
              予約番号: {reservation.reservation_number}
            </div>
            <div className={`reservation-status ${getStatusClass(reservation.status)}`}>
              {getStatusLabel(reservation.status)}
            </div>
          </div>

          <div className="reservation-details">
            <div className="reservation-detail-row">
              <span className="detail-label">来店日時:</span>
              <span className="detail-value">
                {new Date(reservation.visit_date).toLocaleDateString('ja-JP')}{' '}
                {reservation.visit_time}
              </span>
            </div>

            {reservation.products && reservation.products.length > 0 && (
              <div className="reservation-detail-row">
                <span className="detail-label">商品:</span>
                <span className="detail-value">
                  {reservation.products.map((p, idx) => (
                    <span key={idx}>
                      {p.product_id} × {p.quantity}
                      {idx < reservation.products.length - 1 && ', '}
                    </span>
                  ))}
                </span>
              </div>
            )}

            <div className="reservation-detail-row">
              <span className="detail-label">予約日:</span>
              <span className="detail-value">
                {new Date(reservation.created_at).toLocaleString('ja-JP')}
              </span>
            </div>
          </div>

          {canCancel(reservation) && (
            <div className="reservation-actions">
              <button
                type="button"
                className="cancel-button"
                onClick={() => handleCancel(reservation.reservation_id)}
                disabled={cancellingId === reservation.reservation_id}
              >
                {cancellingId === reservation.reservation_id ? 'キャンセル中...' : 'キャンセル'}
              </button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default ReservationList;



