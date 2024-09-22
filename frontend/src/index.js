import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';  // 메인 컴포넌트 가져오기

// 애플리케이션 렌더링
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
