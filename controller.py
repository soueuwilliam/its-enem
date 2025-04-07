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
        """Generate a human-readable report based on feedback flags using messages from pedagogy.yml."""
        # Build a lookup dictionary for feedback messages from pedagogy_model
        feedback_messages = {ftype["name"]: ftype["message"] for ftype in self.pedagogy_model.feedback_types}

        report = f"Recommendation Report for {learner_id}\n\n"

        # Categorize topics and areas based on SDT feedback flags
        strengths_topics = [topic for topic in feedback_flags["topics"] if feedback_flags["topics"][topic].get("feedback_competence", 0) == 1]
        growth_topics = [topic for topic in feedback_flags["topics"] if feedback_flags["topics"][topic].get("feedback_autonomy", 0) == 1]
        focus_topics = [topic for topic in feedback_flags["topics"] if feedback_flags["topics"][topic].get("feedback_relatedness", 0) == 1]

        strengths_areas = [area for area in feedback_flags["areas"] if feedback_flags["areas"][area].get("feedback_competence", 0) == 1]
        growth_areas = [area for area in feedback_flags["areas"] if feedback_flags["areas"][area].get("feedback_autonomy", 0) == 1]
        focus_areas = [area for area in feedback_flags["areas"] if feedback_flags["areas"][area].get("feedback_relatedness", 0) == 1]

        # Your Strengths
        report += "**Your Strengths:**\n"
        for topic in strengths_topics:
            report += f"- {feedback_messages['competence'].format(item=topic)}\n"
        for area in strengths_areas:
            report += f"- {feedback_messages['competence'].format(item=area)}\n"
        if not strengths_topics and not strengths_areas:
            report += "- No specific strengths identified yet. Keep working!\n"

        # Opportunities for Growth
        report += "\n**Opportunities for Growth:**\n"
        for topic in growth_topics:
            report += f"- {feedback_messages['autonomy'].format(item=topic)}"
            if feedback_flags["topics"][topic].get("feedback_review", 0) == 1:
                report += f" {feedback_messages['review'].format(item=topic)}"
            report += "\n"
        for area in growth_areas:
            report += f"- {feedback_messages['autonomy'].format(item=area)}\n"
        if not growth_topics and not growth_areas:
            report += "- No specific opportunities for growth at this time.\n"

        # Areas to Focus On
        report += "\n**Areas to Focus On:**\n"
        for topic in focus_topics:
            report += f"- {feedback_messages['relatedness'].format(item=topic)}"
            if feedback_flags["topics"][topic].get("feedback_urgent", 0) == 1:
                report += f" {feedback_messages['urgent'].format(item=topic)}"
            if feedback_flags["topics"][topic].get("feedback_review", 0) == 1:
                report += f" {feedback_messages['review'].format(item=topic)}"
            report += "\n"
        for area in focus_areas:
            report += f"- {feedback_messages['relatedness'].format(item=area)}\n"
        if not focus_topics and not focus_areas:
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