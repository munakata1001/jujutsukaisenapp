// 時間帯選択コンポーネント
import React, { useState, useEffect } from 'react';
import { getTimeSlots, getMockTimeSlots } from '../services/calendarService';
import './TimeSlotSelector.css';

const TimeSlotSelector = ({ selectedDate, onTimeSelect, selectedTime }) => {
  const [timeSlots, setTimeSlots] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // 選択された日付の時間枠を取得
  useEffect(() => {
    if (!selectedDate) {
      setTimeSlots([]);
      return;
    }

    const fetchTimeSlots = async () => {
      setLoading(true);
      setError('');
      
      // APIからデータを取得（失敗時はモックデータを使用）
      const result = await getTimeSlots(selectedDate);
      if (result.success) {
        setTimeSlots(result.data);
      } else {
        // APIが利用できない場合はモックデータを使用
        if (result.useMock) {
          const mockResult = getMockTimeSlots(selectedDate);
          setTimeSlots(mockResult.data);
        } else {
          setError(result.error || '時間枠の取得に失敗しました');
          setTimeSlots([]);
        }
      }
      setLoading(false);
    };

    fetchTimeSlots();
  }, [selectedDate]);

  // 時間帯を選択
  const handleTimeSelect = (timeSlot) => {
    if (timeSlot.status === 'full' || timeSlot.available === 0) {
      return;
    }
    if (onTimeSelect) {
      onTimeSelect(timeSlot.time);
    }
  };

  // ステータスに応じたクラス名を取得
  const getStatusClass = (status) => {
    switch (status) {
      case 'available':
        return 'time-slot-available';
      case 'limited':
        return 'time-slot-limited';
      case 'full':
        return 'time-slot-full';
      default:
        return '';
    }
  };

  // ステータスに応じたラベルを取得
  const getStatusLabel = (status) => {
    switch (status) {
      case 'available':
        return '空きあり';
      case 'limited':
        return '残りわずか';
      case 'full':
        return '満席';
      default:
        return '';
    }
  };

  if (!selectedDate) {
    return (
      <div className="time-slot-selector">
        <p className="time-slot-message">日付を選択してください</p>
      </div>
    );
  }

  return (
    <div className="time-slot-selector">
      <h3 className="time-slot-title">
        {selectedDate.toLocaleDateString('ja-JP', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        })}
        の予約可能時間
      </h3>

      {loading && <div className="time-slot-loading">読み込み中...</div>}
      {error && <div className="time-slot-error">{error}</div>}

      {!loading && timeSlots.length === 0 && (
        <p className="time-slot-message">この日は予約可能な時間がありません</p>
      )}

      {!loading && timeSlots.length > 0 && (
        <div className="time-slot-grid">
          {timeSlots.map((slot) => (
            <button
              key={slot.time}
              type="button"
              className={`time-slot-item ${getStatusClass(slot.status)} ${
                selectedTime === slot.time ? 'time-slot-selected' : ''
              }`}
              onClick={() => handleTimeSelect(slot)}
              disabled={slot.status === 'full' || slot.available === 0}
            >
              <div className="time-slot-time">{slot.time}</div>
              <div className="time-slot-status">{getStatusLabel(slot.status)}</div>
              <div className="time-slot-availability">
                残り {slot.available} / {slot.capacity}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default TimeSlotSelector;

