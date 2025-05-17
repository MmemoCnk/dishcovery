// frontend/src/setupProxy.js

/**
 * ไฟล์นี้ช่วยในการตั้งค่า proxy สำหรับ React dev server 
 * เพื่อให้สามารถทำงานร่วมกับ Streamlit ในโหมดพัฒนาได้
 */

const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    ['/stream', '/favicon.ico', '/media'],
    createProxyMiddleware({
      target: 'http://localhost:8501', // Streamlit server port
      changeOrigin: true,
      ws: true,
    })
  );
};