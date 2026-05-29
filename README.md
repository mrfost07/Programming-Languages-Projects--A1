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
   git clone <repo-url>
   cd ProgrammingLanguageProject-A1
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

## Rules

- Only edit files inside your own group folder.
- Include a `README.md` inside your folder describing your project, members, and how to run it.
- Do not commit large binaries, build artifacts, or virtual environments (see `.gitignore`).
