// カレンダーコンポーネント
import React, { useState, useEffect, useMemo, useCallback } from 'react';
import Calendar from 'react-calendar';
import { getCalendarData, getMockCalendarData } from '../services/calendarService';
import './Calendar.css';

const ReservationCalendar = ({ onDateSelect, selectedDate, userReservations = [] }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [calendarData, setCalendarData] = useState({});
  const [loading, setLoading] = useState(false);

  // カレンダーデータを取得（パフォーマンス最適化）
  useEffect(() => {
    const fetchCalendarData = async () => {
      setLoading(true);
      const year = currentDate.getFullYear();
      const month = currentDate.getMonth();
      
      // APIからデータを取得（失敗時はモックデータを使用）
      const result = await getCalendarData(year, month);
      if (result.success) {
        setCalendarData(result.data);
      } else {
        // APIが利用できない場合はモックデータを使用
        if (result.useMock) {
          const mockResult = getMockCalendarData(year, month);
          setCalendarData(mockResult.data);
        } else {
          // その他のエラーの場合は空のデータを設定
          setCalendarData({});
        }
      }
      setLoading(false);
    };

    fetchCalendarData();
    // currentDateオブジェクトの年月のみを依存関係として使用
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentDate.getFullYear(), currentDate.getMonth()]);

  // 日付が変更されたときの処理（useCallbackで最適化）
  const handleDateChange = useCallback((date) => {
    setCurrentDate(date);
    if (onDateSelect) {
      onDateSelect(date);
    }
  }, [onDateSelect]);

  // ユーザー予約を日付文字列のSetに変換（パフォーマンス最適化）
  const userReservationDates = useMemo(() => {
    if (!userReservations || userReservations.length === 0) return new Set();
    
    return new Set(
      userReservations
        .filter(res => res.status !== 'cancelled')
        .map(res => new Date(res.visit_date).toISOString().split('T')[0])
    );
  }, [userReservations]);

  // 指定日のユーザー予約をチェック（最適化版）
  const hasUserReservation = useCallback((date) => {
    if (userReservationDates.size === 0) return false;
    
    const dateStr = date.toISOString().split('T')[0];
    return userReservationDates.has(dateStr);
  }, [userReservationDates]);

  // 現在の月の年月をメモ化（パフォーマンス最適化）
  const currentMonthYear = useMemo(() => ({
    month: currentDate.getMonth(),
    year: currentDate.getFullYear(),
  }), [currentDate.getMonth(), currentDate.getFullYear()]);

  // カレンダーの日付タイルをカスタマイズ（useCallbackで最適化）
  const tileContent = useCallback(({ date, view }) => {
    if (view === 'month') {
      const day = date.getDate();
      const month = date.getMonth();
      const year = date.getFullYear();
      const isUserReserved = hasUserReservation(date);
      
      // 現在表示中の月のデータのみ表示
      if (
        month === currentMonthYear.month &&
        year === currentMonthYear.year &&
        calendarData[day]
      ) {
        const dayData = calendarData[day];
        return (
          <div className={`calendar-day-status calendar-day-${dayData.status}`}>
            <div className="calendar-day-slots">{dayData.availableSlots}</div>
            {isUserReserved && (
              <div className="calendar-day-user-reservation" title="あなたの予約">
                ★
              </div>
            )}
          </div>
        );
      } else if (
        month === currentMonthYear.month &&
        year === currentMonthYear.year &&
        isUserReserved
      ) {
        // カレンダーデータがなくても予約があれば表示
        return (
          <div className="calendar-day-status">
            <div className="calendar-day-user-reservation" title="あなたの予約">
              ★
            </div>
          </div>
        );
      }
    }
    return null;
  }, [calendarData, currentMonthYear, hasUserReservation]);

  // 日付を無効化（過去の日付と満席の日付）（useCallbackで最適化）
  const tileDisabled = useCallback(({ date, view }) => {
    if (view === 'month') {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const checkDate = new Date(date);
      checkDate.setHours(0, 0, 0, 0);
      
      // 過去の日付は無効化
      if (checkDate < today) {
        return true;
      }
      
      // 満席の日付も無効化
      const day = date.getDate();
      const month = date.getMonth();
      const year = date.getFullYear();
      
      if (
        month === currentMonthYear.month &&
        year === currentMonthYear.year &&
        calendarData[day] &&
        calendarData[day].status === 'full'
      ) {
        return true;
      }
    }
    return false;
  }, [calendarData, currentMonthYear]);

  return (
    <div className="reservation-calendar">
      {loading && <div className="calendar-loading">読み込み中...</div>}
      <Calendar
        onChange={handleDateChange}
        value={selectedDate || currentDate}
        tileContent={tileContent}
        tileDisabled={tileDisabled}
        minDate={new Date()}
        locale="ja-JP"
        calendarType="gregory"
      />
    </div>
  );
};

export default ReservationCalendar;

