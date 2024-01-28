# MAILSENDER
#### Description:
- MAILSENDER is a Flask-based web application that implements a simple email system. It includes features such as user registration, authentication, email composition, inbox, sentbox, and email detail view. The project utilizes SQLite for database management, Flask for web development, and the CS50 library for simplified database interactions.

# Features:
User Registration and Authentication:

Users can register for an account with a unique username and password.
Passwords are securely hashed using the generate_password_hash function from the werkzeug.security module.
User authentication is implemented, ensuring that only registered users can access certain pages.
Email Composition:

Registered users can compose emails, providing the recipient, subject, and body of the email.
Basic form validation is implemented to ensure that no fields are left empty.
Inbox and Sentbox:

Users can view their inbox, displaying emails received by them.
The sentbox allows users to view emails they have sent.
Email Detail View:

Users can click on an email to view its details, including sender, recipient, subject, timestamp, and body.
File Structure:
app.py: The main Flask application file containing the routes and configurations.
helpers.py: Contains helper functions, including the apology, login_required, lookup, and usd functions.
project.db: SQLite database file storing user information and emails.
templates: Directory containing HTML templates for rendering pages.
static: Directory for static files such as stylesheets.
How to Run:
Install required packages: Flask, cs50, and werkzeug.

bash
Copy code
pip install Flask cs50 Werkzeug
Run the application:

bash
Copy code
flask run
The application will be accessible at http://127.0.0.1:5000/ in your web browser.

# Dependencies:
Flask: The web framework used for building the application.
CS50 Library: Simplifies interactions with the SQLite database.
Werkzeug: Provides password hashing and security features.
Notes:
Ensure that the required dependencies are installed before running the application.
The SQLite database (project.db) is used to store user information and emails.
Feel free to customize, enhance, and expand upon this template for your own email system project.
Email Detail View Template (email_detail.html):
html
Copy code
{% extends "layout.html" %}

{% block title %}
    Email Details
{% endblock %}

{% block main %}
    <div>
        <div class="list-group-item">
            <strong>Sender: </strong> {{ emailDetail.sender }}
        </div>
        <div class="list-group-item">
            <strong>Recipient: </strong> {{ emailDetail.recipient }}
        </div>
        <div class="list-group-item">
            <strong>Subject: </strong> {{ emailDetail.subject }}
        </div>
        <div class="list-group-item">
            <strong>TimeStamp: </strong> {{ emailDetail.timestamp }}
        </div>
        <div class="list-group-item">
            <strong>Body: </strong> {{ emailDetail.body }}
        </div>
    </div>
{% endblock %}
Inbox Template (inbox.html):
html
Copy code
{% extends "layout.html" %}

{% block title %}
    Inbox
{% endblock %}

{% block main %}
    <div>
        {% for email in emails %}
        <div class="list-group-item">
            <h6>Sender: {{ email.sender }}</h6>
            <h2>{{ email.subject }}</h2>
            <p>{{ email.timestamp }}</p>
            <form action="email" method="post">
                <input type="hidden" name="emailId" value="{{ email.id }}">
                <input type="submit" class="btn btn-info" value="View Email">
            </form>
        </div>
        {% endfor %}
    </div>
{% endblock %}
Styles (styles.css):
css
Copy code
/* Size for brand */
nav .navbar-brand {
    font-size: xx-large;
}

/* Colors for brand */
nav .navbar-brand .blue {
    color: #537fbe;
}
nav .navbar-brand .red {
    color: #ea433b;
}
nav .navbar-brand .yellow {
    color: #f5b82e;
}
nav .navbar-brand .green {
    color: #2e944b;
}

textarea {
    width: 200px;
    height: 100px;
    border: 1px solid lightgray;
    border-radius: 10px;
}

.list-group-item {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}
Junk Template (junk.html):
html
Copy code
{% extends "layout.html" %}

{% block title %}
    Junk
{% endblock %}

{% block main %}
    <form action="/junk" method="post">
        <div class="mb-3">
            <label>FROM: </label>
            <input autocomplete="off" autofocus class="form-control mx-auto w-auto" id="username" name="sender" value="{{ sender }}" type="text">
        </div>
        <label>TO: </label>
        <div class="mb-3">
            <input class="form-control mx-auto w-auto" id="recipient" name="recipient" placeholder="Recipient" type="text">
        </div>
        <label>Subject: </label>
        <div class="mb-3">
            <input class="form-control mx-auto w-auto" id="subject" name="subject" placeholder="Subject" type="text">
        </div>
        <div class="mb-3">
            <textarea name="body"></textarea>
        </div>
        <button class="btn btn-primary" type="submit">Send</button>
    </form>
{% endblock %}
Register Template (register.html):
html
Copy code
{% extends "layout.html" %}

{% block title %}
    Register
{% endblock %}

{% block main %}
    <form action="/register" method="post">
        <div class="mb-3">
            <input autocomplete="off" autofocus class="form-control mx-auto w-auto" name="username" placeholder="Username" type="text">
        </div>
        <div class="mb-3">
            <input class="form-control mx-auto w-auto" name="password" placeholder="Password (again)" type="password">
        </div>
        <div class="mb-3">
            <input class="form-control mx-auto w-auto" name="confirmation" placeholder="Confirm password" type="password">
        </div>
        <button class="btn btn-primary" type="submit">Register</button>
    </form>
{% endblock %}
Layout Template (layout.html):
html
Copy code
<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Head content here -->
</head>

<body>

    <nav class="bg-light border navbar navbar-expand-md navbar-light">
        <!-- Navigation content here -->
    </nav>

    {% if get_flashed_messages() %}
        <header>
            <div class="alert alert-primary mb-0 text-center" role="alert">
                {{ get_flashed_messages() | join(" ") }}
            </div>
        </header>
    {% endif %}

    <main class="container py-5 text-center">
        {% block main %}{% endblock %}
    </main>

    <footer class="mb-5">
        <!-- Footer content here -->
    </footer>

</body>

</html>
Feel free to customize the templates and styles to fit your project's specific needs.
