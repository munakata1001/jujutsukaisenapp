// 商品関連APIサービス
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// 商品一覧を取得
export const getProducts = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/products`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data: data,
    };
  } catch (error) {
    console.error('商品一覧の取得に失敗:', error);
    return {
      success: false,
      error: error.message,
      data: [],
    };
  }
};

// 商品詳細を取得
export const getProduct = async (productId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/products/${productId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data: data,
    };
  } catch (error) {
    console.error('商品詳細の取得に失敗:', error);
    return {
      success: false,
      error: error.message,
      data: null,
    };
  }
};

// 商品の購入可能数を確認
export const checkProductAvailability = async (productId) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/products/${productId}/availability`,
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
    console.error('購入可能数の確認に失敗:', error);
    return {
      success: false,
      error: error.message,
      data: null,
    };
  }
};

