from client import AutonomousGraphqlQueryComplexityCalculatorClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    calculator = AutonomousGraphqlQueryComplexityCalculatorClient(max_allowed_depth=5, max_allowed_complexity=180)
    print("=== AUTONOMOUS GRAPHQL QUERY COMPLEXITY CALCULATOR ===")
    
    # Complex query with nested relations and pagination multiplier
    query = """
    query GetOrganizationData {
      organization(id: "org_99") {
        id
        name
        departments(first: 5) {
          id
          title
          teams(first: 10) {
            id
            lead_name
            members {
              id
              email
            }
          }
        }
      }
    }
    """
    
    res = calculator.analyze_complexity(query)
    print()
    print(f"Evaluated Query Depth: {res['max_query_depth']} (Limit: {res['max_depth_threshold']})")
    print(f"Complexity Score: {res['calculated_complexity_score']} (Budget: {res['max_complexity_threshold']})")
    print(f"Compliant: Depth={res['is_depth_compliant']} | Cost={res['is_complexity_compliant']}")
    print(f"Gateway Decision: {res['gateway_action']}")

if __name__ == "__main__":
    main()
