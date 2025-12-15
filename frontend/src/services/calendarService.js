// カレンダー関連のAPI呼び出し
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// カレンダーデータを取得（月次）
export const getCalendarData = async (year, month) => {
  try {
    // monthは0-11で来るので、APIが1-12を期待する場合は+1する
    // ここではAPIが1-12を期待すると仮定（必要に応じて調整）
    const apiMonth = month + 1;
    const response = await fetch(`${API_URL}/api/calendar?year=${year}&month=${apiMonth}`);
    
    // 400エラーや404エラーの場合は、バックエンドが未実装と判断してモックデータを使用
    if (!response.ok) {
      if (response.status === 400 || response.status === 404) {
        console.warn('APIエンドポイントが利用できません。モックデータを使用します。');
        return { success: false, error: 'API未実装', useMock: true };
      }
      const errorText = await response.text();
      throw new Error(`カレンダーデータの取得に失敗しました: ${response.status} ${errorText}`);
    }
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    // ネットワークエラーやCORSエラーの場合もモックデータを使用
    if (error.name === 'TypeError' || error.message.includes('Failed to fetch')) {
      console.warn('APIサーバーに接続できません。モックデータを使用します。');
      return { success: false, error: 'APIサーバー未接続', useMock: true };
    }
    console.error('カレンダーデータ取得エラー:', error);
    return { success: false, error: error.message, useMock: true };
  }
};

// 指定日の予約可能枠を取得
export const getTimeSlots = async (date) => {
  try {
    const dateStr = date.toISOString().split('T')[0];
    const response = await fetch(`${API_URL}/api/timeslots?date=${dateStr}`);
    
    // 400エラーや404エラーの場合は、バックエンドが未実装と判断してモックデータを使用
    if (!response.ok) {
      if (response.status === 400 || response.status === 404) {
        console.warn('APIエンドポイントが利用できません。モックデータを使用します。');
        return { success: false, error: 'API未実装', useMock: true };
      }
      const errorText = await response.text();
      throw new Error(`予約可能枠の取得に失敗しました: ${response.status} ${errorText}`);
    }
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    // ネットワークエラーやCORSエラーの場合もモックデータを使用
    if (error.name === 'TypeError' || error.message.includes('Failed to fetch')) {
      console.warn('APIサーバーに接続できません。モックデータを使用します。');
      return { success: false, error: 'APIサーバー未接続', useMock: true };
    }
    console.error('予約可能枠取得エラー:', error);
    return { success: false, error: error.message, useMock: true };
  }
};

// 空き状況を確認
export const checkAvailability = async (date, time) => {
  try {
    const dateStr = date.toISOString().split('T')[0];
    const response = await fetch(
      `${API_URL}/api/timeslots/availability?date=${dateStr}&time=${time}`
    );
    if (!response.ok) {
      throw new Error('空き状況の確認に失敗しました');
    }
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error('空き状況確認エラー:', error);
    return { success: false, error: error.message };
  }
};

// デモ用のモックデータ（APIが利用できない場合）
export const getMockCalendarData = (year, month) => {
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const data = {};
  
  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month, day);
    // 過去の日付は予約不可
    if (date < new Date()) {
      data[day] = { status: 'past', availableSlots: 0 };
    } else {
      // ランダムに予約状況を設定（デモ用）
      const random = Math.random();
      if (random < 0.3) {
        data[day] = { status: 'available', availableSlots: 5 };
      } else if (random < 0.6) {
        data[day] = { status: 'limited', availableSlots: 2 };
      } else {
        data[day] = { status: 'full', availableSlots: 0 };
      }
    }
  }
  
  return { success: true, data };
};

// デモ用のモック時間枠データ
export const getMockTimeSlots = (date) => {
  const timeSlots = [
    { time: '10:00', capacity: 10, reserved: 3, available: 7, status: 'available' },
    { time: '11:00', capacity: 10, reserved: 5, available: 5, status: 'available' },
    { time: '12:00', capacity: 10, reserved: 8, available: 2, status: 'limited' },
    { time: '13:00', capacity: 10, reserved: 10, available: 0, status: 'full' },
    { time: '14:00', capacity: 10, reserved: 4, available: 6, status: 'available' },
    { time: '15:00', capacity: 10, reserved: 6, available: 4, status: 'available' },
    { time: '16:00', capacity: 10, reserved: 9, available: 1, status: 'limited' },
    { time: '17:00', capacity: 10, reserved: 7, available: 3, status: 'available' },
  ];
  
  return { success: true, data: timeSlots };
};

