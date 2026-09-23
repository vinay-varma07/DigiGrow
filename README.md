# DigiGrow Full-Stack CEP Project

Digital Marketing Training for Small Businesses.

## Stack
- Python + Flask
- Flask-SQLAlchemy
- SQLite
- HTML/CSS/JavaScript
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

The admin dashboard is intended for the local CEP demonstration. If the project is deployed publicly, add authentication before exposing `/admin`.

The SQLite database `digigrow.db` is created automatically when the Flask app starts.
