from typing import List, Dict
from models import DomainModel, LearnerModel, PedagogyModel

class Controller:
    def __init__(self, domain_model: DomainModel, pedagogy_model: PedagogyModel, questions: List[Dict]):
        self.domain_model = domain_model
        self.pedagogy_model = pedagogy_model
        self.questions = questions
        self.difficulty_points = {"easy": 1, "medium": 2, "hard": 3}
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
                        "correct_hard": 0, "total_hard": 0,
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
                            "correct_hard": 0, "total_hard": 0,
                            "points": 0
                        }
                    performance["topics"][leaf_topic]["total_questions"] += 1
                    if correct:
                        performance["topics"][leaf_topic][f"correct_{difficulty}"] += 1
                        performance["topics"][leaf_topic]["points"] += self.difficulty_points[difficulty]
                    performance["topics"][leaf_topic][f"total_{difficulty}"] += 1

        # Calculate percentages for topics
        for topic, data in performance["topics"].items():
            for diff in ["easy", "medium", "hard"]:
                total = data.get(f"total_{diff}", 0)
                correct = data.get(f"correct_{diff}", 0)
                data[f"percent_correct_{diff}_questions"] = (correct / total * 100) if total > 0 else 0.0
            # Clean up temporary counters
            del data["correct_easy"], data["total_easy"], data["correct_medium"], data["total_medium"], data["correct_hard"], data["total_hard"]

        # Calculate percentages for areas
        for area, data in performance["areas"].items():
            for diff in ["easy", "medium", "hard"]:
                total = data.get(f"total_{diff}", 0)
                correct = data.get(f"correct_{diff}", 0)
                data[f"percent_correct_{diff}_questions"] = (correct / total * 100) if total > 0 else 0.0
            del data["correct_easy"], data["total_easy"], data["correct_medium"], data["total_medium"], data["correct_hard"], data["total_hard"]

        learner.performance = performance
        self.learners.append(learner)
        return learner

    def apply_pedagogy(self, learner: LearnerModel) -> Dict:
        """Apply pedagogical rules to evaluate learner performance."""
        return self.pedagogy_model.apply_rules(learner)

    def generate_report(self, feedback_flags: Dict, learner_id: str) -> str:
        """Generate a human-readable report based on feedback flags."""
        report = f"Recommendation Report for {learner_id}\n\n"
        report += "**Topics to Review:**\n"
        for topic, flags in feedback_flags["topics"].items():
            if flags["needs_review"]:
                report += f"- {topic}: Performance below 50%. Consider reviewing this topic.\n"
            if flags.get("needs_hint"):
                report += f"  * Hint recommended for {topic}.\n"
            if flags.get("needs_visualization"):
                report += f"  * Visualization suggested for {topic}.\n"
        if not any(flags["needs_review"] for flags in feedback_flags["topics"].values()):
            report += "- No specific topics need review.\n"

        report += "\n**Areas to Focus On:**\n"
        for area, flags in feedback_flags["areas"].items():
            if flags["needs_focus"]:
                report += f"- {area}: Overall performance below 50%. Dedicate more time to this area.\n"
        if not any(flags["needs_focus"] for flags in feedback_flags["areas"].values()):
            report += "- All areas are performing satisfactorily.\n"
        return report

    def generate_learners(self, num_learners: int) -> List[LearnerModel]:
        """Generate a list of mock learners with random answers."""
        import random
        learners = []
        for i in range(1, num_learners + 1):
            answers = {q["id"]: random.choice("ABCDE") for q in self.questions}
            learners.append(LearnerModel(id=f"learner_{i}", answers=answers))
        return learners

    def generate_mock_reports(self, num_learners: int) -> None:
        """Generate learners, process them, and print their reports."""
        learners = self.generate_learners(num_learners)
        for learner in learners:
            learner = self.process_learner(learner)
            feedback_flags = self.apply_pedagogy(learner)
            report = self.generate_report(feedback_flags, learner.id)
            print(f"    Report for {learner.id}:\n{report}\n")