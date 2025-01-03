# Billify

**Billify** is a Flask-based web application that scrapes the [Billboard Hot 100](https://www.billboard.com/charts/hot-100) for a user-selected date and creates a Spotify playlist with those songs. It also includes a contact form that sends an email using Gmail’s SMTP server.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Environment Variables](#environment-variables)
7. [Running the App Locally](#running-the-app-locally)
8. [Docker Usage](#docker-usage)
9. [Testing](#testing)
10. [License](#license)
11. [Contributing](#contributing)

---

## Project Overview

**Billify** lets you:
1. Enter a date via the home page form (e.g., “YYYY-MM-DD”).
2. Scrape Billboard’s top 100 for that date using BeautifulSoup.
3. Create a **private** Spotify playlist with those songs in your Spotify account.
4. Optionally send a message through the “Contact” page, which is then emailed to you using Gmail’s SMTP.

---

## Features

- **Scrape Billboard**: Uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to gather song data from Billboard.
- **Spotify Playlist Creation**: Leverages [Spotipy](https://spotipy.readthedocs.io/) for OAuth and playlist management.
- **Simple Contact Form**: Submits user data and emails it to your inbox using Gmail’s SMTP service.
- **Flask Routes**: 
  - **Home (/)**: Enter date form, display top 100 songs.
  - **Contact (/contact)**: Send an email inquiry.
  - **About (/about)**: Basic info page.
- **OAuth Flow** with Spotify: Login, callback, token refresh.

---

## Tech Stack

- **Programming Language**: Python (3.9+)
- **Framework**: Flask
- **Web Scraping**: BeautifulSoup
- **Spotify Integration**: Spotipy
- **Email**: smtplib (Gmail SMTP)
- **Template Engine**: Jinja2

---

## Prerequisites

1. **Python 3.9+** (or a recent 3.x version).
2. **Pip** or **Poetry** (to install dependencies).
3. A **Spotify Developer** account with:
   - **Client ID**  
   - **Client Secret**  
   - **Redirect URI** set to `https://yourapp.example.com/callback` (or your production domain/callback).
4. A **Gmail Account** with either:
   - **App Password** (if 2FA is enabled), **or**  
   - “Less Secure Apps” (deprecated by Google, not recommended).
5. *(Optional)* **Docker** and **Docker Compose** if you plan to deploy in containers.

---

## Installation

1. **Clone** this repository:
   ```bash
   git https://github.com/JoeUzo/Billify-Web.git
   cd Billify-Web
   ```
2. **Create** and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   # or for Windows:
   .venv\Scripts\activate
   ```
3. **Install** dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Variables

The project uses a **`.env`** file to manage secrets and configurations. A sample `.env` might look like:

```dotenv
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SECRET_KEY=your_flask_secret_key
EMAIL_KEY=your_email_app_password
EMAIL=your_email_address@gmail.com
SPOTIPY_REDIRECT_URI=https://yourapp.example.com/callback
```

**Descriptions**:
- **`SPOTIFY_CLIENT_ID`**: Your Spotify developer client ID.
- **`SPOTIFY_CLIENT_SECRET`**: Your Spotify developer client secret.
- **`SPOTIPY_REDIRECT_URI`**: Must match your Spotify app settings.
- **`SECRET_KEY`**: Flask secret key (for sessions).  
- **`EMAIL`**: Gmail address used to send emails (e.g., “jo....ct@gmail.com”).  
- **`EMAIL_KEY`**: If your Gmail has 2FA, this should be an **App Password**.

**Security Note**: Don’t commit real secrets to public repos! Make sure `.env` is in your `.gitignore`.

---

## Running the App Locally

1. **Activate** your virtual environment and ensure `.env` is set correctly.
2. **Run** the Flask app:
   ```bash
   python app.py
   ```
3. Open your browser at [http://localhost:5000](http://localhost:5000).

---

## Docker Usage

1. **Build** the Docker image:
   ```bash
   docker build -t billify:latest .
   ```
2. **Run** the container (exposing port 5000):
   ```bash
   docker run -p 5000:5000 --env-file .env billify:latest
   ```
3. Visit [http://localhost:5000](http://localhost:5000) in your browser.

**Note**:  
- Ensure you copy or provide `.env` to the container using `--env-file .env` (or set environment variables in your Dockerfile, but never commit secrets publicly).  
- If you’re deploying to a remote server or Kubernetes, adapt accordingly.

---

## Testing

This project uses **pytest** for testing. Tests are located in `test_mail.py` (and possibly others).  
1. Install pytest (if not already):
   ```bash
   pip install pytest
   ```
2. Run tests:
   ```bash
   pytest tests/
   ```

**Mocking**: Some tests mock external services (like SMTP or Spotify). This prevents making real network calls.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

1. **Fork** the project.  
2. Create a **feature branch** (`git checkout -b feature/some-improvement`).  
3. **Commit** changes and push to your fork.  
4. Create a **Pull Request** describing your changes.  

Contributions are welcome if you’d like to improve this application—whether by refining the scraping logic, upgrading tests, or enhancing the UI.

---

**Thank you for using Billify!** If you encounter any issues or want to suggest improvements, feel free to open an [issue](https://github.com/your-username/billify/issues) or submit a pull request. Enjoy creating your throwback Spotify playlists!