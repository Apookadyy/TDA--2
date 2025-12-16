# SocialSite -- Django Social Networking Platform

SocialSite is a fully functional social media web application built
using **Django**.\
It allows users to create profiles, create posts, like/unlike content,
comment, and interact with other users.\
The project includes authentication, user feed, admin management, and a
clean UI built with HTML, CSS, and Bootstrap.

------------------------------------------------------------------------

## 🚀 Features

### 👤 User Accounts

-   User Registration & Login (Django Authentication)
-   Edit Profile (bio, profile picture)
-   View Other Users' Profiles

### 📝 Posts

-   Create, Edit, Delete Posts
-   Add images to posts
-   Like/Unlike Posts
-   Comment on Posts

### 📰 News Feed

-   View posts from all users
-   Sorted by most recent

### 🛠 Admin Panel

-   Manage Users
-   Manage Posts
-   Manage Comments
-   View Reports

### 🎨 Frontend

-   HTML, CSS, Bootstrap
-   Responsive UI

------------------------------------------------------------------------

## 📂 Project Structure

    SocialSite/
    │── manage.py
    │── requirements.txt
    │
    ├── SocialSite/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    │
    ├── accounts/
    │   ├── models.py
    │   ├── views.py
    │   ├── forms.py
    │   ├── urls.py
    │   └── templates/accounts/
    │
    ├── posts/
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── templates/posts/
    │
    ├── static/
    │── templates/

------------------------------------------------------------------------

## 🛠 Installation & Setup

1.  **Clone the repository**

```{=html}
<!-- -->
```
    git clone https://github.com/yourusername/SocialSite.git
    cd SocialSite

2.  **Create & activate virtual environment**

```{=html}
<!-- -->
```
    python -m venv env
    env\Scripts\activate   # Windows
    source env/bin/activate   # Mac/Linux

3.  **Install dependencies**

```{=html}
<!-- -->
```
    pip install -r requirements.txt

4.  **Run migrations**

```{=html}
<!-- -->
```
    python manage.py makemigrations
    python manage.py migrate

5.  **Create superuser**

```{=html}
<!-- -->
```
    python manage.py createsuperuser

6.  **Run server**

```{=html}
<!-- -->
```
    python manage.py runserver

------------------------------------------------------------------------

## 🧪 Tests

The `tests.py` includes: - User registration\
- Login\
- Post creation\
- Like/unlike\
- Commenting\
- Profile update

Run tests using:

    python manage.py test

------------------------------------------------------------------------


------------------------------------------------------------------------

## 💬 Support

Feel free to reach out if you need help!

