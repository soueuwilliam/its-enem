from typing import List, Dict
from model.models import DomainModel, LearnerModel, PedagogyModel

class Controller:
    def __init__(self, domain_model: DomainModel, pedagogy_model: PedagogyModel, questions: List[Dict]):
        self.domain_model = domain_model
        self.pedagogy_model = pedagogy_model
        self.questions = questions
        self.difficulty_points = {"easy": 1, "medium": 2, "high": 3}
        self.learners = []

    def process_learner(self, learner: LearnerModel) -> LearnerModel:
        performance = {"topics": {}, "areas": {}}

        for q in self.questions:
            correct = learner.answers[q["id"]] == q["correct"]
            difficulty = q["difficulty"]

            # Process areas
            for area in q["topics"].keys():
                if area not in performance["areas"]:
                    performance["areas"][area] = {
                        "total_questions": 0,
                        "correct_easy": 0, "total_easy": 0,
                        "correct_medium": 0, "total_medium": 0,
                        "correct_high": 0, "total_high": 0,
                        "points": 0
                    }
                performance["areas"][area]["total_questions"] += 1
                if correct:
                    performance["areas"][area][f"correct_{difficulty}"] += 1
                    performance["areas"][area]["points"] += self.difficulty_points[difficulty]
                performance["areas"][area][f"total_{difficulty}"] += 1

            # Process topics
            for area, topic_paths in q["topics"].items():
                for path in topic_paths:
                    leaf_topic = path[-1]
                    if leaf_topic not in performance["topics"]:
                        performance["topics"][leaf_topic] = {
                            "total_questions": 0,
                            "correct_easy": 0, "total_easy": 0,
                            "correct_medium": 0, "total_medium": 0,
                            "correct_high": 0, "total_high": 0,
                            "points": 0
                        }
                    performance["topics"][leaf_topic]["total_questions"] += 1
                    if correct:
                        performance["topics"][leaf_topic][f"correct_{difficulty}"] += 1
                        performance["topics"][leaf_topic]["points"] += self.difficulty_points[difficulty]
                    performance["topics"][leaf_topic][f"total_{difficulty}"] += 1

        # Calculate percentages for topics
        for topic, data in performance["topics"].items():
            for diff in ["easy", "medium", "high"]:
                total = data.get(f"total_{diff}", 0)
                correct = data.get(f"correct_{diff}", 0)
                data[f"percent_correct_{diff}_questions"] = (correct / total * 100) if total > 0 else 0.0
            # Clean up temporary counters
            del data["correct_easy"], data["total_easy"], data["correct_medium"], data["total_medium"], data["correct_high"], data["total_high"]

        # Calculate percentages for areas
        for area, data in performance["areas"].items():
            for diff in ["easy", "medium", "high"]:
                total = data.get(f"total_{diff}", 0)
                correct = data.get(f"correct_{diff}", 0)
                data[f"percent_correct_{diff}_questions"] = (correct / total * 100) if total > 0 else 0.0
            del data["correct_easy"], data["total_easy"], data["correct_medium"], data["total_medium"], data["correct_high"], data["total_high"]

        learner.performance = performance
        self.learners.append(learner)
        return learner

    def apply_pedagogy(self, learner: LearnerModel) -> Dict:
        """Apply pedagogical rules to evaluate learner performance."""
        return self.pedagogy_model.apply_rules(learner)

    def generate_report(self, feedback_flags: Dict, learner_id: str) -> str:
        """Generate a human-readable report based on feedback flags using messages from pedagogy.yml."""
        # Create a lookup dictionary for feedback messages
        feedback_messages = {ftype["name"]: ftype["message"] for ftype in self.pedagogy_model.feedback_types}

        # Initialize the report
        report = f"Feedback Report for {learner_id}\n\n"

        # Topics section
        report += "**Feedback on Topics:**\n"
        topics_with_feedback = [
            topic for topic in feedback_flags["topics"]
            if feedback_flags["topics"][topic].get("needs_review", False)
        ]
        if topics_with_feedback:
            for topic in sorted(topics_with_feedback):
                report += f"- {feedback_messages['review'].format(item=topic)}\n"
        else:
            report += "- No topics require review at this time.\n"
        report += "\n"

        # Areas section
        report += "**Feedback on Areas:**\n"
        areas_with_feedback = [
            area for area in feedback_flags["areas"]
            if feedback_flags["areas"][area].get("needs_focus", False)
        ]
        if areas_with_feedback:
            for area in sorted(areas_with_feedback):
                report += f"- {feedback_messages['relatedness'].format(item=area)}\n"
        else:
            report += "- No areas need additional focus at this time.\n"

        return report