from pydantic import BaseModel, Field
from typing import Dict, Optional, Union
import yaml
import networkx as nx
import matplotlib.pyplot as plt


class DomainModel:
    def __init__(self, domain_file: str):
        with open(domain_file, 'r') as f:
            self.domain = yaml.safe_load(f)

    def validate_topic_path(self, area: str, path: list) -> bool:
        """Validate if a topic path exists in the domain hierarchy."""
        current = self.domain.get(area, {})
        for part in path:
            if isinstance(current, dict):
                current = current.get(part, {})
            else:
                return False
        return True

    def print_domain(self, domain=None, indent=0):
        """Pretty print the domain hierarchy."""
        if domain is None:
            domain = self.domain
        for key, value in domain.items():
            print("  " * indent + key)
            if isinstance(value, dict):
                self.print_domain(value, indent + 1)
            elif isinstance(value, list):
                for item in value:
                    print("  " * (indent + 1) + "- " + item)

    def plot(self):
        """Plot the domain hierarchy as a directed graph."""
        G = nx.DiGraph()
        self._build_graph(G, self.domain)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold")
        plt.title("Domain Knowledge Graph")
        plt.show()

    def _build_graph(self, G, domain, parent=None):
        """Recursively build the graph from the domain dictionary."""
        for key, value in domain.items():
            G.add_node(key)
            if parent:
                G.add_edge(parent, key)
            if isinstance(value, dict):
                self._build_graph(G, value, key)
            elif isinstance(value, list):
                for item in value:
                    G.add_node(item)
                    G.add_edge(key, item)


class LearnerModel(BaseModel):
    id: str = Field(..., description="Unique identifier for the learner")
    answers: Dict[str, str] = Field(..., description="Answers to questions (question_id: A/B/C/D/E)")
    performance: Optional[Dict[str, Dict]] = Field(None, description="Performance metrics")

    def print_performance(self):
        """Pretty print the learner's performance metrics."""
        if not self.performance:
            print("No performance data available.")
            return
        print(f"Performance for {self.id}:")
        for category, metrics in self.performance.items():
            print(f"  {category.capitalize()}:")
            for key, value in metrics.items():
                print(f"    {key}: {value}")

    class Config:
        schema_extra = {
            "example": {
                "id": "learner_001",
                "answers": {"1": "A", "2": "B", "3": "C"},
                "performance": {
                    "topics": {
                        "Membrana Plasmática": {
                            "total_questions": 5,
                            "percent_correct_easy_questions": 80.0,
                            "percent_correct_medium_questions": 50.0,
                            "percent_correct_hard_questions": 33.3,
                            "points": 10
                        }
                    },
                    "areas": {
                        "Biologia": {
                            "total_questions": 60,
                            "percent_correct_easy_questions": 75.0,
                            "percent_correct_medium_questions": 60.0,
                            "percent_correct_hard_questions": 40.0,
                            "points": 80
                        }
                    }
                }
            }
        }


class PedagogyModel:
    def __init__(self, pedagogy_file: str, threshold_topics: float = 50.0, threshold_areas: float = 50.0):
        with open(pedagogy_file, 'r') as f:
            data = yaml.safe_load(f)
            self.feedback_types = data.get('feedback_types', [])
            self.rules = data.get('feedback_rules', [])
        self.threshold_topics = threshold_topics
        self.threshold_areas = threshold_areas
        
    def apply_rules(self, learner: LearnerModel) -> Dict:
        """Apply pedagogical rules to evaluate learner performance."""
        feedback = {"topics": {}, "areas": {}}

        # Initialize feedback for each topic and area
        if learner.performance:
            for topic in learner.performance.get("topics", {}):
                feedback["topics"][topic] = {"needs_review": False}
            for area in learner.performance.get("areas", {}):
                feedback["areas"][area] = {"needs_focus": False}

        # Check topics below threshold
        for topic, data in learner.performance.get("topics", {}).items():
            if data.get("percent_correct", 0) < self.threshold_topics:
                feedback["topics"][topic]["needs_review"] = True

        # Check areas below threshold
        for area, data in learner.performance.get("areas", {}).items():
            if data.get("percent_correct", 0) < self.threshold_areas:
                feedback["areas"][area]["needs_focus"] = True

        # Apply custom rules from pedagogy.yml
        if self.rules:
            for rule in self.rules:
                rule_name = rule.get("name", "Unnamed Rule")
                condition = rule.get("condition", {})
                if self._evaluate_condition(condition, learner):
                    action = rule.get("action", "")
                    action_parts = action.split("(")
                    action_type = action_parts[0]
                    if action_type == "provide_hint":
                        topic = action_parts[1].strip(")").strip("'").strip('"')
                        if topic in feedback["topics"]:
                            feedback["topics"][topic]["needs_hint"] = True
                    elif action_type == "suggest_visualization":
                        topic = action_parts[1].strip(")").strip("'").strip('"')
                        if topic in feedback["topics"]:
                            feedback["topics"][topic]["needs_visualization"] = True

        return feedback

    def _evaluate_condition(self, condition: Dict, learner: LearnerModel) -> bool:
        """Evaluate a rule condition recursively."""
        if not condition:
            return False
        condition_type = condition.get("type", "")
        if condition_type == "and":
            return all(self._evaluate_condition(cond, learner) for cond in condition.get("conditions", []))
        elif condition_type == "or":
            return any(self._evaluate_condition(cond, learner) for cond in condition.get("conditions", []))
        elif condition_type in ["less_than", "greater_than", "equal", "greater_than_or_equal", "less_than_or_equal"]:
            left_value = self._resolve_reference(condition.get("left", ""), learner)
            right_value = self._resolve_reference(condition.get("right", ""), learner)
            if left_value is None or right_value is None:
                return False
            if condition_type == "less_than":
                return left_value < right_value
            elif condition_type == "greater_than":
                return left_value > right_value
            elif condition_type == "equal":
                return left_value == right_value
            elif condition_type == "greater_than_or_equal":
                return left_value >= right_value
            elif condition_type == "less_than_or_equal":
                return left_value <= right_value
        return False

    def _resolve_reference(self, reference, learner: LearnerModel):
        """Resolve a reference to a value in the learner model."""
        if isinstance(reference, (int, float, bool)):
            return reference
        if not isinstance(reference, str):
            return None
        if reference.startswith("performance."):
            path = reference[11:].split(".")
            value = learner.performance
            for key in path:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return None
            return value
        return reference

    def print_rules(self):
        """Pretty print the pedagogical rules with readable conditions and actions."""
        print("Pedagogical Rules:")
        for rule in self.rules:
            print(f"  Rule: {rule.get('name', 'Unnamed')}")
            condition_str = self._format_condition(rule.get('condition', {}))
            print(f"    Condition: {condition_str}")
            print(f"    Action: {rule.get('action', 'No action specified')}")
            print()

    def _format_condition(self, condition):
        """Format a condition dictionary into a readable string."""
        if not condition:
            return "No condition"
        condition_type = condition.get("type", "")
        if condition_type in ["and", "or"]:
            sub_conditions = [self._format_condition(cond) for cond in condition.get("conditions", [])]
            return f" {condition_type.upper()} ".join(sub_conditions)
        elif condition_type in ["less_than", "greater_than", "equal", "greater_than_or_equal", "less_than_or_equal"]:
            left = condition.get("left", "unknown")
            right = condition.get("right", "unknown")
            operator = {
                "less_than": "<",
                "greater_than": ">",
                "equal": "==",
                "greater_than_or_equal": ">=",
                "less_than_or_equal": "<="
            }[condition_type]
            return f"{left} {operator} {right}"
        return str(condition)