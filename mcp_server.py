from fastmcp import FastMCP
from pydantic import BaseModel
from typing import Dict, Any, List
import math
import statistics

# MCP 서버 인스턴스 생성
mcp = FastMCP("calculator-mcp")

# 계산 결과를 위한 응답 모델
class CalculationResponse(BaseModel):
    result: float
    operation: str
    a: float
    b: float
    message: str

# 통계 계산 결과를 위한 응답 모델
class StatisticsResponse(BaseModel):
    operation: str
    numbers: List[float]
    count: int
    results: Dict[str, float]
    message: str

# 덧셈 함수
@mcp.tool()
def add(a: float, b: float) -> CalculationResponse:
    """두 숫자를 더합니다."""
    result = a + b
    return CalculationResponse(
        result=result,
        operation="add",
        a=a,
        b=b,
        message=f"{a} + {b} = {result}"
    )

# 뺄셈 함수
@mcp.tool()
def subtract(a: float, b: float) -> CalculationResponse:
    """두 숫자에서 첫 번째 숫자에서 두 번째 숫자를 뺍니다."""
    result = a - b
    return CalculationResponse(
        result=result,
        operation="subtract",
        a=a,
        b=b,
        message=f"{a} - {b} = {result}"
    )

# 곱셈 함수
@mcp.tool()
def multiply(a: float, b: float) -> CalculationResponse:
    """두 숫자를 곱합니다."""
    result = a * b
    return CalculationResponse(
        result=result,
        operation="multiply",
        a=a,
        b=b,
        message=f"{a} × {b} = {result}"
    )

# 나눗셈 함수
@mcp.tool()
def divide(a: float, b: float) -> CalculationResponse:
    """첫 번째 숫자를 두 번째 숫자로 나눕니다."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    result = a / b
    return CalculationResponse(
        result=result,
        operation="divide",
        a=a,
        b=b,
        message=f"{a} ÷ {b} = {result}"
    )

# 복합 계산 함수
@mcp.tool()
def calculate(operation: str, a: float, b: float) -> CalculationResponse:
    """지정된 연산을 수행합니다. 지원되는 연산: add, subtract, multiply, divide"""
    operations = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
    }
    
    if operation not in operations:
        raise ValueError(f"지원되지 않는 연산입니다: {operation}. 지원되는 연산: {list(operations.keys())}")
    
    return operations[operation](a, b)

# 통계 계산 함수들
@mcp.tool()
def statistics_basic(numbers: List[float]) -> StatisticsResponse:
    """기본 통계를 계산합니다: 개수, 합계, 평균, 최대값, 최소값"""
    if not numbers:
        raise ValueError("숫자 목록이 비어있습니다.")
    
    count = len(numbers)
    total = sum(numbers)
    mean = total / count
    maximum = max(numbers)
    minimum = min(numbers)
    
    results = {
        "count": count,
        "sum": total,
        "mean": mean,
        "max": maximum,
        "min": minimum
    }
    
    return StatisticsResponse(
        operation="basic_statistics",
        numbers=numbers,
        count=count,
        results=results,
        message=f"숫자 {count}개의 기본 통계: 평균={mean:.2f}, 최대={maximum}, 최소={minimum}"
    )

@mcp.tool()
def statistics_advanced(numbers: List[float]) -> StatisticsResponse:
    """고급 통계를 계산합니다: 중앙값, 표준편차, 분산"""
    if not numbers:
        raise ValueError("숫자 목록이 비어있습니다.")
    
    if len(numbers) < 2:
        raise ValueError("고급 통계를 계산하려면 최소 2개 이상의 숫자가 필요합니다.")
    
    count = len(numbers)
    sorted_numbers = sorted(numbers)
    
    # 중앙값
    if count % 2 == 0:
        median = (sorted_numbers[count//2 - 1] + sorted_numbers[count//2]) / 2
    else:
        median = sorted_numbers[count//2]
    
    # 표준편차와 분산
    mean = sum(numbers) / count
    variance = sum((x - mean) ** 2 for x in numbers) / count
    std_dev = math.sqrt(variance)
    
    results = {
        "count": count,
        "median": median,
        "variance": variance,
        "std_deviation": std_dev,
        "mean": mean
    }
    
    return StatisticsResponse(
        operation="advanced_statistics",
        numbers=numbers,
        count=count,
        results=results,
        message=f"숫자 {count}개의 고급 통계: 중앙값={median:.2f}, 표준편차={std_dev:.2f}, 분산={variance:.2f}"
    )

@mcp.tool()
def statistics_full(numbers: List[float]) -> StatisticsResponse:
    """전체 통계를 계산합니다: 모든 기본 및 고급 통계"""
    if not numbers:
        raise ValueError("숫자 목록이 비어있습니다.")
    
    count = len(numbers)
    total = sum(numbers)
    mean = total / count
    maximum = max(numbers)
    minimum = min(numbers)
    
    # 중앙값
    sorted_numbers = sorted(numbers)
    if count % 2 == 0:
        median = (sorted_numbers[count//2 - 1] + sorted_numbers[count//2]) / 2
    else:
        median = sorted_numbers[count//2]
    
    # 표준편차와 분산
    variance = sum((x - mean) ** 2 for x in numbers) / count
    std_dev = math.sqrt(variance)
    
    # 범위
    range_val = maximum - minimum
    
    results = {
        "count": count,
        "sum": total,
        "mean": mean,
        "median": median,
        "max": maximum,
        "min": minimum,
        "range": range_val,
        "variance": variance,
        "std_deviation": std_dev
    }
    
    return StatisticsResponse(
        operation="full_statistics",
        numbers=numbers,
        count=count,
        results=results,
        message=f"숫자 {count}개의 전체 통계: 평균={mean:.2f}, 중앙값={median:.2f}, 표준편차={std_dev:.2f}, 범위={range_val}"
    )

# 수학 함수들
@mcp.tool()
def power(base: float, exponent: float) -> CalculationResponse:
    """거듭제곱을 계산합니다: base^exponent"""
    result = base ** exponent
    return CalculationResponse(
        result=result,
        operation="power",
        a=base,
        b=exponent,
        message=f"{base}^{exponent} = {result}"
    )

@mcp.tool()
def square_root(number: float) -> CalculationResponse:
    """제곱근을 계산합니다."""
    if number < 0:
        raise ValueError("음수의 제곱근은 계산할 수 없습니다.")
    result = math.sqrt(number)
    return CalculationResponse(
        result=result,
        operation="square_root",
        a=number,
        b=0,
        message=f"√{number} = {result}"
    )

@mcp.tool()
def factorial(n: int) -> CalculationResponse:
    """팩토리얼을 계산합니다: n!"""
    if n < 0:
        raise ValueError("음수의 팩토리얼은 계산할 수 없습니다.")
    if n > 20:
        raise ValueError("20보다 큰 수의 팩토리얼은 계산할 수 없습니다.")
    
    result = math.factorial(n)
    return CalculationResponse(
        result=float(result),
        operation="factorial",
        a=float(n),
        b=0,
        message=f"{n}! = {result}"
    )

# 서버 정보 및 상태 확인 (사람 확인용 - 선택사항)
@mcp.app.get("/")
async def root():
    """서버 기본 정보를 반환합니다."""
    return {
        "message": "계산기 MCP 서버에 오신 것을 환영합니다! 🧮",
        "version": "1.0.0",
        "status": "running",
        "available_tools": [
            {
                "name": "add",
                "description": "두 숫자 더하기",
                "endpoint": "/tools/add",
                "example": {"a": 10, "b": 5}
            },
            {
                "name": "subtract", 
                "description": "두 숫자 빼기",
                "endpoint": "/tools/subtract",
                "example": {"a": 10, "b": 3}
            },
            {
                "name": "multiply",
                "description": "두 숫자 곱하기",
                "endpoint": "/tools/multiply",
                "example": {"a": 6, "b": 7}
            },
            {
                "name": "divide",
                "description": "두 숫자 나누기",
                "endpoint": "/tools/divide",
                "example": {"a": 20, "b": 4}
            },
            {
                "name": "calculate",
                "description": "지정된 연산 수행",
                "endpoint": "/tools/calculate",
                "example": {"operation": "add", "a": 15, "b": 25}
            },
            {
                "name": "statistics_basic",
                "description": "기본 통계 계산 (개수, 합계, 평균, 최대값, 최소값)",
                "endpoint": "/tools/statistics_basic",
                "example": {"numbers": [1, 2, 3, 4, 5]}
            },
            {
                "name": "statistics_advanced",
                "description": "고급 통계 계산 (중앙값, 표준편차, 분산)",
                "endpoint": "/tools/statistics_advanced",
                "example": {"numbers": [1, 2, 3, 4, 5]}
            },
            {
                "name": "statistics_full",
                "description": "전체 통계 계산 (모든 통계)",
                "endpoint": "/tools/statistics_full",
                "example": {"numbers": [1, 2, 3, 4, 5]}
            },
            {
                "name": "power",
                "description": "거듭제곱 계산",
                "endpoint": "/tools/power",
                "example": {"base": 2, "exponent": 3}
            },
            {
                "name": "square_root",
                "description": "제곱근 계산",
                "endpoint": "/tools/square_root",
                "example": {"number": 16}
            },
            {
                "name": "factorial",
                "description": "팩토리얼 계산",
                "endpoint": "/tools/factorial",
                "example": {"n": 5}
            }
        ],
        "mcp_endpoints": {
            "tools_list": "/.well-known/mcp/tools",
            "tool_call": "/mcp/call/{tool}",
            "note": "MCP 에이전트는 위 엔드포인트를 사용합니다"
        }
    }

# 서버 상태 확인 (사람 확인용 - 선택사항)
@mcp.app.get("/health")
async def health_check():
    """서버 상태를 확인합니다."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "uptime": "running"
    }

# 사용 가능한 도구 목록 (사람 확인용 - 선택사항)
@mcp.app.get("/tools")
async def list_tools():
    """사용 가능한 모든 도구 목록을 반환합니다."""
    tools_info = [
        {
            "name": "add",
            "description": "두 숫자를 더합니다",
            "parameters": {
                "a": {"type": "float", "description": "첫 번째 숫자"},
                "b": {"type": "float", "description": "두 번째 숫자"}
            }
        },
        {
            "name": "subtract",
            "description": "두 숫자를 뺍니다",
            "parameters": {
                "a": {"type": "float", "description": "첫 번째 숫자"},
                "b": {"type": "float", "description": "두 번째 숫자"}
            }
        },
        {
            "name": "multiply",
            "description": "두 숫자를 곱합니다",
            "parameters": {
                "a": {"type": "float", "description": "첫 번째 숫자"},
                "b": {"type": "float", "description": "두 번째 숫자"}
            }
        },
        {
            "name": "divide",
            "description": "두 숫자를 나눕니다",
            "parameters": {
                "a": {"type": "float", "description": "첫 번째 숫자"},
                "b": {"type": "float", "description": "두 번째 숫자"}
            }
        },
        {
            "name": "calculate",
            "description": "지정된 연산을 수행합니다",
            "parameters": {
                "operation": {"type": "string", "description": "연산 종류 (add/subtract/multiply/divide)"},
                "a": {"type": "float", "description": "첫 번째 숫자"},
                "b": {"type": "float", "description": "두 번째 숫자"}
            }
        },
        {
            "name": "statistics_basic",
            "description": "기본 통계를 계산합니다",
            "parameters": {
                "numbers": {"type": "array", "description": "숫자 목록 (예: [1, 2, 3, 4, 5])"}
            }
        },
        {
            "name": "statistics_advanced",
            "description": "고급 통계를 계산합니다",
            "parameters": {
                "numbers": {"type": "array", "description": "숫자 목록 (최소 2개 이상)"}
            }
        },
        {
            "name": "statistics_full",
            "description": "전체 통계를 계산합니다",
            "parameters": {
                "numbers": {"type": "array", "description": "숫자 목록"}
            }
        },
        {
            "name": "power",
            "description": "거듭제곱을 계산합니다",
            "parameters": {
                "base": {"type": "float", "description": "밑수"},
                "exponent": {"type": "float", "description": "지수"}
            }
        },
        {
            "name": "square_root",
            "description": "제곱근을 계산합니다",
            "parameters": {
                "number": {"type": "float", "description": "양수"}
            }
        },
        {
            "name": "factorial",
            "description": "팩토리얼을 계산합니다",
            "parameters": {
                "n": {"type": "integer", "description": "0 이상 20 이하의 정수"}
            }
        }
    ]
    
    return {
        "tools": tools_info,
        "total_count": len(tools_info),
        "note": "이 엔드포인트는 사람 확인용입니다. MCP 에이전트는 /.well-known/mcp/tools를 사용합니다."
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 계산기 MCP 서버를 시작합니다...")
    print("📍 서버 주소: http://localhost:8000")
    print("📖 API 문서: http://localhost:8000/docs")
    print("🔧 사용 가능한 도구: http://localhost:8000/tools")
    print("=" * 50)
    print("🔗 MCP 표준 엔드포인트:")
    print("  📋 도구 목록: http://localhost:8000/.well-known/mcp/tools")
    print("  🚀 도구 실행: http://localhost:8000/mcp/call/{tool}")
    print("=" * 50)
    
    uvicorn.run(mcp.app, host="0.0.0.0", port=8000)
