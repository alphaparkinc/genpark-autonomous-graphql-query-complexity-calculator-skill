import re, sys
sys.stdout.reconfigure(encoding='utf-8')

class AutonomousGraphqlQueryComplexityCalculatorClient:
    """
    GraphQL AST complexity estimator. Evaluates query nesting depth, field multiplier weights,
    pagination arguments (first, limit), and enforces maximum query budget limits.
    """
    def __init__(self, max_allowed_depth=6, max_allowed_complexity=250):
        self.max_depth = max_allowed_depth
        self.max_complexity = max_allowed_complexity

    def analyze_complexity(self, query_string):
        cleaned = re.sub(r'#[^\n]*', '', query_string).strip()
        
        # Calculate maximum nesting depth by tracking curly brace indentation
        max_depth = 0
        current_depth = 0
        complexity_score = 0
        depth_multipliers = [1]

        # Tokenize lines/elements
        lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
        
        for line in lines:
            # Check opening braces
            open_count = line.count('{')
            close_count = line.count('}')

            # Look for pagination multipliers e.g. users(first: 20) or items(limit: 50)
            mult_match = re.search(r'(first|limit)\s*:\s*(\d+)', line)
            multiplier = int(mult_match.group(2)) if mult_match else 1

            if open_count > 0:
                for _ in range(open_count):
                    current_depth += 1
                    if current_depth > max_depth:
                        max_depth = current_depth
                    # Apply multiplier down the hierarchy
                    depth_multipliers.append(depth_multipliers[-1] * multiplier)
            
            # Simple field counting: count words in line
            words = re.findall(r'[a-zA-Z0-9_]+', line)
            reserved = {"query", "mutation", "subscription", "fragment", "on", "first", "limit", "offset", "after"}
            field_words = [w for w in words if w.lower() not in reserved and not w.isdigit()]
            
            curr_mult = depth_multipliers[-1] if depth_multipliers else 1
            complexity_score += len(field_words) * curr_mult

            if close_count > 0:
                for _ in range(close_count):
                    current_depth = max(0, current_depth - 1)
                    if len(depth_multipliers) > 1:
                        depth_multipliers.pop()

        is_depth_exceeded = max_depth > self.max_depth
        is_complexity_exceeded = complexity_score > self.max_complexity
        is_safe = not is_depth_exceeded and not is_complexity_exceeded

        action = "EXECUTE_QUERY" if is_safe else "REJECT_QUERY_COST_OVERFLOW"

        return {
            "status": "success",
            "evaluated_query_length": len(query_string),
            "max_query_depth": max_depth,
            "max_depth_threshold": self.max_depth,
            "calculated_complexity_score": complexity_score,
            "max_complexity_threshold": self.max_complexity,
            "is_depth_compliant": not is_depth_exceeded,
            "is_complexity_compliant": not is_complexity_exceeded,
            "gateway_action": action
        }
