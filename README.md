<h1>Health Information System API</h1>

<p>A RESTful API for managing health programs and client enrollments, built with Flask, SQLAlchemy, and SQLite. The API supports creating programs, registering clients, enrolling clients in programs, searching clients, and retrieving client profiles, with data encryption, authentication, and caching. Swagger UI is integrated for API documentation.</p>

<h1>Table of Contents</h1>

<ul>
    <li><a href="#features">Features</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#setup">Setup</a></li>
    <li><a href="#running-the-application">Running the Application</a></li>
    <li><a href="#api-endpoints">API Endpoints</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#troubleshooting">Troubleshooting</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
</ul>

<h2 id="features">Features</h2>

<ul>
    <li><strong>Program Management:</strong> Create health programs with name and description.</li>
    <li><strong>Client Management:</strong> Register clients with encrypted personal data (name, date of birth).</li>
    <li><strong>Enrollment:</strong> Enroll clients in programs with a many-to-many relationship.</li>
    <li><strong>Search:</strong> Search clients by name (async support).</li>
    <li><strong>Profile Retrieval:</strong> Get client profiles with enrolled programs (cached for performance).</li>
    <li><strong>Security:</strong> Token-based authentication and data encryption using cryptography.</li>
    <li><strong>Documentation:</strong> Swagger UI for interactive API documentation at <code>/apidocs/</code>.</li>
    <li><strong>Modular Design:</strong> Code organized into modules (<code>app</code>, <code>models</code>, <code>routes</code>, etc.) for maintainability.</li>
</ul>

<h2 id="project-structure">Project Structure</h2>

<pre>
HIS/
├── .venv/               # Virtual environment (ignored by Git)
├── .git/                # Git repository
├── .gitignore           # Git ignore file
├── README.md            # This file
├── requirements.txt     # Python dependencies
├── health_system.db     # SQLite database (ignored by Git)
├── test_health_system.py # Unit tests
├── app/                 # Python package
│   ├── __init__.py      # Marks app/ as a package
│   ├── app.py           # Flask app initialization
│   ├── config.py        # Configuration (database URI, etc.)
│   ├── models.py        # SQLAlchemy models (Program, Client)
│   ├── routes.py        # API routes and Swagger documentation
│   ├── schemas.py       # JSON schemas for validation
│   ├── utils.py         # Utility functions (encryption)
</pre>

<h2 id="prerequisites">Prerequisites</h2>

<ul>
    <li><strong>Python 3.8+:</strong> Ensure Python is installed.</li>
    <li><strong>Git:</strong> For cloning and version control.</li>
    <li><strong>Git Bash (Windows):</strong> For running commands (or equivalent terminal).</li>
    <li><strong>SQLite:</strong> For the database (included with Python).</li>
</ul>

<h2 id="setup">Setup</h2>

<h3>Clone the Repository:</h3>
<pre>
git clone https://github.com/your-username/health-information-system.git
cd health-information-system
</pre>

<h3>Create a Virtual Environment:</h3>
<pre>
python -m venv .venv
source .venv/bin/activate  # On Windows Git Bash
# Or: source .venv/Scripts/activate
</pre>

<h3>Install Dependencies:</h3>
<pre>
pip install -r requirements.txt
</pre>

<h3>Initialize the Database:</h3>
<pre>
python -c "from app.app import create_app; app=create_app(); app.app_context().push(); from app.models import db; db.create_all()"
</pre>

<h2 id="running-the-application">Running the Application</h2>

<h3>Activate the Virtual Environment:</h3>
<pre>
source .venv/bin/activate
</pre>

<h3>Run the Flask App:</h3>
<pre>
python -m app.app
</pre>

<p>The server runs at <a href="http://localhost:5001">http://localhost:5001</a>.</p>

<h3>Access Swagger UI:</h3>
<p>Open <a href="http://localhost:5001/apidocs/">http://localhost:5001/apidocs/</a> in a browser to view API documentation.</p>

<h2 id="api-endpoints">API Endpoints</h2>

<p>All endpoints require authentication with the header <code>Authorization: Bearer secret-token-123</code>.</p>

<table>
    <thead>
        <tr>
            <th>Endpoint</th>
            <th>Method</th>
            <th>Description</th>
            <th>Payload Example</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>/programs</td>
            <td>POST</td>
            <td>Create a health program</td>
            <td><code>{"name": "TB", "description": "Tuberculosis Treatment"}</code></td>
        </tr>
        <tr>
            <td>/clients</td>
            <td>POST</td>
            <td>Register a client</td>
            <td><code>{"name": "John Doe", "date_of_birth": "1990-01-01", "gender": "Male"}</code></td>
        </tr>
        <tr>
            <td>/clients/&lt;client_id&gt;/enroll</td>
            <td>POST</td>
            <td>Enroll a client in a program</td>
            <td><code>{"program_id": "uuid-string"}</code></td>
        </tr>
        <tr>
            <td>/clients/search</td>
            <td>GET</td>
            <td>Search clients by name</td>
            <td>Query: <code>?name=John</code></td>
        </tr>
        <tr>
            <td>/clients/&lt;client_id&gt;</td>
            <td>GET</td>
            <td>Get client profile and enrolled programs</td>
            <td>None</td>
        </tr>
    </tbody>
</table>

<h2 id="testing">Testing</h2>

<pre>
python -m unittest test_health_system.py
</pre>

<h2 id="troubleshooting">Troubleshooting</h2>

<ul>
    <li><strong>No <code>health_system.db</code>:</strong> Run <code>python -m app.app</code> or the manual database creation command above.</li>
    <li><strong><code>/apidocs/</code> 404:</strong> Ensure <code>flasgger</code> is installed (<code>pip install flasgger</code>) and <code>Swagger(app)</code> is in <code>app/app.py</code>.</li>
    <li><strong>Port Conflicts:</strong> If port 5001 is in use, kill the process or change the port in <code>app/app.py</code>: <code>app.run(host='0.0.0.0', port=5002, debug=True)</code>.</li>
    <li><strong>OneDrive Issues:</strong> If sync errors occur, move the project: <code>mv /c/Users/User/OneDrive/Desktop/Interview/HIS /c/Users/User/Desktop/HIS</code>.</li>
</ul>

<h2 id="contributing">Contributing</h2>

<ol>
    <li>Fork the repository.</li>
    <li>Create a feature branch: <code>git checkout -b feature/your-feature</code>.</li>
    <li>Commit changes: <code>git commit -m "Add your feature"</code>.</li>
    <li>Push to the branch: <code>git push origin feature/your-feature</code>.</li>
    <li>Open a pull request.</li>
</ol>

<h2 id="license">License</h2>

<p>This project is licensed under the MIT License. See the <code>LICENSE</code> file for details.</p>
