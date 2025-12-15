// 商品カードコンポーネント（画像表示対応）
import React from 'react';
import './ProductCard.css';

const ProductCard = ({ product, onSelect, selectedQuantity = 0 }) => {
  // 画像が存在しない場合のデフォルト画像URL（必要に応じて変更）
  const defaultImageUrl = '/images/default-product.png';
  const imageUrl = product.image_url || defaultImageUrl;

  return (
    <div className="product-card">
      <div className="product-image-container">
        <img
          src={imageUrl}
          alt={product.name}
          className="product-image"
          onError={(e) => {
            // 画像読み込みエラー時のフォールバック
            e.target.src = defaultImageUrl;
          }}
        />
      </div>
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        {product.description && (
          <p className="product-description">{product.description}</p>
        )}
        <div className="product-price">¥{product.price.toLocaleString()}</div>
        {onSelect && (
          <div className="product-selector">
            <label htmlFor={`quantity-${product.product_id}`}>
              数量:
            </label>
            <input
              id={`quantity-${product.product_id}`}
              type="number"
              min="0"
              max={product.max_per_reservation}
              value={selectedQuantity}
              onChange={(e) => onSelect(product.product_id, parseInt(e.target.value) || 0)}
              className="quantity-input"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductCard;

