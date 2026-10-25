import sys, json
from client import AutonomousGraphqlQueryComplexityCalculatorClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    calculator = AutonomousGraphqlQueryComplexityCalculatorClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-autonomous-graphql-query-complexity-calculator-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    q = req.get("query", "{ user { id name } }")
    res = calculator.analyze_complexity(q)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
