// カレンダーページコンポーネント
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ReservationCalendar from '../components/Calendar';
import TimeSlotSelector from '../components/TimeSlotSelector';
import ReservationList from '../components/ReservationList';
import { getUserReservations } from '../services/reservationService';
import './CalendarPage.css';

const CalendarPage = () => {
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedTime, setSelectedTime] = useState(null);
  const [reservations, setReservations] = useState([]);
  const [reservationsLoading, setReservationsLoading] = useState(true);

  // 認証チェック
  React.useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login');
    }
  }, [user, authLoading, navigate]);

  // 予約一覧を取得
  useEffect(() => {
    const fetchReservations = async () => {
      if (!user || !user.email) {
        setReservationsLoading(false);
        return;
      }

      setReservationsLoading(true);
      const result = await getUserReservations(user.email);
      if (result.success) {
        setReservations(result.data || []);
      } else {
        console.error('予約一覧の取得に失敗:', result.error);
        setReservations([]);
      }
      setReservationsLoading(false);
    };

    if (user) {
      fetchReservations();
    }
  }, [user]);

  // 日付選択時の処理
  const handleDateSelect = (date) => {
    setSelectedDate(date);
    setSelectedTime(null); // 日付が変更されたら時間をリセット
  };

  // 時間選択時の処理
  const handleTimeSelect = (time) => {
    setSelectedTime(time);
  };

  // 予約に進む
  const handleReserve = () => {
    if (selectedDate && selectedTime) {
      // 予約ページに遷移（日付と時間をパラメータとして渡す）
      const dateStr = selectedDate.toISOString().split('T')[0];
      navigate(`/reservation?date=${dateStr}&time=${selectedTime}`);
    }
  };

  // 予約キャンセル後の処理
  const handleReservationCancel = (reservationId) => {
    setReservations((prev) =>
      prev.filter((r) => r.reservation_id !== reservationId)
    );
  };

  if (authLoading) {
    return (
      <div className="calendar-page">
        <div className="loading-container">読み込み中...</div>
      </div>
    );
  }

  return (
    <div className="calendar-page">
      <div className="calendar-page-header">
        <h1 className="calendar-page-title">予約カレンダー</h1>
        <p className="calendar-page-subtitle">来店希望日時を選択してください</p>
      </div>

      <div className="calendar-page-content">
        <div className="calendar-section">
          <ReservationCalendar
            onDateSelect={handleDateSelect}
            selectedDate={selectedDate}
            userReservations={reservations}
          />
        </div>

        <div className="timeslot-section">
          <TimeSlotSelector
            selectedDate={selectedDate}
            onTimeSelect={handleTimeSelect}
            selectedTime={selectedTime}
          />
        </div>
      </div>

      {selectedDate && selectedTime && (
        <div className="calendar-page-footer">
          <div className="selected-info">
            <p>
              選択日時: {selectedDate.toLocaleDateString('ja-JP')} {selectedTime}
            </p>
          </div>
          <button
            type="button"
            className="reserve-button"
            onClick={handleReserve}
          >
            この日時で予約する
          </button>
        </div>
      )}

      {/* マイページセクション（予約一覧） */}
      <div className="calendar-page-reservations">
        <div className="reservations-section-header">
          <h2 className="reservations-section-title">マイ予約一覧</h2>
          <button
            type="button"
            className="mypage-link-button"
            onClick={() => navigate('/mypage')}
          >
            マイページへ
          </button>
        </div>
        <ReservationList
          reservations={reservations}
          onCancel={handleReservationCancel}
          loading={reservationsLoading}
        />
      </div>
    </div>
  );
};

export default CalendarPage;


