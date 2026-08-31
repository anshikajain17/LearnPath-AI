def apply_assessment(skills, skill, score):
    old = float(skills.get(skill, 0))
    # Evidence-weighted update: recent assessment matters, but does not erase history.
    new = round(old * 0.35 + float(score) * 0.65, 1)
    skills[skill] = new
    return skills, old, new
