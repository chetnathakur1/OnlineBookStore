# Online Bookstore Project
<body>
    <section id="installation">
        <h2>Installation</h2>
        <ol>
            <li>Clone the repository:
                <pre><code>git clone https://github.com/chetnathakur1/OnlineBookStore.git</code></pre>
            </li>
            <li>Create a virtual environment:
                <pre><code>python -m venv venv</code></pre>
            </li>
            <li>Activate virtual environment:
                <pre><code>source .venv/bin/activate</code></pre>
            </li>
            <li>Install project dependencies:
                <pre><code>pip install -r requirements.txt</code></pre>
            </li>
            <li>Set up the database:
                <pre><code>python manage.py makemigrations</code></pre>
                <pre><code>python manage.py migrate</code></pre>
            </li>
            <li>Create Super User(Admin):
                <pre><code>python manage.py createsuperuser</code></pre>
            </li>
            <li>Now run the Server:
                <pre><code>python manage.py runserver</code></pre>
            </li>
        </ol>
    </section>
  </body>
</html>


