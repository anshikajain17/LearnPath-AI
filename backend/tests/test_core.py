from app.services.goal_parser import parse_goal
from app.services.recommender import build_plan

def test_goal_parser():
    role, months, hours, known, target = parse_goal("Become an AI Engineer in 6 months. I know Python. I can study 2 hours a day.")
    assert role == "AI Engineer"
    assert months == 6
    assert hours == 2
    assert "Python" in known

def test_prerequisite_ordering():
    roadmap, _ = build_plan("MERN Developer", "Become a MERN developer in 5 months", {"JavaScript":80}, 2, 5)
    skills=[x["skill"] for x in roadmap]
    if "React" in skills and "JavaScript" in skills:
        assert skills.index("JavaScript") < skills.index("React")
