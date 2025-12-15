import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import CalendarPage from './pages/CalendarPage';
import ReservationConfirmPage from './pages/ReservationConfirmPage';
import ReservationCompletePage from './pages/ReservationCompletePage';
import MyPage from './pages/MyPage';
import './App.css';

// 認証が必要なページを保護するコンポーネント
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div style={{ color: '#fff', textAlign: 'center', padding: '50px' }}>読み込み中...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

// トップページコンポーネント
const HomePage = () => {
  const navigate = useNavigate();
  
  return (
    <div style={{ color: '#fff', padding: '20px', textAlign: 'center' }}>
      <h1>呪術廻戦ポップアップショップ</h1>
      <p style={{ marginBottom: '30px' }}>予約カレンダーへようこそ</p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', alignItems: 'center' }}>
        <button
          onClick={() => navigate('/calendar')}
          style={{
            background: 'linear-gradient(135deg, #4a90e2 0%, #357abd 100%)',
            border: 'none',
            borderRadius: '8px',
            color: '#fff',
            fontSize: '16px',
            fontWeight: '600',
            padding: '14px 32px',
            cursor: 'pointer',
            width: '250px',
          }}
        >
          予約カレンダーを開く
        </button>
        <button
          onClick={() => navigate('/mypage')}
          style={{
            background: 'rgba(255, 255, 255, 0.1)',
            border: '1px solid rgba(255, 255, 255, 0.3)',
            borderRadius: '8px',
            color: '#fff',
            fontSize: '16px',
            fontWeight: '600',
            padding: '14px 32px',
            cursor: 'pointer',
            width: '250px',
          }}
        >
          マイページ
        </button>
      </div>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route 
              path="/calendar" 
              element={
                <ProtectedRoute>
                  <CalendarPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/reservation" 
              element={
                <ProtectedRoute>
                  <ReservationConfirmPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/reservation-complete" 
              element={
                <ProtectedRoute>
                  <ReservationCompletePage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/mypage" 
              element={
                <ProtectedRoute>
                  <MyPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <HomePage />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

