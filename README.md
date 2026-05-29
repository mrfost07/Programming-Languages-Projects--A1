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

## Example (Windows Walkthrough)

You're from group **Fajardo-Baybay** and your project files are sitting somewhere on your computer (Desktop, Downloads, USB, wherever). Replace `Fajardo-Baybay` with **your own** group folder name as you follow along.

Make sure Git is installed first: https://git-scm.com/download/win (default options are fine). After installing, you'll have **Git Bash** on your computer.

### Step 1 — Make a new folder for the project on your PC

1. Open **File Explorer** (Win + E).
2. Go wherever you want to keep this — for example, your **Desktop**.
3. Right-click on empty space → **New** → **Folder**.
4. Name it something like `GitHub Projects`. This is just a parent folder to keep things tidy.
5. Double-click into `GitHub Projects` so you're now **inside** it.

### Step 2 — Clone the repo into that folder

While you're inside the `GitHub Projects` folder:

1. Right-click on empty space inside the folder.
2. Choose **Open Git Bash here** (or **Show more options** → Open Git Bash here on Windows 11).
3. A black terminal window opens. Paste this and press Enter:
   ```bash
   git clone https://github.com/mrfost07/Programming-Languages-Projects--A1.git
   ```
4. Wait for it to finish. You'll see a new folder called `Programming-Languages-Projects--A1` appear inside `GitHub Projects`.

### Step 3 — Open the cloned folder

Back in File Explorer, double-click the new folder: `Programming-Languages-Projects--A1`.

Inside, you'll see all the group folders — including yours.

### Step 4 — Make your branch (so you don't push to main)

1. Right-click on empty space inside `Programming-Languages-Projects--A1` → **Open Git Bash here**.
2. Paste this (change the group name to yours):
   ```bash
   git checkout -b submission/Fajardo-Baybay
   ```
3. You should see: `Switched to a new branch 'submission/Fajardo-Baybay'`. Keep this terminal open.

### Step 5 — Open your project's original folder

In a **second** File Explorer window, go to wherever your project files actually live — wherever you've been working on your project (Desktop, Documents, etc.).

Select **all** the files and folders that make up your project (Ctrl + A). Right-click → **Copy** (or Ctrl + C).

### Step 6 — Paste your project into your group's folder

1. Switch back to the File Explorer window showing `Programming-Languages-Projects--A1`.
2. Double-click your group's folder (e.g. `Fajardo-Baybay`).
3. Right-click on empty space → **Paste** (or Ctrl + V).

Your group's folder should now contain all your project files. It might look like this:

```
Fajardo-Baybay/
├── README.md
├── calculator.py
└── tests/
    └── test_calculator.py
```

⚠️ **Do not put files in the root of the repo. Do not edit other groups' folders.**

### Step 7 — Commit and push

Go back to the Git Bash terminal you left open in Step 4. Run these one by one:

```bash
git add Fajardo-Baybay/
git commit -m "Submit: Fajardo-Baybay project"
git push -u origin submission/Fajardo-Baybay
```

If GitHub asks for login, sign in with your GitHub account in the popup window. (If you don't have a GitHub account, make one at https://github.com first.)

### Step 8 — Open a Pull Request

1. Go to https://github.com/mrfost07/Programming-Languages-Projects--A1
2. You'll see a yellow banner: **Compare & pull request** — click it.
3. Title: `Submission: Fajardo-Baybay`
4. Description: list your members and a short description of your project.
5. Click **Create pull request**.

Done. ✅

### Full command summary

You'll only ever type these inside Git Bash. Replace `Fajardo-Baybay` with your group:

```bash
# After right-clicking → Open Git Bash here inside your "GitHub Projects" folder:
git clone https://github.com/mrfost07/Programming-Languages-Projects--A1.git

# After right-clicking → Open Git Bash here inside the cloned folder:
git checkout -b submission/Fajardo-Baybay
# (now copy-paste your project files into the Fajardo-Baybay folder using File Explorer)
git add Fajardo-Baybay/
git commit -m "Submit: Fajardo-Baybay project"
git push -u origin submission/Fajardo-Baybay
```

## Rules

- Only edit files inside your own group folder.
- Include a `README.md` inside your folder describing your project, members, and how to run it.
- Do not commit large binaries, build artifacts, or virtual environments (see `.gitignore`).
