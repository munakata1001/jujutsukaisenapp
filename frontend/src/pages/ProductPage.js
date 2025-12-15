// 商品一覧ページ（画像表示対応の使用例）
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ProductList from '../components/ProductList';
import { getProducts } from '../services/productService';
import './ProductPage.css';

const ProductPage = () => {
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();
  const [products, setProducts] = useState([]);
  const [selectedProducts, setSelectedProducts] = useState({});
  const [loading, setLoading] = useState(true);

  // 認証チェック
  React.useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login');
    }
  }, [user, authLoading, navigate]);

  // 商品一覧を取得
  useEffect(() => {
    const fetchProducts = async () => {
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

    if (user) {
      fetchProducts();
    }
  }, [user]);

  // 商品選択時の処理
  const handleProductSelect = (productId, quantity) => {
    setSelectedProducts((prev) => ({
      ...prev,
      [productId]: quantity,
    }));
  };

  if (authLoading || loading) {
    return (
      <div className="product-page">
        <div className="loading-container">読み込み中...</div>
      </div>
    );
  }

  return (
    <div className="product-page">
      <div className="product-page-header">
        <h1 className="product-page-title">商品一覧</h1>
        <p className="product-page-subtitle">購入希望の商品を選択してください</p>
      </div>

      <ProductList
        products={products}
        selectedProducts={selectedProducts}
        onProductSelect={handleProductSelect}
      />

      {Object.keys(selectedProducts).length > 0 && (
        <div className="product-page-footer">
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
              合計: ¥
              {Object.entries(selectedProducts).reduce((sum, [productId, quantity]) => {
                const product = products.find((p) => p.product_id === productId);
                return sum + (product ? product.price * quantity : 0);
              }, 0).toLocaleString()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductPage;

