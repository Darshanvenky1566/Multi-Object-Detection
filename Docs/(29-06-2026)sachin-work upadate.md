# Work Log — 29 June 2026

**Project:** NexVision — Multi-Object Detection
**Author:** Sachin Adihalli Ravigowda

## What I did today

### Repository cleanup
- Pulled the latest team code from main and reviewed recent updates from teammates.
- Identified duplicate files in the repo — the docs and database scripts had been
  committed twice (once at the project root, once inside a nested
  `Multi-Object-Detection/` folder and a `.env/updates/` folder).
- Created a `cleanup-duplicate-folder` branch and removed the duplicate nested
  folder (14 files) and the misplaced `.env/updates/` db scripts (2 files).
- Opened a pull request for review so the deletions could be checked by the team.

### Git workflow
- Practised the full branch → commit → push → pull request workflow.
- Kept each change on its own branch to keep pull requests focused.
- Added my class work log to the Docs folder via a separate branch and merged it.

### Housekeeping
- Added Flask runtime files (`flask_pid.txt`, `flask_job_id.txt`) and `*.log`
  to `.gitignore` so temporary generated files are no longer tracked in git.

### Deployment progress
- Continued setting up Docker and Portainer to run the application in a container.
- Worked through deployment issues (missing `requirements.txt`, environment setup).

## What I learned
- How to identify and safely remove duplicate files using branches and pull requests.
- The importance of keeping runtime/generated files out of version control.
- Team collaboration etiquette — letting teammates review changes to their own files.

## Next steps
- Finish deploying the app in Docker / Portainer.
- Connect the database with credentials stored securely in environment variables.
