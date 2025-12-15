MemoryLane — Digital Time Capsule Platform

MemoryLane is a digital time capsule web application that allows users to preserve memories (text, photos, audio, and video) and unlock them in the future — either on a specific date or after a life event.
It focuses on privacy, emotional storytelling, and family collaboration.

Built using Django 6, designed to be deployable and production-ready.

🚀 Features
🔐 Digital Time Capsules

Create time capsules with:

📝 Text messages

🖼️ Images

🎧 Audio

🎥 Videos

Capsules unlock:

📅 On a future date

🎉 On a life event (manual trigger)

👥 Sharing & Privacy

Assign recipients to capsules

Privacy levels:

Private

Family

Public

Access controlled at backend level

🤝 Collaboration

Add collaborators to a capsule

Collaborators can contribute memories

Contributions appear after unlock

⏳ Countdown & Unlock

Live countdown timer for locked capsules

Automatic unlock when time/event condition is met

🔔 In-App Notifications

Users receive notifications when:

A capsule unlocks

They are added as recipient/collaborator

Notification count updates without page refresh

💬 Post-Unlock Interaction

Comments and reflections after unlock

Emoji reactions to memories

🛠️ Tech Stack

Backend: Django 6

Frontend: HTML, CSS, JavaScript

Database: SQLite (development)

Media Storage: Cloudinary

Static Files: WhiteNoise

Authentication: Custom User Model (AbstractUser)

Deployment: Render

📂 Project Structure

memorylane/
├── app/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/app/
├── templates/
│   ├── main.html
│   └── navbar.html
├── static/
│   ├── styles/
│   │   └── style.css
│   └── js/
│       └── main.js
├── website/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── README.md

Environment Variables:
SECRET_KEY=your_django_secret_key
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

Local Setup
1️⃣ Clone the repository
git clone https://github.com/RaUnAkKS/memorylane.git
cd memorylane

2️⃣ Create virtual environment
python -m venv env
env\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Run the server
python manage.py runserver


Open:

http://127.0.0.1:8000

🌐 Deployment Notes (Render)

Static files are handled using WhiteNoise

Media files are stored on Cloudinary

Migrations are run automatically during build

Build Command
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput

Start Command
gunicorn website.wsgi:application


🙌 Author

Raunak
B.Tech Student | Django Developer
Built during a hackathon 🚀

📜 License

This project is for educational and hackathon purposes.

Running server link : https://memorylane-bg2f.onrender.com
