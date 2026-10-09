# 🤝 Contributing to Smart Resume Analyzer

Thank you for your interest in contributing to **Smart Resume Analyzer**! 🎉

Whether you're fixing a bug, improving the UI, adding a feature, enhancing documentation, or optimizing performance, every contribution is appreciated.

If you're participating in **Elite Coders Summer of Code (ECSoC) 2026**, please read this guide before making your first contribution.

---

# 📑 Table of Contents

- Introduction
- Getting Started
- Prerequisites
- Project Setup
- Project Structure
- Ways to Contribute
- Branch Naming Convention
- Coding Standards
- Commit Message Guidelines
- Pull Request Workflow
- Contributor Checklist
- ECSoC Guidelines
- Code of Conduct
- Need Help?

---

# 🚀 Getting Started

## 1. Fork the Repository

Click the **Fork** button at the top-right of this repository.

## 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/smart-resume-analyzer.git
cd smart-resume-analyzer
```

## 3. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Run the Project

```bash
streamlit run app.py
```

Open your browser and visit

```
http://localhost:8501
```

---

# 📋 Prerequisites

Before contributing, make sure you have:

- Python 3.10+
- Git
- GitHub account
- Basic knowledge of Python
- Streamlit installed through requirements.txt

---

# 📁 Project Structure

```
smart-resume-analyzer/
│
├── app.py                 # Main Streamlit application
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
│
└── utils/
    ├── __init__.py
    ├── parser.py          # Resume parsing
    ├── analyzer.py        # NLP analysis
    ├── scorer.py          # ATS scoring
    ├── job_roles.py       # Role keywords
    └── report_generator.py # PDF report generation
```

---

# 💡 Ways to Contribute

You can contribute by:

- Fixing bugs
- Adding new features
- Improving ATS scoring
- Improving resume parsing
- Enhancing UI/UX
- Improving documentation
- Writing tests
- Optimizing performance
- Refactoring code

---

# 🛠 Contribution Workflow

## Step 1

Check the **Issues** section.

## Step 2

Choose an issue you'd like to work on.

## Step 3

Comment on the issue requesting assignment.

Example:

> I'd like to work on this issue. Please assign it to me.

Wait until a maintainer assigns it before starting work.

## Step 4

Create a new branch.

```bash
git checkout -b feature/add-dark-mode
```

or

```bash
git checkout -b fix/login-bug
```

---

# 🌿 Branch Naming Convention

Use meaningful branch names.

Examples:

```
feature/add-resume-preview

feature/improve-ui

fix/pdf-parser

fix/login-error

docs/update-readme

docs/add-contributing

refactor/analyzer

test/add-unit-tests
```

Avoid names like

```
branch1

new

update

test
```

---

# 🎨 Coding Standards

Please follow these practices:

- Write clean and readable code.
- Use meaningful variable names.
- Keep functions short.
- Reuse existing components whenever possible.
- Follow the existing project structure.
- Remove unused imports.
- Avoid duplicate code.
- Keep formatting consistent.

---

# 📝 Commit Message Guidelines

Use descriptive commit messages.

Good examples:

```
feat: add resume preview section

fix: resolve PDF upload issue

docs: add CONTRIBUTING guide

style: improve sidebar layout

refactor: simplify ATS scoring logic
```

Avoid:

```
update

changes

fix

done
```

---

# 🔄 Pull Request Process

Before opening a PR:

- Pull the latest changes.
- Resolve merge conflicts.
- Test your changes locally.
- Ensure the application runs successfully.

Push your branch:

```bash
git push origin feature/your-feature
```

Create a Pull Request against the **main** branch.

Your PR description should include:

- Summary of changes
- Screenshots (if UI changes)
- Testing performed
- Related issue

Example:

```
Fixes #4
```

Respond to review comments by pushing new commits to the same branch instead of opening another PR.

---

# ✅ Contributor Checklist

Before submitting your PR, verify:

- Code builds successfully
- No unnecessary files are included
- No merge conflicts
- Documentation updated (if needed)
- Screenshots added for UI changes
- Issue linked
- Branch is up to date
- Commit messages are meaningful

---

# 🏷 ECSoC Guidelines

This repository participates in **Elite Coders Summer of Code (ECSoC) 2026**.

Please note:

- Request issue assignment before working.
- Ensure your PR includes the **ECSoC26** label (applied by maintainers).
- Difficulty labels are assigned automatically after merge.
- Bonus labels are maintained by project admins.

---

# 📜 Code of Conduct

Please be respectful and professional.

Be kind and welcoming to all contributors.

Constructive feedback is encouraged.

Harassment or disrespectful behavior will not be tolerated.

If the repository includes a separate **CODE_OF_CONDUCT.md**, please follow it.

---

# 💬 Need Help?

If you're stuck:

- Open a GitHub Discussion
- Comment on the related issue
- Ask questions before making major changes

Maintainers are happy to help new contributors.

---

# ❤️ Thank You

Thank you for taking the time to contribute to Smart Resume Analyzer.

Every contribution—big or small—helps make the project better for everyone.

Happy Coding! 🚀