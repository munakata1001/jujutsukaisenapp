// 商品一覧コンポーネント（画像表示対応）
import React from 'react';
import ProductCard from './ProductCard';
import './ProductList.css';

const ProductList = ({ products, selectedProducts = {}, onProductSelect }) => {
  if (!products || products.length === 0) {
    return (
      <div className="product-list-empty">
        <p>商品がありません</p>
      </div>
    );
  }

  return (
    <div className="product-list">
      {products.map((product) => (
        <ProductCard
          key={product.product_id}
          product={product}
          onSelect={onProductSelect}
          selectedQuantity={selectedProducts[product.product_id] || 0}
        />
      ))}
    </div>
  );
};

export default ProductList;

