# 🧮 계산기 MCP 서버 (FastMCP HTTP 방식)

FastMCP를 사용하여 만든 HTTP 방식의 Model Context Protocol (MCP) 서버입니다. 기본적인 사칙연산부터 복잡한 통계 계산까지 다양한 수학 기능을 제공하며, 웹 API로 쉽게 접근할 수 있습니다.

## ✨ 주요 특징

- **🚀 FastMCP 기반**: 빠르고 현대적인 MCP 서버
- **🌐 HTTP API**: RESTful API 엔드포인트 제공
- **📖 자동 문서화**: Swagger UI와 ReDoc 지원
- **🔧 기본 계산**: add, subtract, multiply, divide
- **📊 통계 계산**: 기본/고급/전체 통계
- **🔢 수학 함수**: 거듭제곱, 제곱근, 팩토리얼
- **⚡ 실시간 응답**: JSON 형식의 구조화된 응답
- **🔗 MCP 표준 준수**: `/.well-known/mcp/tools`, `/mcp/call/{tool}` 자동 제공

## 🚀 빠른 시작

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
python mcp_server.py
```

### 3. 서버 접속
- **메인 서버**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **ReDoc 문서**: http://localhost:8000/redoc
- **도구 목록**: http://localhost:8000/tools
- **상태 확인**: http://localhost:8000/health

## 🔗 MCP 표준 엔드포인트 (에이전트용)

FastMCP가 자동으로 제공하는 표준 MCP 엔드포인트입니다:

- **`/.well-known/mcp/tools`** - 사용 가능한 도구 목록 조회
- **`/mcp/call/{tool}`** - 특정 도구 실행

이 엔드포인트들은 MCP 에이전트가 실제로 사용하는 표준 인터페이스입니다.

## 🔧 사용 가능한 도구

### 1. **기본 사칙연산**

#### 덧셈 (add)
```bash
# MCP 표준 방식 (에이전트용)
curl -X POST "http://localhost:8000/mcp/call/add" \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5}'

# 사용자 확인용 (선택사항)
curl -X POST "http://localhost:8000/tools/add" \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5}'
```

**응답:**
```json
{
  "result": 15,
  "operation": "add",
  "a": 10,
  "b": 5,
  "message": "10 + 5 = 15"
}
```

#### 뺄셈 (subtract)
```bash
curl -X POST "http://localhost:8000/mcp/call/subtract" \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 3}'
```

#### 곱셈 (multiply)
```bash
curl -X POST "http://localhost:8000/mcp/call/multiply" \
  -H "Content-Type: application/json" \
  -d '{"a": 6, "b": 7}'
```

#### 나눗셈 (divide)
```bash
curl -X POST "http://localhost:8000/mcp/call/divide" \
  -H "Content-Type: application/json" \
  -d '{"a": 20, "b": 4}'
```

#### 복합 계산 (calculate)
```bash
curl -X POST "http://localhost:8000/mcp/call/calculate" \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 15, "b": 25}'
```

### 2. **📊 통계 계산 도구**

#### 기본 통계 (statistics_basic)
```bash
curl -X POST "http://localhost:8000/mcp/call/statistics_basic" \
  -H "Content-Type: application/json" \
  -d '{"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}'
```

**응답:**
```json
{
  "operation": "basic_statistics",
  "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "count": 10,
  "results": {
    "count": 10,
    "sum": 55,
    "mean": 5.5,
    "max": 10,
    "min": 1
  },
  "message": "숫자 10개의 기본 통계: 평균=5.50, 최대=10, 최소=1"
}
```

#### 고급 통계 (statistics_advanced)
```bash
curl -X POST "http://localhost:8000/mcp/call/statistics_advanced" \
  -H "Content-Type: application/json" \
  -d '{"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}'
```

**응답:**
```json
{
  "operation": "advanced_statistics",
  "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "count": 10,
  "results": {
    "count": 10,
    "median": 5.5,
    "variance": 8.25,
    "std_deviation": 2.87,
    "mean": 5.5
  },
  "message": "숫자 10개의 고급 통계: 중앙값=5.50, 표준편차=2.87, 분산=8.25"
}
```

#### 전체 통계 (statistics_full)
```bash
curl -X POST "http://localhost:8000/mcp/call/statistics_full" \
  -H "Content-Type: application/json" \
  -d '{"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}'
```

**응답:**
```json
{
  "operation": "full_statistics",
  "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "count": 10,
  "results": {
    "count": 10,
    "sum": 55,
    "mean": 5.5,
    "median": 5.5,
    "max": 10,
    "min": 1,
    "range": 9,
    "variance": 8.25,
    "std_deviation": 2.87
  },
  "message": "숫자 10개의 전체 통계: 평균=5.50, 중앙값=5.50, 표준편차=2.87, 범위=9"
}
```

### 3. **🔢 수학 함수 도구**

#### 거듭제곱 (power)
```bash
curl -X POST "http://localhost:8000/mcp/call/power" \
  -H "Content-Type: application/json" \
  -d '{"base": 2, "exponent": 3}'
```

**응답:**
```json
{
  "result": 8,
  "operation": "power",
  "a": 2,
  "b": 3,
  "message": "2^3 = 8"
}
```

#### 제곱근 (square_root)
```bash
curl -X POST "http://localhost:8000/mcp/call/square_root" \
  -H "Content-Type: application/json" \
  -d '{"number": 16}'
```

**응답:**
```json
{
  "result": 4,
  "operation": "square_root",
  "a": 16,
  "b": 0,
  "message": "√16 = 4"
}
```

#### 팩토리얼 (factorial)
```bash
curl -X POST "http://localhost:8000/mcp/call/factorial" \
  -H "Content-Type: application/json" \
  -d '{"n": 5}'
```

**응답:**
```json
{
  "result": 120,
  "operation": "factorial",
  "a": 5,
  "b": 0,
  "message": "5! = 120"
}
```

## 📖 API 엔드포인트

### 🔗 MCP 표준 엔드포인트 (에이전트용)
| 엔드포인트 | 메서드 | 설명 |
|------------|--------|------|
| `/.well-known/mcp/tools` | GET | 사용 가능한 도구 목록 (MCP 표준) |
| `/mcp/call/{tool}` | POST | 특정 도구 실행 (MCP 표준) |

### 🌐 사용자 확인용 엔드포인트 (선택사항)
| 엔드포인트 | 메서드 | 설명 |
|------------|--------|------|
| `/` | GET | 서버 기본 정보 및 도구 목록 |
| `/health` | GET | 서버 상태 확인 |
| `/tools` | GET | 사용 가능한 도구 상세 정보 |
| `/docs` | GET | Swagger UI API 문서 |
| `/redoc` | GET | ReDoc API 문서 |

## 🧪 테스트

### 자동 테스트 실행
```bash
python test_server.py
```

### 수동 테스트
```bash
# MCP 표준 엔드포인트 테스트
curl http://localhost:8000/.well-known/mcp/tools

# 기본 통계 테스트 (MCP 표준)
curl -X POST "http://localhost:8000/mcp/call/statistics_basic" \
  -H "Content-Type: application/json" \
  -d '{"numbers": [10, 20, 30, 40, 50]}'

# 거듭제곱 테스트 (MCP 표준)
curl -X POST "http://localhost:8000/mcp/call/power" \
  -H "Content-Type: application/json" \
  -d '{"base": 3, "exponent": 4}'

# 사용자 확인용 엔드포인트 테스트
curl http://localhost:8000/health
curl http://localhost:8000/tools
```

## 🌐 웹 브라우저에서 테스트

1. **서버 실행**: `python mcp_server.py`
2. **브라우저에서 접속**: http://localhost:8000/docs
3. **Swagger UI**에서 각 도구를 직접 테스트 가능

## 📋 요구사항

- **Python**: 3.7+
- **FastMCP**: >=0.1.0
- **Uvicorn**: >=0.24.0
- **Pydantic**: >=2.0.0

## ⚠️ 주의사항

- **0으로 나누기**: `divide` 도구에서 `b=0`인 경우 오류 발생
- **숫자 입력**: 모든 매개변수는 숫자여야 함
- **지원 연산**: `add`, `subtract`, `multiply`, `divide`만 지원
- **통계 계산**: 빈 숫자 목록은 오류 발생
- **제곱근**: 음수 입력 시 오류 발생
- **팩토리얼**: 0 이상 20 이하의 정수만 지원

## 🔍 오류 코드

| 상태 코드 | 설명 |
|-----------|------|
| 200 | 성공 |
| 422 | 유효성 검사 오류 (잘못된 입력) |
| 500 | 서버 내부 오류 |

## 🚀 고급 사용법

### Python requests로 사용
```python
import requests

# MCP 표준 방식으로 기본 통계 계산
response = requests.post(
    "http://localhost:8000/mcp/call/statistics_basic",
    json={"numbers": [1, 2, 3, 4, 5]}
)
result = response.json()
print(f"평균: {result['results']['mean']}")
print(f"표준편차: {result['results']['std_deviation']}")

# MCP 표준 방식으로 거듭제곱 계산
response = requests.post(
    "http://localhost:8000/mcp/call/power",
    json={"base": 2, "exponent": 10}
)
result = response.json()
print(f"2^10 = {result['result']}")
```

### JavaScript fetch로 사용
```javascript
// MCP 표준 방식으로 전체 통계 계산
fetch('http://localhost:8000/mcp/call/statistics_full', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
})
.then(response => response.json())
.then(data => {
    console.log(data.message);
    console.log(`분산: ${data.results.variance}`);
    console.log(`범위: ${data.results.range}`);
});

// MCP 표준 방식으로 팩토리얼 계산
fetch('http://localhost:8000/mcp/call/factorial', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({n: 7})
})
.then(response => response.json())
.then(data => console.log(data.message));
```

## 📁 프로젝트 구조

```
sample_mcp/
├── mcp_server.py          # 메인 MCP 서버 (11개 도구)
├── test_server.py         # 테스트 스크립트
├── requirements.txt       # 의존성 목록
├── run.bat               # Windows 실행 스크립트
└── README.md             # 이 파일
```

## 🎯 다음 단계

- [x] 기본 사칙연산 도구
- [x] 통계 계산 도구 (기본/고급/전체)
- [x] 수학 함수 도구 (거듭제곱/제곱근/팩토리얼)
- [ ] 삼각함수 도구 (sin, cos, tan)
- [ ] 로그 함수 도구 (ln, log10)
- [ ] 단위 변환 도구
- [ ] 시간 계산 도구
- [ ] 기하학 계산 도구
- [ ] 계산 히스토리 저장
- [ ] 인증 및 권한 관리
- [ ] Docker 컨테이너화

---

**🎉 FastMCP로 만든 고급 계산기 MCP 서버를 즐겨보세요!**

**📊 총 11개의 다양한 수학 도구를 제공합니다:**
- 4개 기본 사칙연산
- 3개 통계 계산
- 3개 수학 함수
- 1개 복합 계산

**🔗 MCP 표준 엔드포인트:**
- `/.well-known/mcp/tools` - 도구 목록
- `/mcp/call/{tool}` - 도구 실행

**🌐 사용자 확인용 엔드포인트:**
- `/`, `/health`, `/tools` - 사람이 확인하기 위한 선택사항
