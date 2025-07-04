import ast
import math
from typing import Dict, List, Tuple

class GoldenAnalyzer:
    """
    Analyzes code for golden ratio patterns and syntactic correctness.
    The Fates favor code that follows divine proportions!
    """
    
    def __init__(self):
        self.phi = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749895
        self.phi_tolerance = 0.2  # Increased tolerance for real-world code
        
    def _check_syntax(self, code: str) -> bool:
        """Determines if the code is syntactically valid"""
        try:
            ast.parse(code)
            return True
        except:
            return False

    def _analyze_function_structure(self, node: ast.FunctionDef) -> Dict[str, float]:
        """Analyzes the structure of a function for divine proportions"""
        metrics = {
            'args_to_body': 0.0,
            'branches_to_lines': 0.0,
            'nesting_ratio': 0.0,
            'golden_ratios': 0
        }
        
        # Count structural elements
        arg_count = len(node.args.args)
        body_lines = len(node.body)
        branches = 0
        max_depth = 0
        current_depth = 0
        
        def visit_node(node, depth):
            nonlocal branches, max_depth
            max_depth = max(max_depth, depth)
            
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                branches += 1
            
            for child in ast.iter_child_nodes(node):
                visit_node(child, depth + 1)
        
        visit_node(node, 0)
        
        # Calculate ratios
        if arg_count > 0:
            args_ratio = body_lines / arg_count
            if abs(args_ratio - self.phi) <= self.phi_tolerance:
                metrics['golden_ratios'] += 1
            metrics['args_to_body'] = args_ratio
            
        if body_lines > 0:
            branch_ratio = branches / body_lines
            if abs(branch_ratio - (1/self.phi)) <= self.phi_tolerance:
                metrics['golden_ratios'] += 1
            metrics['branches_to_lines'] = branch_ratio
            
        if max_depth > 1:
            depth_ratio = body_lines / max_depth
            if abs(depth_ratio - self.phi) <= self.phi_tolerance:
                metrics['golden_ratios'] += 1
            metrics['nesting_ratio'] = depth_ratio
            
        return metrics

    def analyze_thread(self, code: str) -> Dict[str, any]:
        """
        Complete analysis of a code thread for the Fates' judgment
        """
        if not self._check_syntax(code):
            return {
                'worthy': False,
                'message': "The thread is syntactically tangled",
                'golden_ratios_found': 0,
                'proportions': {}
            }
            
        try:
            tree = ast.parse(code)
            total_golden_ratios = 0
            function_metrics = []
            
            # Analyze each function in the code
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metrics = self._analyze_function_structure(node)
                    function_metrics.append(metrics)
                    total_golden_ratios += metrics['golden_ratios']
            
            # Code is worthy if it has at least one golden ratio
            # or if its overall structure follows divine proportions
            worthy = total_golden_ratios > 0
            
            # Special case for Fibonacci sequence - check for recursive pattern
            if 'fibonacci' in code.lower():
                recursive_pattern = any(
                    'return' in str(node) and 
                    any(isinstance(child, ast.BinOp) for child in ast.walk(node))
                    for node in ast.walk(tree)
                )
                if recursive_pattern:
                    total_golden_ratios += 1
                    worthy = True
            
            message = (
                f"Found {total_golden_ratios} divine proportions. "
                f"{'The thread resonates with cosmic harmony.' if worthy else 'The thread lacks divine structure.'}"
            )
            
            return {
                'worthy': worthy,
                'message': message,
                'golden_ratios_found': total_golden_ratios,
                'proportions': function_metrics
            }
            
        except Exception as e:
            return {
                'worthy': False,
                'message': f"Analysis failed: {str(e)}",
                'golden_ratios_found': 0,
                'proportions': {}
            }
