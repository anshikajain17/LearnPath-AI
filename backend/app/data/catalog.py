SKILLS = {
    "Python": {"domain": "Programming", "difficulty": 2},
    "JavaScript": {"domain": "Programming", "difficulty": 2},
    "HTML/CSS": {"domain": "Web", "difficulty": 1},
    "Git/GitHub": {"domain": "Tools", "difficulty": 1},
    "SQL": {"domain": "Data", "difficulty": 2},
    "React": {"domain": "Web", "difficulty": 3},
    "Node.js": {"domain": "Backend", "difficulty": 3},
    "FastAPI": {"domain": "Backend", "difficulty": 3},
    "REST APIs": {"domain": "Backend", "difficulty": 3},
    "MongoDB": {"domain": "Data", "difficulty": 2},
    "PostgreSQL": {"domain": "Data", "difficulty": 3},
    "Statistics": {"domain": "AI", "difficulty": 3},
    "NumPy/Pandas": {"domain": "AI", "difficulty": 2},
    "Machine Learning": {"domain": "AI", "difficulty": 4},
    "Deep Learning": {"domain": "AI", "difficulty": 5},
    "NLP": {"domain": "AI", "difficulty": 4},
    "LLMs": {"domain": "AI", "difficulty": 4},
    "MLOps": {"domain": "Cloud", "difficulty": 5},
    "Docker": {"domain": "Cloud", "difficulty": 3},
    "System Design": {"domain": "Architecture", "difficulty": 5},
    "DSA": {"domain": "Computer Science", "difficulty": 4},
}

ROLE_SKILLS = {
    "AI Engineer": ["Python","Statistics","NumPy/Pandas","Machine Learning","Deep Learning","LLMs","MLOps","Docker","Git/GitHub","SQL"],
    "ML Engineer": ["Python","Statistics","NumPy/Pandas","Machine Learning","Deep Learning","MLOps","Docker","SQL","Git/GitHub"],
    "Data Scientist": ["Python","Statistics","NumPy/Pandas","SQL","Machine Learning","Git/GitHub"],
    "MERN Developer": ["HTML/CSS","JavaScript","React","Node.js","REST APIs","MongoDB","Git/GitHub"],
    "Full Stack Developer": ["HTML/CSS","JavaScript","React","Node.js","REST APIs","PostgreSQL","Git/GitHub"],
    "Backend Engineer": ["Python","FastAPI","REST APIs","PostgreSQL","Docker","Git/GitHub","System Design"],
    "Software Engineer": ["DSA","Python","SQL","REST APIs","Git/GitHub","System Design"],
}

PREREQS = {
    "React": ["HTML/CSS","JavaScript"],
    "Node.js": ["JavaScript"],
    "REST APIs": ["Node.js"],
    "MongoDB": ["JavaScript"],
    "PostgreSQL": ["SQL"],
    "Machine Learning": ["Python","Statistics","NumPy/Pandas"],
    "Deep Learning": ["Python","Machine Learning"],
    "NLP": ["Machine Learning"],
    "LLMs": ["Python","NLP"],
    "MLOps": ["Machine Learning","Docker"],
    "Docker": ["Git/GitHub"],
    "System Design": ["REST APIs","SQL"],
}

RESOURCES = {
    "Python": ["Python official tutorial", "Python practice set"],
    "JavaScript": ["MDN JavaScript Guide", "JavaScript mini-project"],
    "React": ["React Learn", "Build a component library"],
    "Node.js": ["Node.js Learn", "Build a REST API"],
    "Machine Learning": ["scikit-learn tutorials", "Build a classification project"],
    "Deep Learning": ["PyTorch tutorials", "Build an image classifier"],
    "LLMs": ["Prompt engineering lab", "Build an RAG prototype"],
    "MLOps": ["ML deployment lab", "Containerize an ML service"],
}
