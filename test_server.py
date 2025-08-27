import requests
import json
import time

# 서버 기본 URL
BASE_URL = "http://localhost:8000"

def test_server_info():
    """서버 기본 정보 테스트"""
    print("🔍 서버 정보 테스트")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ 서버 정보 조회 성공")
            print(f"  메시지: {data.get('message')}")
            print(f"  버전: {data.get('version')}")
            print(f"  상태: {data.get('status')}")
            print(f"  사용 가능한 도구: {len(data.get('available_tools', []))}개")
            
            # MCP 표준 엔드포인트 정보 출력
            mcp_endpoints = data.get('mcp_endpoints', {})
            if mcp_endpoints:
                print("  🔗 MCP 표준 엔드포인트:")
                print(f"    도구 목록: {mcp_endpoints.get('tools_list')}")
                print(f"    도구 실행: {mcp_endpoints.get('tool_call')}")
        else:
            print(f"❌ 서버 정보 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 서버 정보 조회 오류: {e}")

def test_health_check():
    """서버 상태 확인 테스트"""
    print("\n🏥 서버 상태 확인 테스트")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ 서버 상태 확인 성공")
            print(f"  상태: {data.get('status')}")
            print(f"  타임스탬프: {data.get('timestamp')}")
        else:
            print(f"❌ 서버 상태 확인 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 서버 상태 확인 오류: {e}")

def test_mcp_standard_endpoints():
    """MCP 표준 엔드포인트 테스트"""
    print("\n🔗 MCP 표준 엔드포인트 테스트")
    print("-" * 40)
    
    # MCP 도구 목록 조회
    print("MCP 도구 목록 조회:")
    try:
        response = requests.get(f"{BASE_URL}/.well-known/mcp/tools")
        if response.status_code == 200:
            data = response.json()
            tools = data.get('tools', [])
            print(f"  ✅ 성공: {len(tools)}개 도구 발견")
            for tool in tools:
                print(f"    - {tool.get('name')}: {tool.get('description')}")
        else:
            print(f"  ❌ 실패: {response.status_code}")
            print(f"  오류: {response.text}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")

def test_tools_list():
    """도구 목록 조회 테스트 (사용자 확인용)"""
    print("\n📋 도구 목록 조회 테스트 (사용자 확인용)")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/tools")
        if response.status_code == 200:
            data = response.json()
            tools = data.get('tools', [])
            print(f"✅ 도구 목록 조회 성공 (총 {data.get('total_count')}개)")
            print(f"  참고: {data.get('note', '')}")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
                print(f"    매개변수: {tool['parameters']}")
        else:
            print(f"❌ 도구 목록 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 도구 목록 조회 오류: {e}")

def test_calculation_tools():
    """계산 도구들 테스트 (MCP 표준 엔드포인트 사용)"""
    print("\n🧮 계산 도구 테스트 (MCP 표준 엔드포인트)")
    print("-" * 40)
    
    test_cases = [
        ("add", {"a": 10, "b": 5}, "15"),
        ("subtract", {"a": 10, "b": 3}, "7"),
        ("multiply", {"a": 6, "b": 7}, "42"),
        ("divide", {"a": 20, "b": 4}, "5.0")
    ]
    
    for tool_name, params, expected in test_cases:
        print(f"\n{tool_name} 도구 테스트:")
        try:
            response = requests.post(
                f"{BASE_URL}/mcp/call/{tool_name}",
                headers={"Content-Type": "application/json"},
                data=json.dumps(params)
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('result')
                message = data.get('message')
                print(f"  ✅ 성공: {message}")
                print(f"  결과: {result} (예상: {expected})")
            else:
                print(f"  ❌ 실패: {response.status_code}")
                print(f"  오류: {response.text}")
        except Exception as e:
            print(f"  ❌ 오류: {e}")

def test_calculate_tool():
    """복합 계산 도구 테스트 (MCP 표준 엔드포인트 사용)"""
    print("\n🔄 복합 계산 도구 테스트 (MCP 표준 엔드포인트)")
    print("-" * 40)
    
    test_cases = [
        ({"operation": "add", "a": 15, "b": 25}, "40"),
        ({"operation": "subtract", "a": 100, "b": 30}, "70"),
        ({"operation": "multiply", "a": 8, "b": 9}, "72"),
        ({"operation": "divide", "a": 50, "b": 10}, "5.0")
    ]
    
    for params, expected in test_cases:
        operation = params['operation']
        print(f"\n{operation} 연산 테스트:")
        try:
            response = requests.post(
                f"{BASE_URL}/mcp/call/calculate",
                headers={"Content-Type": "application/json"},
                data=json.dumps(params)
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('result')
                message = data.get('message')
                print(f"  ✅ 성공: {message}")
                print(f"  결과: {result} (예상: {expected})")
            else:
                print(f"  ❌ 실패: {response.status_code}")
                print(f"  오류: {response.text}")
        except Exception as e:
            print(f"  ❌ 오류: {e}")

def test_statistics_tools():
    """통계 계산 도구들 테스트 (MCP 표준 엔드포인트 사용)"""
    print("\n📊 통계 계산 도구 테스트 (MCP 표준 엔드포인트)")
    print("-" * 40)
    
    test_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 기본 통계 테스트
    print("\n기본 통계 테스트:")
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/call/statistics_basic",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"numbers": test_numbers})
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', {})
            print(f"  ✅ 성공: {data.get('message')}")
            print(f"  개수: {results.get('count')}")
            print(f"  합계: {results.get('sum')}")
            print(f"  평균: {results.get('mean'):.2f}")
            print(f"  최대값: {results.get('max')}")
            print(f"  최소값: {results.get('min')}")
        else:
            print(f"  ❌ 실패: {response.status_code}")
            print(f"  오류: {response.text}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")
    
    # 고급 통계 테스트
    print("\n고급 통계 테스트:")
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/call/statistics_advanced",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"numbers": test_numbers})
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', {})
            print(f"  ✅ 성공: {data.get('message')}")
            print(f"  중앙값: {results.get('median')}")
            print(f"  분산: {results.get('variance'):.2f}")
            print(f"  표준편차: {results.get('std_deviation'):.2f}")
        else:
            print(f"  ❌ 실패: {response.status_code}")
            print(f"  오류: {response.text}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")
    
    # 전체 통계 테스트
    print("\n전체 통계 테스트:")
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/call/statistics_full",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"numbers": test_numbers})
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', {})
            print(f"  ✅ 성공: {data.get('message')}")
            print(f"  범위: {results.get('range')}")
            print(f"  모든 통계: {results}")
        else:
            print(f"  ❌ 실패: {response.status_code}")
            print(f"  오류: {response.text}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")

def test_math_functions():
    """수학 함수 도구들 테스트 (MCP 표준 엔드포인트 사용)"""
    print("\n🔢 수학 함수 도구 테스트 (MCP 표준 엔드포인트)")
    print("-" * 40)
    
    # 거듭제곱 테스트
    print("\n거듭제곱 테스트:")
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/call/power",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"base": 2, "exponent": 3})
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('result')
            message = data.get('message')
            print(f"  ✅ 성공: {message}")
            print(f"  결과: {result}")
        else:
            print(f"  ❌ 실패: {response.status_code}")
            print(f"  오류: {response.text}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")
    
    # 제곱근 테스트
    print("\n제곱근 테스트:")
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/call/square_root",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"number": 16})
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('result')
            message = data.get('message')
            print(f"  ✅ 성공: {message}")
            print(f"  결과: {result}")
        else:
            print(f"  ❌ 실패: {response.status_code}")
            print(f"  오류: {response.text}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")
    
    # 팩토리얼 테스트
    print("\n팩토리얼 테스트:")
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/call/factorial",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"n": 5})
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('result')
            message = data.get('message')
            print(f"  ✅ 성공: {message}")
            print(f"  결과: {result}")
        else:
            print(f"  ❌ 실패: {response.status_code}")
            print(f"  오류: {response.text}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")

def test_error_cases():
    """오류 케이스 테스트 (MCP 표준 엔드포인트 사용)"""
    print("\n⚠️ 오류 케이스 테스트 (MCP 표준 엔드포인트)")
    print("-" * 40)
    
    # 0으로 나누기
    print("0으로 나누기 테스트:")
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/call/divide",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"a": 10, "b": 0})
        )
        if response.status_code == 422:  # FastMCP는 validation error를 422로 반환
            print("  ✅ 예상된 오류 발생 (0으로 나누기)")
        else:
            print(f"  ❌ 예상치 못한 응답: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")
    
    # 잘못된 연산
    print("\n잘못된 연산 테스트:")
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/call/calculate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"operation": "invalid", "a": 10, "b": 5})
        )
        if response.status_code == 422:
            print("  ✅ 예상된 오류 발생 (잘못된 연산)")
        else:
            print(f"  ❌ 예상치 못한 응답: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")
    
    # 빈 숫자 목록
    print("\n빈 숫자 목록 테스트:")
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/call/statistics_basic",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"numbers": []})
        )
        if response.status_code == 422:
            print("  ✅ 예상된 오류 발생 (빈 숫자 목록)")
        else:
            print(f"  ❌ 예상치 못한 응답: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")
    
    # 음수 제곱근
    print("\n음수 제곱근 테스트:")
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/call/square_root",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"number": -4})
        )
        if response.status_code == 422:
            print("  ✅ 예상된 오류 발생 (음수 제곱근)")
        else:
            print(f"  ❌ 예상치 못한 응답: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 오류: {e}")

def test_api_documentation():
    """API 문서 접근 테스트"""
    print("\n📖 API 문서 접근 테스트")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API 문서 접근 성공")
            print("  📖 Swagger UI: http://localhost:8000/docs")
            print("  📚 ReDoc: http://localhost:8000/redoc")
        else:
            print(f"❌ API 문서 접근 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ API 문서 접근 오류: {e}")

def main():
    """메인 테스트 함수"""
    print("🚀 HTTP MCP 서버 테스트 시작")
    print("=" * 60)
    
    # 서버가 실행 중인지 확인
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 서버가 실행 중입니다")
        else:
            print("❌ 서버 응답이 예상과 다릅니다")
            return
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. 서버를 먼저 실행해주세요.")
        print("  실행 명령: python mcp_server.py")
        return
    except Exception as e:
        print(f"❌ 서버 연결 오류: {e}")
        return
    
    # 테스트 실행
    test_server_info()
    test_health_check()
    test_mcp_standard_endpoints()
    test_tools_list()
    test_calculation_tools()
    test_calculate_tool()
    test_statistics_tools()
    test_math_functions()
    test_error_cases()
    test_api_documentation()
    
    print("\n" + "=" * 60)
    print("✨ 모든 테스트가 완료되었습니다!")
    print("\n🔗 유용한 링크:")
    print(f"  🌐 서버: {BASE_URL}")
    print(f"  📖 API 문서: {BASE_URL}/docs")
    print(f"  🔧 도구 목록: {BASE_URL}/tools")
    print(f"  🏥 상태 확인: {BASE_URL}/health")
    print(f"  🔗 MCP 표준 엔드포인트:")
    print(f"    📋 도구 목록: {BASE_URL}/.well-known/mcp/tools")
    print(f"    🚀 도구 실행: {BASE_URL}/mcp/call/{{tool}}")

if __name__ == "__main__":
    main()
