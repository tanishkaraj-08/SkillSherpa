"""
SkillSherpa Data Generator
Generates all seed datasets required for SkillSherpa:
- roles.json
- resources.json
- opportunities.json
- jargon.json
- cohort.json
- personas.json
"""

import json
import os
import random

os.makedirs("data", exist_ok=True)

# 1. ROLES
roles = {
    "Full Stack Developer": {
        "title": "Full Stack Developer",
        "category": "Software Engineering",
        "description": "Build end-to-end web applications with modern frontend and backend architectures.",
        "skills": {
            "HTML/CSS": {"weight": 1.0, "target_level": 3, "category": "Frontend"},
            "Git & GitHub": {"weight": 1.0, "target_level": 2, "category": "Tooling"},
            "JavaScript": {"weight": 1.5, "target_level": 3, "category": "Frontend"},
            "React": {"weight": 2.0, "target_level": 3, "category": "Frontend"},
            "Node.js": {"weight": 2.0, "target_level": 3, "category": "Backend"},
            "SQL": {"weight": 1.5, "target_level": 3, "category": "Database"}
        },
        "prerequisites": {
            "JavaScript": ["HTML/CSS"],
            "React": ["JavaScript", "Git & GitHub"],
            "Node.js": ["JavaScript"],
            "SQL": []
        }
    },
    "Data Analyst": {
        "title": "Data Analyst",
        "category": "Data & Analytics",
        "description": "Transform messy raw data into business insights, dashboards, and metric forecasts.",
        "skills": {
            "Excel & Spreadsheets": {"weight": 1.0, "target_level": 3, "category": "Foundation"},
            "SQL": {"weight": 2.0, "target_level": 4, "category": "Database"},
            "Python": {"weight": 2.0, "target_level": 3, "category": "Programming"},
            "Pandas": {"weight": 2.0, "target_level": 3, "category": "Data Analysis"},
            "Data Visualization": {"weight": 1.5, "target_level": 3, "category": "Visualization"},
            "Statistics": {"weight": 1.5, "target_level": 3, "category": "Math"}
        },
        "prerequisites": {
            "SQL": ["Excel & Spreadsheets"],
            "Pandas": ["Python"],
            "Data Visualization": ["Pandas"],
            "Statistics": []
        }
    },
    "AI/ML Engineer": {
        "title": "AI/ML Engineer",
        "category": "Artificial Intelligence",
        "description": "Design, train, evaluate and deploy machine learning models to production.",
        "skills": {
            "Python": {"weight": 2.0, "target_level": 4, "category": "Programming"},
            "Linear Algebra & Calculus": {"weight": 1.5, "target_level": 3, "category": "Math"},
            "Machine Learning": {"weight": 2.0, "target_level": 3, "category": "Machine Learning"},
            "Deep Learning": {"weight": 2.0, "target_level": 3, "category": "Deep Learning"},
            "MLOps & API Deployment": {"weight": 1.5, "target_level": 3, "category": "Production"}
        },
        "prerequisites": {
            "Linear Algebra & Calculus": [],
            "Machine Learning": ["Python", "Linear Algebra & Calculus"],
            "Deep Learning": ["Machine Learning"],
            "MLOps & API Deployment": ["Deep Learning"]
        }
    },
    "Bioinformatics Analyst": {
        "title": "Bioinformatics Analyst",
        "category": "Biotech & Healthcare",
        "description": "Analyze genomic, proteomic, and clinical dataset sequences using computational pipelines.",
        "skills": {
            "Biology Domain Knowledge": {"weight": 2.0, "target_level": 4, "category": "Domain"},
            "Python": {"weight": 2.0, "target_level": 3, "category": "Programming"},
            "Biopython & Genomic Data": {"weight": 2.0, "target_level": 3, "category": "Specialized"},
            "SQL": {"weight": 1.5, "target_level": 2, "category": "Database"},
            "Next-Gen Sequencing Basics": {"weight": 1.5, "target_level": 3, "category": "Domain"}
        },
        "prerequisites": {
            "Biopython & Genomic Data": ["Biology Domain Knowledge", "Python"],
            "Next-Gen Sequencing Basics": ["Biopython & Genomic Data"],
            "SQL": []
        }
    },
    "Frontend Developer": {
        "title": "Frontend Developer",
        "category": "Software Engineering",
        "description": "Craft responsive, accessible, interactive web interfaces with modern design systems.",
        "skills": {
            "HTML/CSS": {"weight": 1.5, "target_level": 4, "category": "Frontend"},
            "Git & GitHub": {"weight": 1.0, "target_level": 2, "category": "Tooling"},
            "JavaScript": {"weight": 2.0, "target_level": 4, "category": "Frontend"},
            "Responsive Design & Tailwind": {"weight": 1.5, "target_level": 3, "category": "Styling"},
            "React": {"weight": 2.0, "target_level": 3, "category": "Frontend"},
            "Next.js": {"weight": 1.5, "target_level": 3, "category": "Framework"}
        },
        "prerequisites": {
            "Responsive Design & Tailwind": ["HTML/CSS"],
            "JavaScript": ["HTML/CSS"],
            "React": ["JavaScript", "Git & GitHub"],
            "Next.js": ["React"]
        }
    }
}

with open("data/roles.json", "w") as f:
    json.dump(roles, f, indent=2)

# 2. RESOURCES
resources = {
    "HTML/CSS": {
        "description": "Structure web documents semantically and style with Flexbox and CSS Grid.",
        "weekly_quest": "Build a responsive profile card and host it on GitHub Pages.",
        "mini_project": {
            "title": "Semantic Mountain Rescue Landing Page",
            "prompt": "Create a fully responsive landing page using semantic HTML5 tags (<header>, <main>, <section>, <footer>) and Flexbox/CSS Grid. Include a contact form and mobile navigation.",
            "deliverable": "GitHub repo URL with index.html, styles.css, and live demo link."
        },
        "items": [
            {
                "type": "video",
                "title": "HTML & CSS Full Course - Beginner to Pro",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=G3e-cpL7ofc",
                "hours": 6,
                "difficulty": "Beginner"
            },
            {
                "type": "tutorial",
                "title": "MDN Learn Web Development: Getting Started with the Web",
                "platform": "MDN Web Docs",
                "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development",
                "hours": 4,
                "difficulty": "Beginner"
            },
            {
                "type": "practice",
                "title": "CSS Flexbox Froggy & Grid Garden Interactive Exercises",
                "platform": "Codepip",
                "url": "https://flexboxfroggy.com/",
                "hours": 2,
                "difficulty": "Beginner"
            }
        ]
    },
    "Git & GitHub": {
        "description": "Version control essentials, commit hygiene, branches, pull requests, and collaborative workflows.",
        "weekly_quest": "Fork an open repository, create a branch, submit a mock Pull Request.",
        "mini_project": {
            "title": "Documented Open-Source Starter Kit",
            "prompt": "Create a repository with a clean README.md, LICENSE, .gitignore, and a multi-commit history showcasing feature branches merged via PRs.",
            "deliverable": "GitHub repository URL with clear commit log and Markdown README."
        },
        "items": [
            {
                "type": "video",
                "title": "Git and GitHub for Beginners - Crash Course",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=RGOj5yH7evk",
                "hours": 2,
                "difficulty": "Beginner"
            },
            {
                "type": "tutorial",
                "title": "GitHub Skills: Introduction to GitHub Interactive Lab",
                "platform": "GitHub Skills",
                "url": "https://skills.github.com/",
                "hours": 2,
                "difficulty": "Beginner"
            },
            {
                "type": "practice",
                "title": "Learn Git Branching - Visual Sandbox",
                "platform": "LearnGitBranching",
                "url": "https://learngitbranching.js.org/",
                "hours": 3,
                "difficulty": "Intermediate"
            }
        ]
    },
    "JavaScript": {
        "description": "Modern ES6+ syntax, asynchronous programming (Promises/async-await), closures, DOM manipulation.",
        "weekly_quest": "Write an async API fetcher that handles loading states, timeouts, and network errors.",
        "mini_project": {
            "title": "Interactive Weather & Habit Dashboard",
            "prompt": "Build a client-side JavaScript app that queries a public REST API, renders dynamic DOM elements, filters by keyword, and stores user habits in localStorage.",
            "deliverable": "GitHub repository with app.js demonstrating async/await and array methods (.map, .filter, .reduce)."
        },
        "items": [
            {
                "type": "video",
                "title": "JavaScript Programming - Full Course",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=jS4aFq5-91M",
                "hours": 8,
                "difficulty": "Beginner-Intermediate"
            },
            {
                "type": "tutorial",
                "title": "The Modern JavaScript Tutorial (javascript.info)",
                "platform": "JavaScript.info",
                "url": "https://javascript.info/",
                "hours": 6,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "Exercism JavaScript Track - 5 Core Katas",
                "platform": "Exercism",
                "url": "https://exercism.org/tracks/javascript",
                "hours": 4,
                "difficulty": "Intermediate"
            }
        ]
    },
    "React": {
        "description": "Functional components, custom hooks, useState/useEffect lifecycle, props, state lifting, Context API.",
        "weekly_quest": "Create a reusable searchable list component with debounced search input.",
        "mini_project": {
            "title": "SkillSherpa Expedition Gear Checklist",
            "prompt": "Build a React component hierarchy for managing checklist items with category filters, checked status, local persistence, and summary metrics.",
            "deliverable": "GitHub repo link containing Vite/React code with at least 3 custom components and clean hook state."
        },
        "items": [
            {
                "type": "video",
                "title": "React Course 2024 - Beginner to Advanced",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=bMknfKXIFA8",
                "hours": 10,
                "difficulty": "Intermediate"
            },
            {
                "type": "tutorial",
                "title": "Thinking in React & Quick Start",
                "platform": "React Docs Official",
                "url": "https://react.dev/learn",
                "hours": 5,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "Scrimba - Interactive React Bootcamp Modules",
                "platform": "Scrimba",
                "url": "https://scrimba.com/learn/learnreact",
                "hours": 5,
                "difficulty": "Intermediate"
            }
        ]
    },
    "Node.js": {
        "description": "RESTful API creation with Express, middleware, JSON error handling, environment variables, JWT basics.",
        "weekly_quest": "Build a CRUD REST API with Express and automated request validation.",
        "mini_project": {
            "title": "Mountain Trail Tracker REST API",
            "prompt": "Construct an Express backend providing GET, POST, PUT, DELETE routes for trail checkpoints with validation middleware, status code handling, and mock DB persistence.",
            "deliverable": "GitHub repository with server.js, route tests, and a Postman/curl sample collection in README."
        },
        "items": [
            {
                "type": "video",
                "title": "Node.js and Express.js - Full Course",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=Oe421EPjeBE",
                "hours": 8,
                "difficulty": "Intermediate"
            },
            {
                "type": "tutorial",
                "title": "MDN Express Tutorial: The Local Library website",
                "platform": "MDN Web Docs",
                "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs",
                "hours": 6,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "NodeSchool - Workshopper CLI LearnYouNode",
                "platform": "NodeSchool",
                "url": "https://nodeschool.io/",
                "hours": 3,
                "difficulty": "Intermediate"
            }
        ]
    },
    "SQL": {
        "description": "Relational schema design, normalization, multi-table JOINs, GROUP BY aggregations, window functions.",
        "weekly_quest": "Write a 3-table JOIN query with aggregate grouping and subquery filtering.",
        "mini_project": {
            "title": "University Placement Analytics Schema & Query Suite",
            "prompt": "Design a relational schema (Students, Companies, Interviews, Offers) in SQLite/PostgreSQL with foreign keys, indexes, and write 5 analytical queries reporting conversion rates.",
            "deliverable": "GitHub repository with schema.sql and analytical_queries.sql."
        },
        "items": [
            {
                "type": "video",
                "title": "SQL Tutorial - Full Database Course for Beginners",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
                "hours": 4,
                "difficulty": "Beginner"
            },
            {
                "type": "tutorial",
                "title": "SQLBolt - Interactive Lessons and Queries",
                "platform": "SQLBolt",
                "url": "https://sqlbolt.com/",
                "hours": 3,
                "difficulty": "Beginner"
            },
            {
                "type": "practice",
                "title": "Kaggle Learn: Intro to SQL & Advanced SQL",
                "platform": "Kaggle Learn",
                "url": "https://www.kaggle.com/learn/intro-to-sql",
                "hours": 4,
                "difficulty": "Intermediate"
            }
        ]
    },
    "Python": {
        "description": "Core syntax, data structures (lists, dicts, sets, tuples), OOP, list comprehensions, file I/O, error handling.",
        "weekly_quest": "Build a CSV log parser that computes frequency distributions and writes JSON summaries.",
        "mini_project": {
            "title": "Expedition Log Telemetry Analyzer",
            "prompt": "Create an object-oriented Python command-line tool that parses flight/sensor telemetry logs, handles corrupt rows gracefully, and prints summary stats.",
            "deliverable": "GitHub repository with clean modular Python code, unit tests with unittest/pytest."
        },
        "items": [
            {
                "type": "video",
                "title": "CS50's Introduction to Programming with Python",
                "platform": "Harvard CS50 / YouTube",
                "url": "https://cs50.harvard.edu/python/",
                "hours": 12,
                "difficulty": "Beginner"
            },
            {
                "type": "tutorial",
                "title": "The Official Python Tutorial (docs.python.org)",
                "platform": "Python Software Foundation",
                "url": "https://docs.python.org/3/tutorial/",
                "hours": 6,
                "difficulty": "Beginner-Intermediate"
            },
            {
                "type": "practice",
                "title": "Exercism Python Track & Kaggle Python Course",
                "platform": "Kaggle / Exercism",
                "url": "https://www.kaggle.com/learn/python",
                "hours": 4,
                "difficulty": "Beginner"
            }
        ]
    },
    "Pandas": {
        "description": "DataFrames, Series, missing data imputation, groupby, merge/join, pivot tables, time series manipulation.",
        "weekly_quest": "Clean a messy real-world CSV dataset with missing timestamps and categorical typos.",
        "mini_project": {
            "title": "Public Health Cohort Data Wrangling Pipeline",
            "prompt": "Clean, merge, and transform two tabular datasets. Handle NaN values, parse ISO dates, and export an aggregated pivot table with markdown summary notes.",
            "deliverable": "GitHub Jupyter notebook or clean Python script using vectorized Pandas methods."
        },
        "items": [
            {
                "type": "video",
                "title": "Pandas Full Tutorial for Beginners",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=vmEHCJofslg",
                "hours": 5,
                "difficulty": "Intermediate"
            },
            {
                "type": "tutorial",
                "title": "Kaggle Learn: Pandas 4-Hour Micro-course",
                "platform": "Kaggle Learn",
                "url": "https://www.kaggle.com/learn/pandas",
                "hours": 4,
                "difficulty": "Beginner-Intermediate"
            },
            {
                "type": "practice",
                "title": "100 Pandas Puzzles (Open-Source GitHub Practice)",
                "platform": "GitHub Community",
                "url": "https://github.com/ajcr/100-pandas-puzzles",
                "hours": 3,
                "difficulty": "Intermediate"
            }
        ]
    },
    "Excel & Spreadsheets": {
        "description": "Formulas (VLOOKUP, XLOOKUP, INDEX-MATCH), pivot tables, data hygiene, conditional formatting.",
        "weekly_quest": "Create an automated budget model with dynamic drop-downs and conditional color bands.",
        "mini_project": {
            "title": "Camp Supply Operations Financial Model",
            "prompt": "Build an Excel/Google Sheets model using XLOOKUP, dynamic SUMIFS, and a multi-scenario pivot dashboard.",
            "deliverable": "Shared link or exported .xlsx with clean formula audit trail."
        },
        "items": [
            {
                "type": "video",
                "title": "Excel for Beginners to Advanced Course",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=Vl0H-qTclOg",
                "hours": 4,
                "difficulty": "Beginner"
            },
            {
                "type": "tutorial",
                "title": "Microsoft 365 Excel Training Center",
                "platform": "Microsoft Support",
                "url": "https://support.microsoft.com/en-us/excel",
                "hours": 3,
                "difficulty": "Beginner"
            },
            {
                "type": "practice",
                "title": "Excel Practice Online Exercises",
                "platform": "Excel-Practice-Online",
                "url": "https://www.excel-practice-online.com/",
                "hours": 2,
                "difficulty": "Beginner"
            }
        ]
    },
    "Data Visualization": {
        "description": "Chart selection taxonomy, Matplotlib, Seaborn, Plotly, color theory, storytelling with dashboards.",
        "weekly_quest": "Build an interactive multi-faceted scatter plot with Plotly showing correlation insights.",
        "mini_project": {
            "title": "Global Climate Anomalies Visual Storyboard",
            "prompt": "Create 3 publication-ready charts (distribution, correlation, time series trend) using Seaborn/Plotly with proper annotations and accessible color palettes.",
            "deliverable": "Jupyter notebook on GitHub with annotated figures and executive takeaways."
        },
        "items": [
            {
                "type": "video",
                "title": "Data Visualization with Python - Full Course",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=a9UrKTVEeZA",
                "hours": 4,
                "difficulty": "Intermediate"
            },
            {
                "type": "tutorial",
                "title": "Kaggle Learn: Data Visualization Course",
                "platform": "Kaggle Learn",
                "url": "https://www.kaggle.com/learn/data-visualization",
                "hours": 4,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "From Data to Viz - Interactive Chart Chooser Guide",
                "platform": "Data to Viz",
                "url": "https://www.data-to-viz.com/",
                "hours": 2,
                "difficulty": "Beginner"
            }
        ]
    },
    "Statistics": {
        "description": "Descriptive statistics, hypothesis testing (t-test, chi-square), p-values, distributions, Bayes theorem.",
        "weekly_quest": "Perform an A/B test analysis on mock conversion rates with confidence interval reporting.",
        "mini_project": {
            "title": "A/B Testing Experiment Rigor Report",
            "prompt": "Analyze a two-variant conversion experiment dataset. Calculate p-value, effect size, statistical power, and draft an executive recommendation.",
            "deliverable": "GitHub repository with analytical notebook and clear business summary."
        },
        "items": [
            {
                "type": "video",
                "title": "Statistics for Data Science - Full Course",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=xxpc-HPKN28",
                "hours": 6,
                "difficulty": "Intermediate"
            },
            {
                "type": "tutorial",
                "title": "Khan Academy: High School & College Statistics",
                "platform": "Khan Academy",
                "url": "https://www.khanacademy.org/math/statistics-probability",
                "hours": 6,
                "difficulty": "Beginner-Intermediate"
            },
            {
                "type": "practice",
                "title": "Seeing Theory: A Visual Introduction to Probability & Stats",
                "platform": "Brown University",
                "url": "https://seeing-theory.brown.edu/",
                "hours": 3,
                "difficulty": "Beginner"
            }
        ]
    },
    "Machine Learning": {
        "description": "Supervised & unsupervised learning, Scikit-Learn, cross-validation, regularization, evaluation metrics (ROC-AUC, F1).",
        "weekly_quest": "Train and compare a Random Forest vs Logistic Regression model with 5-fold cross validation.",
        "mini_project": {
            "title": "Credit Risk Default Predictor with Scikit-Learn",
            "prompt": "Build an end-to-end ML pipeline with numerical scaling, one-hot encoding, model training, hyperparameter tuning via GridSearchCV, and metric evaluation.",
            "deliverable": "GitHub repository with pipeline.py and saved model artifact."
        },
        "items": [
            {
                "type": "video",
                "title": "Machine Learning for Everybody - Full Course",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=i_LwzRVP7bg",
                "hours": 4,
                "difficulty": "Intermediate"
            },
            {
                "type": "tutorial",
                "title": "Kaggle Learn: Intro to Machine Learning",
                "platform": "Kaggle Learn",
                "url": "https://www.kaggle.com/learn/intro-to-machine-learning",
                "hours": 4,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "Scikit-Learn Official Tutorials and Examples",
                "platform": "scikit-learn.org",
                "url": "https://scikit-learn.org/stable/tutorial/index.html",
                "hours": 5,
                "difficulty": "Intermediate"
            }
        ]
    },
    "Deep Learning": {
        "description": "Neural network architectures, PyTorch tensors, backprop, loss functions, CNNs, transformers basics.",
        "weekly_quest": "Train a simple CNN classifier on Fashion-MNIST with PyTorch and plot train/val loss curves.",
        "mini_project": {
            "title": "PyTorch Vision Classifier for Medical Image Triage",
            "prompt": "Construct a convolutional neural network or fine-tune a lightweight MobileNet on image data. Implement early stopping, validation checkpointing, and confusion matrix.",
            "deliverable": "GitHub repo with PyTorch training script, requirements, and test accuracy metrics."
        },
        "items": [
            {
                "type": "video",
                "title": "PyTorch for Deep Learning Bootcamp",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=V_xro1rmAuQ",
                "hours": 12,
                "difficulty": "Advanced"
            },
            {
                "type": "tutorial",
                "title": "Fast.ai Practical Deep Learning for Coders",
                "platform": "Fast.ai",
                "url": "https://course.fast.ai/",
                "hours": 10,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "PyTorch Official 60-Minute Blitz",
                "platform": "pytorch.org",
                "url": "https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html",
                "hours": 4,
                "difficulty": "Intermediate"
            }
        ]
    },
    "Linear Algebra & Calculus": {
        "description": "Vectors, matrices, dot products, eigenvalues, partial derivatives, gradient descent math.",
        "weekly_quest": "Implement gradient descent from scratch in pure NumPy without ML frameworks.",
        "mini_project": {
            "title": "Pure NumPy Neural Network Math Engine",
            "prompt": "Write a 2-layer forward and backward propagation pass using only NumPy matrix multiplications and analytical gradients.",
            "deliverable": "GitHub Jupyter notebook detailing the mathematical derivations and code."
        },
        "items": [
            {
                "type": "video",
                "title": "Essence of Linear Algebra by 3Blue1Brown",
                "platform": "3Blue1Brown YouTube",
                "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab",
                "hours": 5,
                "difficulty": "Beginner-Intermediate"
            },
            {
                "type": "tutorial",
                "title": "Khan Academy: Linear Algebra & Multivariable Calculus",
                "platform": "Khan Academy",
                "url": "https://www.khanacademy.org/math/linear-algebra",
                "hours": 8,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "Immersive Math: Interactive Linear Algebra with 3D Graphics",
                "platform": "Immersive Math",
                "url": "http://immersivemath.com/ila/index.html",
                "hours": 3,
                "difficulty": "Intermediate"
            }
        ]
    },
    "MLOps & API Deployment": {
        "description": "FastAPI model serving, Docker containerization, model monitoring, batch vs real-time inference.",
        "weekly_quest": "Wrap a Scikit-Learn model in a FastAPI endpoint and test with Swagger UI.",
        "mini_project": {
            "title": "Containerized ML Inference Microservice",
            "prompt": "Build a FastAPI REST service exposing a /predict endpoint with Pydantic schema validation and a Dockerfile for reproducible deployment.",
            "deliverable": "GitHub repo with main.py, Dockerfile, test_api.py, and sample curl commands."
        },
        "items": [
            {
                "type": "video",
                "title": "FastAPI Full Course - Python API Development",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=0sOvCWFmrtA",
                "hours": 6,
                "difficulty": "Intermediate"
            },
            {
                "type": "tutorial",
                "title": "Full Stack MLOps Course",
                "platform": "Made With ML",
                "url": "https://madewithml.com/",
                "hours": 8,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "FastAPI Official Interactive Documentation & Tutorial",
                "platform": "FastAPI",
                "url": "https://fastapi.tiangolo.com/tutorial/",
                "hours": 3,
                "difficulty": "Intermediate"
            }
        ]
    },
    "Biology Domain Knowledge": {
        "description": "Central dogma of molecular biology, DNA/RNA sequences, amino acid structures, gene expression.",
        "weekly_quest": "Draft a pathway diagram connecting transcription, translation, and mutated protein folding.",
        "mini_project": {
            "title": "Genetic Mutation Impact Analysis Dossier",
            "prompt": "Document a case study of a single nucleotide polymorphism (SNP), explaining its effect on codon translation and phenotypic expression.",
            "deliverable": "Markdown report with citations and amino acid substitution analysis."
        },
        "items": [
            {
                "type": "video",
                "title": "DNA, RNA, and Protein Synthesis",
                "platform": "Khan Academy / YouTube",
                "url": "https://www.khanacademy.org/science/biology/gene-expression-central-dogma",
                "hours": 4,
                "difficulty": "Beginner"
            },
            {
                "type": "tutorial",
                "title": "Nature Education Scitable: Essentials of Genetics",
                "platform": "Nature Scitable",
                "url": "https://www.nature.com/scitable/topic/genetics-5/",
                "hours": 5,
                "difficulty": "Beginner"
            },
            {
                "type": "practice",
                "title": "Learn.Genetics Interactive Tour of the Basics",
                "platform": "University of Utah",
                "url": "https://learn.genetics.utah.edu/",
                "hours": 2,
                "difficulty": "Beginner"
            }
        ]
    },
    "Biopython & Genomic Data": {
        "description": "FASTA/FASTQ parsing, NCBI Entrez queries, pairwise sequence alignment with Bio.Seq, motif finding.",
        "weekly_quest": "Write a Biopython script to calculate GC content and locate open reading frames (ORFs).",
        "mini_project": {
            "title": "Automated Viral Genome Variant Scanner",
            "prompt": "Write a Python script using Biopython to download a target viral FASTA file from NCBI, identify mutation loci against a reference genome, and output a CSV report.",
            "deliverable": "GitHub repository with variant_scanner.py and sample output."
        },
        "items": [
            {
                "type": "video",
                "title": "Bioinformatics with Python Tutorial Series",
                "platform": "Data Professor / YouTube",
                "url": "https://www.youtube.com/watch?v=uNm71wZ_w78",
                "hours": 4,
                "difficulty": "Intermediate"
            },
            {
                "type": "tutorial",
                "title": "Biopython Tutorial and Cookbook",
                "platform": "Biopython.org",
                "url": "https://biopython.org/DIST/docs/tutorial/Tutorial.html",
                "hours": 6,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "Rosalind: Platform for Learning Bioinformatics through Problem Solving",
                "platform": "Rosalind.info",
                "url": "https://rosalind.info/problems/locations/",
                "hours": 5,
                "difficulty": "Intermediate"
            }
        ]
    },
    "Next-Gen Sequencing Basics": {
        "description": "Illumina sequencing workflow, read quality control (FastQC), SAM/BAM alignments, variant calling pipelines.",
        "weekly_quest": "Run a simulated FastQC quality report and interpret Phred score drops.",
        "mini_project": {
            "title": "Mini NGS Read Quality Control Pipeline",
            "prompt": "Construct a bash/python workflow that filters low-quality reads (Phred < 20) from synthetic FASTQ data and generates summary quality plots.",
            "deliverable": "GitHub repository with qc_pipeline.sh/py and generated quality charts."
        },
        "items": [
            {
                "type": "video",
                "title": "Next Generation Sequencing (NGS) - An Introduction",
                "platform": "EMBL-EBI / YouTube",
                "url": "https://www.ebi.ac.uk/training/online/courses/human-genetic-variation-introduction/next-generation-sequencing-ngs/",
                "hours": 3,
                "difficulty": "Intermediate"
            },
            {
                "type": "tutorial",
                "title": "Galaxy Project: NGS Quality Control & Mapping Tutorial",
                "platform": "Galaxy Training Network",
                "url": "https://training.galaxyproject.org/",
                "hours": 4,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "Babraham Bioinformatics FastQC Practice Datasets",
                "platform": "Babraham Institute",
                "url": "https://www.bioinformatics.babraham.ac.uk/projects/fastqc/",
                "hours": 2,
                "difficulty": "Intermediate"
            }
        ]
    },
    "Responsive Design & Tailwind": {
        "description": "Utility-first CSS, mobile-first breakpoints, flex/grid layouts, component styling with Tailwind CSS.",
        "weekly_quest": "Recreate a desktop SaaS dashboard view as an adaptive mobile-first layout.",
        "mini_project": {
            "title": "High-Converting SaaS Pricing Component",
            "prompt": "Build a responsive tiered pricing component with monthly/annual billing toggles and feature comparisons using Tailwind CSS classes.",
            "deliverable": "GitHub repo with HTML/Tailwind demo page hosted on GitHub Pages or Vercel."
        },
        "items": [
            {
                "type": "video",
                "title": "Tailwind CSS Full Course for Beginners",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=ft30zcMlFao",
                "hours": 4,
                "difficulty": "Beginner"
            },
            {
                "type": "tutorial",
                "title": "Tailwind CSS Official Documentation & Core Concepts",
                "platform": "Tailwind Labs",
                "url": "https://tailwindcss.com/docs/utility-first",
                "hours": 3,
                "difficulty": "Beginner"
            },
            {
                "type": "practice",
                "title": "Tailwind Play - Interactive Browser Playground",
                "platform": "Tailwind Labs",
                "url": "https://play.tailwindcss.com/",
                "hours": 2,
                "difficulty": "Beginner"
            }
        ]
    },
    "Next.js": {
        "description": "App Router, Server Components vs Client Components, dynamic routing, API route handlers, SEO.",
        "weekly_quest": "Build a dynamic blog route fetching markdown content via Server Components.",
        "mini_project": {
            "title": "Fast SEO-Optimized Product Catalog in Next.js",
            "prompt": "Create a Next.js 14 App Router application with static generation for product pages, client-side category filtering, and metadata optimization.",
            "deliverable": "GitHub repo with app router structure and deployment on Vercel."
        },
        "items": [
            {
                "type": "video",
                "title": "Next.js 14 Full Course - App Router",
                "platform": "freeCodeCamp",
                "url": "https://www.youtube.com/watch?v=wm5gMKuwSYk",
                "hours": 6,
                "difficulty": "Intermediate"
            },
            {
                "type": "tutorial",
                "title": "Learn Next.js - Official Interactive Course",
                "platform": "Next.js / Vercel",
                "url": "https://nextjs.org/learn",
                "hours": 5,
                "difficulty": "Intermediate"
            },
            {
                "type": "practice",
                "title": "Vercel Next.js Templates & Starter Walkthroughs",
                "platform": "Vercel",
                "url": "https://vercel.com/templates/next.js",
                "hours": 3,
                "difficulty": "Intermediate"
            }
        ]
    }
}

with open("data/resources.json", "w") as f:
    json.dump(resources, f, indent=2)

# 3. OPPORTUNITIES (25 mock entries across internships, jobs, hackathons, open-source, scholarships, free certifications)
opportunities = [
    {
        "id": "opp-01",
        "title": "First Contribution to Docs & Starter Templates",
        "organization": "Mozilla Open Source Community",
        "type": "Open Source",
        "stipend_or_perk": "Community Badge & Review",
        "location": "Remote",
        "required_skills": {"Git & GitHub": 1, "HTML/CSS": 1},
        "beginner_friendly": True,
        "description": "Beginner-friendly 'good-first-issue' fixing broken links, typos, and formatting in developer guides.",
        "apply_url": "https://github.com/mdn/content/issues",
        "why_this": "Matches entry-level Git skills; builds early GitHub contribution history."
    },
    {
        "id": "opp-02",
        "title": "Tamil Nadu State Student Innovation Hackathon 2025",
        "organization": "Anna University & IIT Madras Incubator",
        "type": "Hackathon",
        "stipend_or_perk": "₹1,50,000 Prize Pool + Mentorship",
        "location": "Chennai / Hybrid",
        "required_skills": {"HTML/CSS": 2, "Git & GitHub": 2},
        "beginner_friendly": True,
        "description": "36-hour hackathon designed specifically for first-time hackers from Tier-2/3 institutions and regional boards.",
        "apply_url": "https://tnhackathon.example.org",
        "why_this": "Dedicated beginner track with peer mentors and zero prerequisite experience required."
    },
    {
        "id": "opp-03",
        "title": "FreeCodeCamp Responsive Web Design Certification",
        "organization": "freeCodeCamp.org",
        "type": "Free Certification",
        "stipend_or_perk": "Verified Digital Credential",
        "location": "Online / Self-paced",
        "required_skills": {"HTML/CSS": 2},
        "beginner_friendly": True,
        "description": "Complete 5 interactive projects to earn an industry-recognized open-source web design certificate.",
        "apply_url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/",
        "why_this": "Pure project-based certification that complements your verified HTML/CSS foundation."
    },
    {
        "id": "opp-04",
        "title": "Junior Frontend Web Dev Intern",
        "organization": "FinNest Fintech Labs",
        "type": "Internship",
        "stipend_or_perk": "₹18,000 / month",
        "location": "Bengaluru / Hybrid",
        "required_skills": {"HTML/CSS": 2, "JavaScript": 2, "Git & GitHub": 2},
        "beginner_friendly": False,
        "description": "Build responsive banking dashboards and interactive calculation tools alongside senior frontend mentors.",
        "apply_url": "https://finnest.careers/internships",
        "why_this": "Direct bridge into modern frontend teams once core JavaScript is verified."
    },
    {
        "id": "opp-05",
        "title": "Kaggle Micro-Course Contributor: Good First Issue",
        "organization": "Kaggle Open Community",
        "type": "Open Source",
        "stipend_or_perk": "Kaggle Swag + Contributor Tier",
        "location": "Remote",
        "required_skills": {"Python": 2},
        "beginner_friendly": True,
        "description": "Contribute code snippets and dataset docstrings to community notebooks and open Kaggle micro-courses.",
        "apply_url": "https://www.kaggle.com/community",
        "why_this": "Ideal first public contribution for learners with verified Python skills."
    },
    {
        "id": "opp-06",
        "title": "Full Stack React & Node Developer Intern",
        "organization": "HyperCart E-Commerce",
        "type": "Internship",
        "stipend_or_perk": "₹25,000 / month",
        "location": "Remote",
        "required_skills": {"React": 3, "Node.js": 3, "JavaScript": 3},
        "beginner_friendly": False,
        "description": "Work on customer checkout flows, merchant inventory APIs, and Redis-cached catalog routes.",
        "apply_url": "https://hypercart.io/jobs",
        "why_this": "Requires full-stack verification in React and Node.js for production code authoring."
    },
    {
        "id": "opp-07",
        "title": "Google Summer of Code: Python Scientific Track",
        "organization": "Python Software Foundation (PSF)",
        "type": "Scholarship",
        "stipend_or_perk": "$1,500 - $3,000 Stipend",
        "location": "Remote",
        "required_skills": {"Python": 3, "Git & GitHub": 2},
        "beginner_friendly": False,
        "description": "Spend 12 weeks contributing full-time to core open-source Python packages with 1:1 senior maintainers.",
        "apply_url": "https://summerofcode.withgoogle.com/",
        "why_this": "Prestigious international fellowship proving open-source engineering caliber."
    },
    {
        "id": "opp-08",
        "title": "Data Analyst Trainee - Healthcare Intelligence",
        "organization": "Apollo Health Tech",
        "type": "Job",
        "stipend_or_perk": "₹4.5 - 6.0 LPA",
        "location": "Chennai / Hyderabad",
        "required_skills": {"SQL": 3, "Excel & Spreadsheets": 3, "Python": 2},
        "beginner_friendly": False,
        "description": "Extract hospital patient flow telemetry, build weekly KPI dashboards, and audit diagnostic test turnaround.",
        "apply_url": "https://apollohealthtech.in/careers",
        "why_this": "High demand role matching verified SQL and spreadsheet modeling capabilities."
    },
    {
        "id": "opp-09",
        "title": "Smart India Hackathon (SIH) Internal Campus Qualifier",
        "organization": "Ministry of Education / AICTE",
        "type": "Hackathon",
        "stipend_or_perk": "National Finalist Qualification",
        "location": "On-Campus / Nationwide",
        "required_skills": {"Python": 1, "Git & GitHub": 1},
        "beginner_friendly": True,
        "description": "Solve problem statements proposed by government ministries. Perfect entry platform for college teams.",
        "apply_url": "https://sih.gov.in/",
        "why_this": "Open to any engineering or science student regardless of prior hackathon experience."
    },
    {
        "id": "opp-10",
        "title": "Bioinformatics Research Fellow (Genomics Pipeline)",
        "organization": "Institute of Genomics & Integrative Biology (CSIR-IGIB)",
        "type": "Internship",
        "stipend_or_perk": "₹20,000 / month + Lab Access",
        "location": "New Delhi / Remote",
        "required_skills": {"Biology Domain Knowledge": 3, "Python": 3, "Biopython & Genomic Data": 3},
        "beginner_friendly": False,
        "description": "Execute comparative genomics alignment on SARS-CoV-2 / TB clinical isolate sequences.",
        "apply_url": "https://www.igib.res.in/",
        "why_this": "Combines life sciences knowledge with computational Biopython proficiency."
    },
    {
        "id": "opp-11",
        "title": "Beginner First Issue: UI Accessibility Bug Fixes",
        "organization": "Chakra UI / Free Open Source",
        "type": "Open Source",
        "stipend_or_perk": "Maintainer Shoutout & Discord Role",
        "location": "Remote",
        "required_skills": {"HTML/CSS": 2, "Git & GitHub": 1},
        "beginner_friendly": True,
        "description": "Fix ARIA attributes and contrast color contrast ratios on button and modal components.",
        "apply_url": "https://github.com/chakra-ui/chakra-ui/issues",
        "why_this": "Great starting issue that reinforces accessibility and clean HTML semantics."
    },
    {
        "id": "opp-12",
        "title": "Junior Backend API Developer",
        "organization": "Zoho Partner Ecosystem",
        "type": "Job",
        "stipend_or_perk": "₹5.0 - 7.5 LPA",
        "location": "Chennai / Tenkasi",
        "required_skills": {"Node.js": 3, "SQL": 3, "JavaScript": 3},
        "beginner_friendly": False,
        "description": "Design modular microservices and webhooks for enterprise SaaS CRM integrations.",
        "apply_url": "https://zoho.com/careers",
        "why_this": "Strong match for candidates with verified server-side JS and relational database modeling."
    },
    {
        "id": "opp-13",
        "title": "Kaggle Community Dataset Analysis Sprint",
        "organization": "Kaggle",
        "type": "Hackathon",
        "stipend_or_perk": "$5,000 Community Pool",
        "location": "Online",
        "required_skills": {"Pandas": 2, "Data Visualization": 2},
        "beginner_friendly": True,
        "description": "Publish a high-clarity exploratory data analysis (EDA) notebook on any public dataset.",
        "apply_url": "https://www.kaggle.com/competitions",
        "why_this": "Fast way to earn public notebook upvotes and demonstrate data storytelling."
    },
    {
        "id": "opp-14",
        "title": "Associate AI Engineer (Computer Vision & Tabular)",
        "organization": "NeuralSense Analytics",
        "type": "Job",
        "stipend_or_perk": "₹6.5 - 9.0 LPA",
        "location": "Bengaluru / Hybrid",
        "required_skills": {"Python": 3, "Machine Learning": 3, "Deep Learning": 3},
        "beginner_friendly": False,
        "description": "Deploy deep learning vision models for automated quality defect inspection in manufacturing plants.",
        "apply_url": "https://neuralsense.ai/careers",
        "why_this": "High-impact AI position requiring verified PyTorch and classical ML capabilities."
    },
    {
        "id": "opp-15",
        "title": "Meta Front-End Developer Professional Certificate Grant",
        "organization": "Coursera & Meta Social Impact",
        "type": "Scholarship",
        "stipend_or_perk": "100% Tuition Waiver ($399 Value)",
        "location": "Online",
        "required_skills": {"HTML/CSS": 2, "JavaScript": 2},
        "beginner_friendly": True,
        "description": "Need-based full scholarship for underrepresented students completing frontend learning paths.",
        "apply_url": "https://coursera.org/financial-aid",
        "why_this": "Validates your verified web foundations with a Meta-sponsored credential."
    },
    {
        "id": "opp-16",
        "title": "Biotech Data Science Student Fellowship",
        "organization": "Biocon Academy & DBT India",
        "type": "Scholarship",
        "stipend_or_perk": "₹50,000 Research Grant",
        "location": "Bengaluru / Hybrid",
        "required_skills": {"Biology Domain Knowledge": 3, "Python": 2},
        "beginner_friendly": True,
        "description": "Supports undergraduate life science students transitioning into computational genomics and clinical analytics.",
        "apply_url": "https://bioconacademy.com/fellowships",
        "why_this": "Explicitly values non-CS life science background as an asset for computational biology."
    },
    {
        "id": "opp-17",
        "title": "Frontend Engineer - Design Systems",
        "organization": "Freshworks Ecosystem",
        "type": "Job",
        "stipend_or_perk": "₹7.0 - 10.0 LPA",
        "location": "Chennai / Bengaluru",
        "required_skills": {"React": 3, "Responsive Design & Tailwind": 3, "JavaScript": 3},
        "beginner_friendly": False,
        "description": "Build accessible UI components, theme tokens, and developer documentation for enterprise customer portals.",
        "apply_url": "https://freshworks.com/careers",
        "why_this": "Targets engineers with proven mastery in responsive layout components and modern React."
    },
    {
        "id": "opp-18",
        "title": "Machine Learning Intern (Predictive Modeling)",
        "organization": "Mu Sigma Analytics",
        "type": "Internship",
        "stipend_or_perk": "₹22,000 / month",
        "location": "Bengaluru",
        "required_skills": {"Python": 3, "Machine Learning": 2, "Statistics": 2},
        "beginner_friendly": False,
        "description": "Assist senior decision scientists in building customer churn and demand forecasting pipelines.",
        "apply_url": "https://mu-sigma.com/careers",
        "why_this": "Requires foundational statistics alongside Scikit-Learn modeling skills."
    },
    {
        "id": "opp-19",
        "title": "CS50x Free Harvard Verified Certificate Track",
        "organization": "Harvard University / edX",
        "type": "Free Certification",
        "stipend_or_perk": "Official CS50 Certificate of Completion",
        "location": "Online / Self-paced",
        "required_skills": {"Python": 2, "SQL": 1},
        "beginner_friendly": True,
        "description": "Legendary introductory computer science course completely free of charge, with 9 graded problem sets.",
        "apply_url": "https://cs50.harvard.edu/x",
        "why_this": "World-class foundational credential that tests problem-solving rigor."
    },
    {
        "id": "opp-20",
        "title": "React Native Mobile App Junior Developer",
        "organization": "HealthTap Digital Care",
        "type": "Job",
        "stipend_or_perk": "₹5.5 - 8.0 LPA",
        "location": "Remote (India)",
        "required_skills": {"React": 3, "JavaScript": 3, "Git & GitHub": 2},
        "beginner_friendly": False,
        "description": "Collaborate on patient telehealth booking and doctor appointment reminders for iOS and Android.",
        "apply_url": "https://healthtap.example/careers",
        "why_this": "Natural progression for React web developers looking to build cross-platform apps."
    },
    {
        "id": "opp-21",
        "title": "First Hackathon: SheHacks / Diversity Buildathon",
        "organization": "Women Techmakers & AnitaB.org",
        "type": "Hackathon",
        "stipend_or_perk": "₹75,000 Cash + Cloud Credits",
        "location": "Virtual / Pan-India",
        "required_skills": {"HTML/CSS": 1},
        "beginner_friendly": True,
        "description": "Encouraging weekend hackathon featuring warm mentors, beginner workshops, and zero judgment.",
        "apply_url": "https://shehacks.example.org",
        "why_this": "Super supportive space designed to demystify hackathons for first-time builders."
    },
    {
        "id": "opp-22",
        "title": "Junior MLOps & Fast-API Service Intern",
        "organization": "DataPipe Cloud Systems",
        "type": "Internship",
        "stipend_or_perk": "₹28,000 / month",
        "location": "Remote",
        "required_skills": {"Python": 3, "MLOps & API Deployment": 2},
        "beginner_friendly": False,
        "description": "Package PyTorch and ONNX models into high-throughput containerized microservices.",
        "apply_url": "https://datapipe.cloud/jobs",
        "why_this": "Focuses on deployment engineering rather than theoretical algorithm tuning."
    },
    {
        "id": "opp-23",
        "title": "Bioinformatics Pipeline Contributor: Nextflow Core",
        "organization": "nf-core Genomics Collective",
        "type": "Open Source",
        "stipend_or_perk": "Community Co-authorship in Research Paper",
        "location": "Remote",
        "required_skills": {"Next-Gen Sequencing Basics": 2, "Git & GitHub": 2},
        "beginner_friendly": False,
        "description": "Help validate reproducible NGS workflow modules for RNA-seq and microbial metagenomics.",
        "apply_url": "https://nf-co.re/",
        "why_this": "Direct pathway into international scientific software authoring."
    },
    {
        "id": "opp-24",
        "title": "Junior Next.js / Web Application Developer",
        "organization": "Unicorn Labs Studio",
        "type": "Job",
        "stipend_or_perk": "₹6.0 - 8.5 LPA",
        "location": "Bengaluru / Pune",
        "required_skills": {"React": 3, "Next.js": 2, "JavaScript": 3},
        "beginner_friendly": False,
        "description": "Build modern server-side rendered client portals with Tailwind, Prisma, and Next.js App Router.",
        "apply_url": "https://unicornlabs.io/join",
        "why_this": "Requires verified hands-on Next.js project proof before interview shortlisting."
    },
    {
        "id": "opp-25",
        "title": "Deep Learning Specialization Fellowship Grant",
        "organization": "DeepLearning.AI Equity Initiative",
        "type": "Scholarship",
        "stipend_or_perk": "100% Free Access to Andrew Ng Series",
        "location": "Online",
        "required_skills": {"Python": 3, "Linear Algebra & Calculus": 2},
        "beginner_friendly": True,
        "description": "Full financial scholarship covering the 5-course Deep Learning Specialization on Coursera.",
        "apply_url": "https://deeplearning.ai/scholarships",
        "why_this": "Comprehensive math & neural network curriculum from the pioneer of online AI education."
    }
]

with open("data/opportunities.json", "w") as f:
    json.dump(opportunities, f, indent=2)

# 4. JARGON (Tanglish + English explanations)
jargon = {
    "hackathon": {
        "term": "Hackathon",
        "category": "Events",
        "english": "A 24 to 48-hour team marathon where students build a working prototype software or app from scratch and present it to judges.",
        "tanglish": "Hackathon-na bayapadatheenga! Adhu oru coding festival maadhiri. Oru 24-48 hours-la chinna team-ah serndhu oru useful prototype app pannanum. First-time participate pandradhe periya learning experience!",
        "tip": "You don't need to be an expert to enter. In fact, most hackathons have special beginner categories and provide free mentors!"
    },
    "github": {
        "term": "GitHub",
        "category": "Tools",
        "english": "A cloud platform where programmers store, share, and collaborate on code files using the Git version tracking system.",
        "tanglish": "Namma Google Drive maadhiri, aana programmers code save panna use panra cloud locker. Yaar eppo enna change pannanga-nu line-by-line track pannum. Recruiter unga profile-ah paarthu nambuvaanga.",
        "tip": "Having even 2 simple repositories with clean README files beats 10 certificates on your resume."
    },
    "open source": {
        "term": "Open Source",
        "category": "Culture",
        "english": "Software whose original source code is made freely available to the public and may be redistributed and modified by anyone.",
        "tanglish": "Yaru venaalum code-ah eduthu paarkalaam, use pannalaam, improve pannalaam. World-la irukra big tech companies (Google, Meta) kooda open-source projects-ah rely panranga. Neenga chinna typo fix panna kooda contribute pannalaam!",
        "tip": "Start with 'good first issue' labels to fix documentation or small bugs."
    },
    "api": {
        "term": "API (Application Programming Interface)",
        "category": "Concepts",
        "english": "A messenger mechanism that allows two different computer software systems to communicate and exchange data securely.",
        "tanglish": "Restaurant-la Waiter maadhiri! Neenga (App) menu paathu food order panna, waiter (API) kitchen-ku (Server/Database) poi food eduthu varuvaaru. Two apps pesikka use aagum.",
        "tip": "When you check live cricket scores or weather on your phone, an API brings that data."
    },
    "repository": {
        "term": "Repository (Repo)",
        "category": "Tools",
        "english": "A dedicated digital folder or storage space on Git/GitHub that holds all project files, history, and documentation.",
        "tanglish": "Oru project-oda official file folder. Idhula unga code, images, explanation documents (README) ellam irukkum.",
        "tip": "Always include a README.md file in every repository explaining what the project does."
    },
    "internship": {
        "term": "Internship",
        "category": "Career",
        "english": "A temporary professional work experience (usually 2 to 6 months) offered by companies to students to gain real-world practical skills.",
        "tanglish": "College padikkum pothe oru company-la trainee-ah vela paathu real-world project epdi run aagudhu-nu kathukra chance. Neraya internships stipend (salary) tharuvanga.",
        "tip": "Prioritize internships where you get code reviews over those where you only watch slides."
    },
    "ats": {
        "term": "ATS (Applicant Tracking System)",
        "category": "Recruitment",
        "english": "Automated software used by recruiters to scan, filter, and score resumes against job description keywords before a human reads them.",
        "tanglish": "Companies unga resume-ah aal vechu padikrathukku munnadi, oru computer software scan pannum. Keyword match irundha dhaan interview call varum. Cluttered graphic templates avoid pannanum.",
        "tip": "Use clean single-column plain text and list specific verified technologies (React, SQL, Python)."
    },
    "portfolio": {
        "term": "Portfolio",
        "category": "Career",
        "english": "A curated collection of your best live projects, code repositories, and evidence demonstrating what you can actually build.",
        "tanglish": "Certificates mattum kaataama, 'Idho naane build panna 3 projects, live link idho, code idho'-nu unga thiramaya prove panra showcase.",
        "tip": "Three solid working projects with demo links are 10x more persuasive than 20 course completion badges."
    },
    "ci/cd": {
        "term": "CI/CD (Continuous Integration / Continuous Deployment)",
        "category": "DevOps",
        "english": "Automated pipeline that tests your code whenever you make changes and automatically deploys healthy code to users.",
        "tanglish": "Neenga GitHub-la code upload pannavudane, automatic-ah tests run aagi, ella mistakes-um check pannittu, website-la deploy aagura smart pipeline.",
        "tip": "GitHub Actions is a free and popular way to practice simple CI/CD."
    },
    "framework": {
        "term": "Framework (e.g. React, Express)",
        "category": "Concepts",
        "english": "A pre-built structure and library of reusable code tools that speeds up building applications without reinventing the wheel.",
        "tanglish": "Veedu kattum podhu readymade scaffolding maadhiri! Scratch-la irundhu basic things panna theva illa; standard rules & helpers irukkum, adha vechu fast-ah app build pannalaam.",
        "tip": "Master the core language (JavaScript or Python) first before jumping straight into a framework."
    },
    "pull request": {
        "term": "Pull Request (PR)",
        "category": "Tools",
        "english": "A request made to project maintainers asking them to review and merge your proposed code changes into the main codebase.",
        "tanglish": "'Naan indha issue-ku solution ezhudhirukken, check pannittu unga main project-oda sethukonga' nu maintainer-kita kekkum polite request.",
        "tip": "Keep your pull requests small and write a friendly 2-sentence description of what you changed."
    },
    "full stack": {
        "term": "Full Stack",
        "category": "Career",
        "english": "Proficiency in both the user-facing visual frontend and the server-database backend of an application.",
        "tanglish": "Front-end (kannula theriyura screen) and Back-end (pinnaadi odura server, database) rendu side-layum work panna therinja all-rounder.",
        "tip": "You don't need to know everything at day 1. Start with frontend and slowly connect a simple database."
    }
}

with open("data/jargon.json", "w") as f:
    json.dump(jargon, f, indent=2)

# 5. PERSONAS (3 preloaded demo personas)
personas = {
    "arun": {
        "name": "Arun Kumar",
        "avatar": "🏕️",
        "background": "State Board (Tamil Medium), Rural Tier-3 College",
        "branch": "Information Technology",
        "board": "State Board",
        "current_comfort": "Beginner - knows basic HTML, anxious about technical interviews",
        "confidence_level": "Nervous, worries his English and background are handicaps",
        "weekly_hours": 10,
        "stress_level": "High (wants to support his family, scared of complex coding jargon)",
        "target_role": "Full Stack Developer",
        "learner_type": "Foundation",
        "self_ratings": {
            "HTML/CSS": 3,
            "Git & GitHub": 1,
            "JavaScript": 1,
            "React": 1,
            "Node.js": 1,
            "SQL": 1
        },
        "verified_skills": {
            "HTML/CSS": {
                "level": 2,
                "verified_date": "2026-10-15",
                "quiz_score": 85,
                "viva_score": 80,
                "project_url": "https://github.com/arun-dev/state-board-notes-portal",
                "attempts": 1,
                "time_taken_days": 6
            }
        },
        "failed_attempts": [
            {
                "skill": "JavaScript",
                "attempt_date": "2026-10-22",
                "quiz_score": 42,
                "feedback": "Needs revision on asynchronous event loop and callback functions. Curator suggested lightweight practice exercises."
            }
        ],
        "mentor_notes": "Warm encouragement, Tanglish explanations enabled, step-by-step small wins. Emphasize that language is just communication, logic is what matters.",
        "pressure_free_mode": True
    },
    "meena": {
        "name": "Meena Sundaram",
        "avatar": "🧬",
        "background": "B.Tech Biotechnology, Top State University",
        "branch": "Biotechnology",
        "board": "CBSE",
        "current_comfort": "Comfortable with lab biology and molecular genetics; very basic Python only",
        "confidence_level": "Curious but hesitant if non-CS engineers can succeed in tech",
        "weekly_hours": 15,
        "stress_level": "Medium (wants to transition into computational genomics without repeating 4 years)",
        "target_role": "Bioinformatics Analyst",
        "learner_type": "Bridge",
        "self_ratings": {
            "Biology Domain Knowledge": 5,
            "Python": 2,
            "Biopython & Genomic Data": 1,
            "SQL": 1,
            "Next-Gen Sequencing Basics": 2
        },
        "verified_skills": {
            "Biology Domain Knowledge": {
                "level": 4,
                "verified_date": "2026-09-20",
                "quiz_score": 96,
                "viva_score": 94,
                "project_url": "https://github.com/meena-bio/crispr-target-pathway-audit",
                "attempts": 1,
                "time_taken_days": 4
            },
            "Python": {
                "level": 2,
                "verified_date": "2026-10-05",
                "quiz_score": 78,
                "viva_score": 75,
                "project_url": "https://github.com/meena-bio/dna-fasta-gc-calculator",
                "attempts": 1,
                "time_taken_days": 8
            }
        },
        "failed_attempts": [],
        "mentor_notes": "Bridge Path activated: Explicitly celebrate biology domain depth. Show that software engineers lack biology context, so her domain + Python makes her an elite niche candidate.",
        "pressure_free_mode": False
    },
    "karthik": {
        "name": "Karthik Raja",
        "avatar": "⚡",
        "background": "Computer Science, Tier-2 Engineering College",
        "branch": "Computer Science & Engineering",
        "board": "CBSE",
        "current_comfort": "Strong in C and Python DSA, but burned out by peer pressure and competitive coding",
        "confidence_level": "High technical ability, but emotionally exhausted and cynical about certificates",
        "weekly_hours": 20,
        "stress_level": "High (Burnout risk from 100+ LeetCode expectations, lacks modern web framework practical skills)",
        "target_role": "Full Stack Developer",
        "learner_type": "Pressure-relief",
        "self_ratings": {
            "HTML/CSS": 3,
            "Git & GitHub": 4,
            "JavaScript": 2,
            "React": 1,
            "Node.js": 1,
            "SQL": 4
        },
        "verified_skills": {
            "SQL": {
                "level": 3,
                "verified_date": "2026-09-10",
                "quiz_score": 92,
                "viva_score": 90,
                "project_url": "https://github.com/karthik-r/campus-placement-db-optimizer",
                "attempts": 1,
                "time_taken_days": 3
            },
            "Git & GitHub": {
                "level": 3,
                "verified_date": "2026-09-18",
                "quiz_score": 95,
                "viva_score": 88,
                "project_url": "https://github.com/karthik-r/dotfiles-developer-setup",
                "attempts": 1,
                "time_taken_days": 2
            },
            "HTML/CSS": {
                "level": 2,
                "verified_date": "2026-10-02",
                "quiz_score": 82,
                "viva_score": 78,
                "project_url": "https://github.com/karthik-r/minimalist-dev-portfolio",
                "attempts": 1,
                "time_taken_days": 4
            }
        },
        "failed_attempts": [
            {
                "skill": "React",
                "attempt_date": "2026-10-25",
                "quiz_score": 45,
                "feedback": "Tripped up on useEffect dependency arrays and state closures. Mentor intervened to remove streak penalties and provide focused debugging drills."
            }
        ],
        "mentor_notes": "Pressure-Relief mode: No streaks, no countdown clocks, zero competitive leaderboards. Focus on high-autonomy project building where he has creative ownership.",
        "pressure_free_mode": True
    }
}

with open("data/personas.json", "w") as f:
    json.dump(personas, f, indent=2)

# 6. COHORT (60 mock students for Institution Dashboard)
random.seed(42)

first_names = [
    "Aadhira", "Abhishek", "Ananya", "Arun", "Bhavani", "Chirag", "Deepak", "Divya", "Eashwar", "Gokul",
    "Harini", "Hari", "Ilan", "Ishwarya", "Jeeva", "Kavya", "Keerthi", "Madhav", "Manish", "Meena",
    "Manoj", "Naveen", "Nisha", "Pavithra", "Pranav", "Pooja", "Raghav", "Rahul", "Ramya", "Revathi",
    "Rithanya", "Sanjay", "Saravanan", "Sathish", "Shalini", "Sharanya", "Siddharth", "Sindhu", "Sneha", "Sriram",
    "Subash", "Sudhir", "Surya", "Swetha", "Tamilselvan", "Tarun", "Thendral", "Uma", "Vaishnavi", "Varun",
    "Vignesh", "Vijay", "Vinoth", "Vishal", "Yalini", "Yuvan", "Abirami", "Balaji", "Chandran", "Gayathri"
]

branches = ["Computer Science", "Information Technology", "Electronics & Comm", "Biotechnology", "Mechanical Eng", "Data Science"]
boards = ["State Board", "CBSE", "ICSE / Other"]
role_pool = ["Full Stack Developer", "Data Analyst", "AI/ML Engineer", "Bioinformatics Analyst", "Frontend Developer"]

cohort = []
for i, name in enumerate(first_names):
    branch = branches[i % len(branches)]
    board = random.choices(boards, weights=[0.55, 0.35, 0.10])[0]
    target_role = role_pool[i % len(role_pool)]
    
    # Skills based on target role
    role_info = roles[target_role]
    student_skills = {}
    
    for sname, sdata in role_info["skills"].items():
        # Probability of having verified skill depends on board/branch mock logic
        target_lvl = sdata["target_level"]
        prob = 0.5
        if board == "CBSE":
            prob += 0.15
        if "Computer" in branch or "Data" in branch or "IT" in branch:
            prob += 0.15
            
        if random.random() < prob:
            # Verified at some level
            achieved_lvl = random.randint(1, target_lvl)
            student_skills[sname] = {
                "verified_level": achieved_lvl,
                "target_level": target_lvl,
                "quiz_avg": random.randint(70, 98),
                "verified_days_ago": random.randint(5, 80)
            }
        else:
            student_skills[sname] = {
                "verified_level": 0,
                "target_level": target_lvl,
                "quiz_avg": 0,
                "verified_days_ago": 0
            }
            
    # Calculate student readiness
    total_wt = sum(s["weight"] for s in role_info["skills"].values())
    earned_wt = sum(
        (student_skills[sn]["verified_level"] / role_info["skills"][sn]["target_level"]) * role_info["skills"][sn]["weight"]
        for sn in role_info["skills"]
    )
    readiness = int((earned_wt / total_wt) * 100)
    
    cohort.append({
        "id": f"STU-{1000 + i}",
        "name": name,
        "branch": branch,
        "board": board,
        "target_role": target_role,
        "readiness_score": readiness,
        "skills": student_skills,
        "at_risk": readiness < 40 and board == "State Board"
    })

with open("data/cohort.json", "w") as f:
    json.dump(cohort, f, indent=2)

print("All seed data generated successfully in /data!")

