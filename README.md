# DigiGrow Full-Stack CEP Project

Digital Marketing Training for Small Businesses.

## Stack
- Python + Flask
- Flask-SQLAlchemy
- PostgreSQL for production on Render
- SQLite as the local fallback when `DATABASE_URL` is not set
- HTML, CSS and JavaScript
- Chart.js for the admin dashboard charts

## Run on Windows
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Main pages
- `/` Home
- `/about` About
- `/training` Training modules
- `/survey` Pre/Post survey
- `/results` Public results and comparison
- `/contact` Contact/help
- `/admin` Admin dashboard

## Admin dashboard
The dashboard provides:
- Survey response counts
- Pre/post confidence and online-presence comparison charts
- Platform usage chart
- Training module view counts
- Full survey-response table
- Contact-message table
- Common challenge summary
- CSV export at `/admin/export/surveys`

Admin credentials are read from environment variables:
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `SECRET_KEY`

## Database
The application reads the database connection from `DATABASE_URL`.

- Local development: if `DATABASE_URL` is not set, SQLite is used automatically.
- Render production: set `DATABASE_URL` to the Internal Database URL of the Render PostgreSQL database.
- Database tables are created automatically when the Flask application starts.

## CSS structure
Shared styles are stored in `static/css/base.css`. Each HTML page also has its own stylesheet:

- `index.css`
- `about.css`
- `training.css`
- `module.css`
- `survey.css`
- `results.css`
- `contact.css`
- `admin_login.css`
- `admin.css`
- `404.css`

This keeps page-specific styling separate while avoiding repeated global styles.
