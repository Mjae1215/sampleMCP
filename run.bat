@echo off
echo 🧮 계산기 MCP 서버 (FastMCP HTTP 방식)를 시작합니다...
echo.
echo 📦 의존성을 설치합니다...
pip install -r requirements.txt
echo.
echo 🚀 서버를 시작합니다...
echo.
echo 📍 서버 주소: http://localhost:8000
echo 📖 API 문서: http://localhost:8000/docs
echo 🔧 도구 목록: http://localhost:8000/tools
echo 🏥 상태 확인: http://localhost:8000/health
echo.
echo ========================================
python mcp_server.py
pause
