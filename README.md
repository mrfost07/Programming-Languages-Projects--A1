# Programming Languages Project A1

Submission repository for our Programming Languages class projects. Each group has its own folder. Push your project files into your group's folder only.

## Groups

- Fajardo-Baybay
- Aldueza-Capales
- Diamola-Vallezer
- Eludi-Cabiling
- Gemparo-Deanmark
- Caling-Taro
- Menguito-Vasquez_Nico
- Lumpas-Gargao
- Ligad-Vasquez_Justine
- Anislag-Camingue-Galo
- Romanillos-Gepalla

## How to Submit

1. Clone this repository:
   ```bash
   git clone https://github.com/mrfost07/Programming-Languages-Projects--A1.git
   cd Programming-Languages-Projects--A1
   ```

2. Create a feature branch with your group name:
   ```bash
   git checkout -b submission/<your-group-folder>
   ```

3. Place all your project files inside your group's folder (e.g. `Fajardo-Baybay/`). Do not modify other groups' folders.

4. Commit and push:
   ```bash
   git add <your-group-folder>/
   git commit -m "Submit: <your-group-folder>"
   git push -u origin submission/<your-group-folder>
   ```

5. Open a Pull Request on GitHub targeting the `main` branch.

## Example (Step-by-Step Walkthrough)

Pretend you're from group **Fajardo-Baybay** and your project is a **simple calculator written in Python**. Here's exactly what to do, from zero to a submitted Pull Request. Replace `Fajardo-Baybay` with **your own** group folder name.

### Step 1 — Open a terminal

- **Windows**: right-click on your Desktop → "Git Bash Here" (install Git from https://git-scm.com if you don't have it).
- **Mac/Linux**: open the Terminal app.

### Step 2 — Move into a folder where you want the code to live

```bash
cd Desktop
```

### Step 3 — Clone the repository (download a copy)

```bash
git clone https://github.com/mrfost07/Programming-Languages-Projects--A1.git
cd Programming-Languages-Projects--A1
```

After this, you'll be **inside** the repo folder.

### Step 4 — Make sure you have the latest version

```bash
git checkout main
git pull origin main
```

### Step 5 — Create your own branch

A branch is your personal copy of the project where your changes live until they're merged.

```bash
git checkout -b submission/Fajardo-Baybay
```

You should see: `Switched to a new branch 'submission/Fajardo-Baybay'`.

### Step 6 — Add your project files into your group's folder

Open the repo in your file explorer. Find the `Fajardo-Baybay/` folder. **Copy your project files into it.**

After copying, the folder should look like this:

```
Fajardo-Baybay/
├── README.md             ← describe your project, members, how to run
├── calculator.py         ← your code
└── tests/
    └── test_calculator.py
```

⚠️ **Do not put files in the root of the repo. Do not edit other groups' folders.**

### Step 7 — Replace the placeholder README inside your folder

Open `Fajardo-Baybay/README.md` and replace it with something real. Example:

```markdown
# Fajardo-Baybay — Simple Calculator

## Members
- Juan Fajardo
- Maria Baybay

## Description
A command-line calculator in Python that supports +, -, *, /, and exponentiation.

## How to Run
1. Make sure Python 3.10+ is installed: `python --version`
2. From inside this folder, run: `python calculator.py`

## Requirements
- Python 3.10 or newer
```

### Step 8 — Check what you're about to commit

```bash
git status
```

Every changed file listed should start with `Fajardo-Baybay/`. If anything else shows up, stop and fix it.

### Step 9 — Stage your group's folder

```bash
git add Fajardo-Baybay/
```

### Step 10 — Commit with a clear message

```bash
git commit -m "Submit: Fajardo-Baybay calculator project"
```

### Step 11 — Push your branch to GitHub

```bash
git push -u origin submission/Fajardo-Baybay
```

If GitHub asks for a username and password, use your GitHub username and a **Personal Access Token** as the password (create one at https://github.com/settings/tokens with `repo` scope).

### Step 12 — Open a Pull Request

1. Go to https://github.com/mrfost07/Programming-Languages-Projects--A1
2. You'll see a yellow banner: **Compare & pull request** — click it.
3. Title: `Submission: Fajardo-Baybay`
4. Description: list your members and describe your project briefly.
5. Click **Create pull request**.

Done. ✅

### Full command summary (copy-paste friendly)

```bash
cd Desktop
git clone https://github.com/mrfost07/Programming-Languages-Projects--A1.git
cd Programming-Languages-Projects--A1
git checkout main
git pull origin main
git checkout -b submission/Fajardo-Baybay
# (copy your project files into the Fajardo-Baybay/ folder now)
git status
git add Fajardo-Baybay/
git commit -m "Submit: Fajardo-Baybay calculator project"
git push -u origin submission/Fajardo-Baybay
```

## Rules

- Only edit files inside your own group folder.
- Include a `README.md` inside your folder describing your project, members, and how to run it.
- Do not commit large binaries, build artifacts, or virtual environments (see `.gitignore`).
