// 予約確認ページコンポーネント
import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getProducts } from '../services/productService';
import { createReservation } from '../services/reservationService';
import ProductList from '../components/ProductList';
import './ReservationConfirmPage.css';

const ReservationConfirmPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { user, loading: authLoading } = useAuth();
  
  const [products, setProducts] = useState([]);
  const [selectedProducts, setSelectedProducts] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  
  // フォームデータ
  const [formData, setFormData] = useState({
    user_name: '',
    user_phone: '',
  });

  // URLパラメータから日付と時間を取得
  const dateStr = searchParams.get('date');
  const timeStr = searchParams.get('time');

  // 認証チェック
  useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login');
    }
  }, [user, authLoading, navigate]);

  // 日付・時間のバリデーション
  useEffect(() => {
    if (!dateStr || !timeStr) {
      setError('日付と時間が指定されていません');
      navigate('/calendar');
    }
  }, [dateStr, timeStr, navigate]);

  // 商品一覧を取得
  useEffect(() => {
    const fetchProducts = async () => {
      if (!user) return;
      
      setLoading(true);
      const result = await getProducts();
      if (result.success) {
        setProducts(result.data || []);
      } else {
        console.error('商品一覧の取得に失敗:', result.error);
        setProducts([]);
      }
      setLoading(false);
    };

    if (user && dateStr && timeStr) {
      fetchProducts();
    }
  }, [user, dateStr, timeStr]);

  // 商品選択時の処理
  const handleProductSelect = (productId, quantity) => {
    setSelectedProducts((prev) => {
      const newState = { ...prev };
      if (quantity === 0) {
        delete newState[productId];
      } else {
        newState[productId] = quantity;
      }
      return newState;
    });
  };

  // フォーム入力の処理
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // 予約を確定
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // バリデーション
    if (!formData.user_name.trim()) {
      setError('お名前を入力してください');
      return;
    }

    if (!formData.user_phone.trim()) {
      setError('電話番号を入力してください');
      return;
    }

    // 電話番号の簡易バリデーション（数字、ハイフン、括弧のみ）
    const phoneRegex = /^[0-9-()]+$/;
    if (!phoneRegex.test(formData.user_phone)) {
      setError('電話番号の形式が正しくありません');
      return;
    }

    // 商品が選択されているかチェック（オプション）
    const hasSelectedProducts = Object.keys(selectedProducts).some(
      (productId) => selectedProducts[productId] > 0
    );

    setSubmitting(true);

    try {
      // 選択された商品を配列形式に変換
      const productsArray = Object.entries(selectedProducts)
        .filter(([_, quantity]) => quantity > 0)
        .map(([product_id, quantity]) => ({
          product_id,
          quantity: parseInt(quantity, 10),
        }));

      // 予約データを作成
      const reservationData = {
        user_email: user.email,
        user_name: formData.user_name.trim(),
        user_phone: formData.user_phone.trim(),
        visit_date: dateStr,
        visit_time: timeStr,
        products: productsArray,
      };

      const result = await createReservation(reservationData);

      if (result.success) {
        // 予約完了ページに遷移
        navigate(
          `/reservation-complete?reservation_id=${result.data.reservation_id}`
        );
      } else {
        setError(result.error || '予約の作成に失敗しました');
      }
    } catch (err) {
      console.error('予約作成エラー:', err);
      setError(err.message || '予約の作成に失敗しました');
    } finally {
      setSubmitting(false);
    }
  };

  if (authLoading || loading) {
    return (
      <div className="reservation-confirm-page">
        <div className="loading-container">読み込み中...</div>
      </div>
    );
  }

  if (!dateStr || !timeStr) {
    return (
      <div className="reservation-confirm-page">
        <div className="error-container">
          <h2>エラー</h2>
          <p>日付と時間が指定されていません</p>
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

  // 選択された商品の合計金額を計算
  const totalPrice = Object.entries(selectedProducts).reduce(
    (sum, [productId, quantity]) => {
      if (quantity === 0) return sum;
      const product = products.find((p) => p.product_id === productId);
      return sum + (product ? product.price * quantity : 0);
    },
    0
  );

  return (
    <div className="reservation-confirm-page">
      <div className="reservation-confirm-content">
        <h1 className="confirm-page-title">予約確認</h1>
        <p className="confirm-page-subtitle">
          以下の内容で予約を行います。内容をご確認の上、確定ボタンをクリックしてください。
        </p>

        {/* 予約日時情報 */}
        <div className="reservation-info-card">
          <h2 className="info-card-title">予約日時</h2>
          <div className="info-item">
            <span className="info-label">日付</span>
            <span className="info-value">
              {new Date(dateStr).toLocaleDateString('ja-JP', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                weekday: 'long',
              })}
            </span>
          </div>
          <div className="info-item">
            <span className="info-label">時間</span>
            <span className="info-value">{timeStr}</span>
          </div>
        </div>

        {/* 商品選択 */}
        <div className="product-selection-section">
          <h2 className="section-title">商品選択（任意）</h2>
          {products.length > 0 ? (
            <ProductList
              products={products}
              selectedProducts={selectedProducts}
              onProductSelect={handleProductSelect}
            />
          ) : (
            <p className="no-products-message">商品がありません</p>
          )}

          {Object.keys(selectedProducts).some(
            (productId) => selectedProducts[productId] > 0
          ) && (
            <div className="selected-products-summary">
              <h3>選択中の商品</h3>
              <ul>
                {Object.entries(selectedProducts).map(([productId, quantity]) => {
                  if (quantity === 0) return null;
                  const product = products.find((p) => p.product_id === productId);
                  if (!product) return null;
                  return (
                    <li key={productId}>
                      {product.name} × {quantity} = ¥
                      {(product.price * quantity).toLocaleString()}
                    </li>
                  );
                })}
              </ul>
              <div className="total-price">
                合計: ¥{totalPrice.toLocaleString()}
              </div>
            </div>
          )}
        </div>

        {/* お客様情報入力 */}
        <form className="reservation-form" onSubmit={handleSubmit}>
          <h2 className="section-title">お客様情報</h2>
          
          <div className="form-group">
            <label htmlFor="user_email" className="form-label">
              メールアドレス
            </label>
            <input
              type="email"
              id="user_email"
              name="user_email"
              value={user?.email || ''}
              disabled
              className="form-input disabled"
            />
            <p className="form-note">ログイン中のメールアドレスが使用されます</p>
          </div>

          <div className="form-group">
            <label htmlFor="user_name" className="form-label">
              お名前 <span className="required">必須</span>
            </label>
            <input
              type="text"
              id="user_name"
              name="user_name"
              value={formData.user_name}
              onChange={handleInputChange}
              required
              className="form-input"
              placeholder="山田 太郎"
            />
          </div>

          <div className="form-group">
            <label htmlFor="user_phone" className="form-label">
              電話番号 <span className="required">必須</span>
            </label>
            <input
              type="tel"
              id="user_phone"
              name="user_phone"
              value={formData.user_phone}
              onChange={handleInputChange}
              required
              className="form-input"
              placeholder="090-1234-5678"
            />
          </div>

          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}

          <div className="form-actions">
            <button
              type="button"
              className="cancel-button"
              onClick={() => navigate('/calendar')}
              disabled={submitting}
            >
              キャンセル
            </button>
            <button
              type="submit"
              className="submit-button"
              disabled={submitting}
            >
              {submitting ? '予約確定中...' : '予約を確定する'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ReservationConfirmPage;
