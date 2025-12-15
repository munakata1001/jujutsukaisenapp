// 予約関連APIサービス
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// ユーザーの予約一覧を取得
export const getUserReservations = async (userEmail) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/reservations?user_email=${encodeURIComponent(userEmail)}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data: data,
    };
  } catch (error) {
    console.error('予約一覧の取得に失敗:', error);
    return {
      success: false,
      error: error.message,
      data: [],
    };
  }
};

// 予約を作成
export const createReservation = async (reservationData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/reservations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(reservationData),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data: data,
    };
  } catch (error) {
    console.error('予約の作成に失敗:', error);
    return {
      success: false,
      error: error.message,
      data: null,
    };
  }
};

// 予約詳細を取得（予約番号で）
export const getReservationByNumber = async (reservationNumber) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/reservations/by-number/${encodeURIComponent(reservationNumber)}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      if (response.status === 404) {
        return {
          success: false,
          error: '予約が見つかりません',
          data: null,
        };
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data: data,
    };
  } catch (error) {
    console.error('予約詳細の取得に失敗:', error);
    return {
      success: false,
      error: error.message,
      data: null,
    };
  }
};

// 予約詳細を取得（IDで）
export const getReservation = async (reservationId) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/reservations/${encodeURIComponent(reservationId)}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      if (response.status === 404) {
        return {
          success: false,
          error: '予約が見つかりません',
          data: null,
        };
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data: data,
    };
  } catch (error) {
    console.error('予約詳細の取得に失敗:', error);
    return {
      success: false,
      error: error.message,
      data: null,
    };
  }
};

// 予約を更新
export const updateReservation = async (reservationId, updateData) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/reservations/${encodeURIComponent(reservationId)}`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData),
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data: data,
    };
  } catch (error) {
    console.error('予約の更新に失敗:', error);
    return {
      success: false,
      error: error.message,
      data: null,
    };
  }
};

// 予約をキャンセル
export const cancelReservation = async (reservationId) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/reservations/${encodeURIComponent(reservationId)}`,
      {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data: data,
    };
  } catch (error) {
    console.error('予約のキャンセルに失敗:', error);
    return {
      success: false,
      error: error.message,
      data: null,
    };
  }
};

// 予約を完了状態に更新
export const completeReservation = async (reservationId) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/reservations/${encodeURIComponent(reservationId)}/complete`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data: data,
    };
  } catch (error) {
    console.error('予約の完了処理に失敗:', error);
    return {
      success: false,
      error: error.message,
      data: null,
    };
  }
};
