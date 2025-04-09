from pydantic import BaseModel, Field
from typing import Dict, Optional, Union
import yaml
import networkx as nx
import matplotlib.pyplot as plt
import requests

class DomainModel:

    def __init__(self, domain_file: str):
        try:
          with open(domain_file, 'r') as f:
            self.domain = yaml.safe_load(f)
        except:
          url = domain_file
          try:
              response = requests.get(url)
              response.raise_for_status()
              yaml_data = yaml.safe_load(response.text)
              self.domain = yaml_data
          except requests.exceptions.RequestException as e:
              print(f"Error fetching YAML from {url}: {e}")
              self.domain = None
          except yaml.YAMLError as e:
              print(f"Error parsing YAML from {url}: {e}")
              self.domain = None

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

    def plot(self, area=None, topico=None, root='Ciências da Natureza', simulate_colors=False):
        """Plot the domain hierarchy as a directed graph in a tree-like structure."""
        G = nx.DiGraph()

        # Build the graph
        if area:
            if topico:
                self._build_graph(G, {area: {topico: self.domain[root][area][topico]}})
            else:
                self._build_graph(G, {area: self.domain[root][area]})
        else:
            self._build_graph(G, self.domain[root])

        # Ensure the graph is acyclic
        if not nx.is_directed_acyclic_graph(G):
            raise ValueError("The graph contains cycles and cannot be plotted as a tree.")

        # Compute levels (depth) and topological order
        topo_order = list(nx.topological_sort(G))
        levels = {}  # Depth of each node
        for node in topo_order:
            levels[node] = max([levels.get(pred, 0) + 1 for pred in G.predecessors(node)], default=0)

        # Compute x-coordinates using a tree-like spacing strategy
        pos = {}
        x_positions = {}  # Track x-position for each node
        level_widths = {}  # Track the number of nodes per level for spacing

        # First pass: Assign initial x-positions based on order within each level
        for node in topo_order:
            level = levels[node]
            if level not in level_widths:
                level_widths[level] = 0
            x_positions[node] = level_widths[level]
            level_widths[level] += 1

        # Second pass: Adjust x-positions to center children under parents
        for node in reversed(topo_order):  # Bottom-up adjustment
            children = list(G.successors(node))
            if children:
                avg_child_x = sum(x_positions[child] for child in children) / len(children)
                x_positions[node] = avg_child_x
            pos[node] = (x_positions[node], -levels[node])  # Shortened edges

        # Normalize x-positions to avoid overlap
        max_width = max(level_widths.values())
        if max_width > 1:
            for node in pos:
                pos[node] = (pos[node][0] * 2.0 / (max_width - 1), pos[node][1])

        # Determine node colors
        if simulate_colors:
            num_nodes = G.number_of_nodes()
            colors = np.random.choice(
                ['#DC143C', '#FFD700', '#2E8B57'],
                size=num_nodes,
                p=[0.3, 0.4, 0.3]  # 30% red, 40% yellow, 30% green
            )
            node_color = colors
        else:
            node_color = "skyblue"  # Default color

        # Create a larger figure to accommodate the graph
        plt.figure(figsize=(12, 8))  # Increase figure size (width, height)

        # Draw nodes and edges
        nx.draw_networkx_nodes(G, pos, node_size=5000, node_color=node_color)
        nx.draw_networkx_edges(G, pos)

        # Draw rotated labels manually using Matplotlib
        for node, (x, y) in pos.items():
            plt.text(x, y, str(node), fontsize=10, fontweight="bold", 
                    ha='center', va='center', rotation=45)

        plt.title("Domain Model" if area and topico else "")

        # Adjust layout to prevent clipping
        plt.tight_layout()

        # Add extra padding to ensure labels aren't cut off
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        # Remove the border box (spines) and ticks
        ax = plt.gca()  # Get the current axes
        ax.set_frame_on(False)  # Turn off the frame (border box)
        ax.set_xticks([])  # Remove x-axis ticks
        ax.set_yticks([])  # Remove y-axis ticks

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
        # TODO improve this function
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
        try:
          with open(pedagogy_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
        except:
          url = pedagogy_file
          response = requests.get(url, headers={
              'Cache-Control': 'no-cache', # Or 'no-store'
              'Pragma': 'no-cache'         # Optional, for wider compatibility
          })
          response.raise_for_status()
          yaml_data = yaml.safe_load(response.text)

        self.feedback_types = yaml_data.get('feedback_types', [])
        self.rules = yaml_data.get('feedback_rules', [])
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
