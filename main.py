from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this for production!

# Database initialization
def get_db_connection():
    conn = sqlite3.connect('models.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 login_count INTEGER DEFAULT 0)''')
    
    # Create subscriptions table
    c.execute('''CREATE TABLE IF NOT EXISTS subscriptions
                 (user_id INTEGER,
                  model_id TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id),
                  UNIQUE(user_id, model_id))''')
    
    # Create models table
    c.execute('''CREATE TABLE IF NOT EXISTS models
                 (id TEXT PRIMARY KEY,
                  category TEXT NOT NULL,
                  name TEXT NOT NULL,
                  render_url TEXT NOT NULL,
                  description TEXT)''')
    
    # Insert sample models if they don't exist
    sample_models = [
        ('healthcare_eye', 'healthcare', 'Eye Disease Detection', 
         'https://your-eye-model.onrender.com', 'Detects common eye diseases from retinal images'),
        ('healthcare_heart', 'healthcare', 'Heart Disease Prediction',
         'https://your-heart-model.onrender.com', 'Predicts risk of heart disease'),
        ('pollution_air', 'pollution', 'Air Quality Prediction',
         'https://your-air-model.onrender.com', 'Forecasts air quality index'),
        ('agriculture_crop', 'agriculture', 'Crop Yield Prediction',
         'https://crop-recommendation-ck2c.onrender.com/', 'Predicts crop yields')
    ]
    
    c.executemany('''INSERT OR IGNORE INTO models (id, category, name, render_url, description)
                     VALUES (?, ?, ?, ?, ?)''', sample_models)
    
    conn.commit()
    conn.close()

init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            # Check if user has any subscriptions
            conn = get_db_connection()
            subscription_count = conn.execute(
                'SELECT COUNT(*) FROM subscriptions WHERE user_id = ?', 
                (user['id'],)
            ).fetchone()[0]
            conn.close()
            
            if user['login_count'] >= 3 and subscription_count == 0:
                flash('Login limit reached. Please subscribe to a model for unlimited access.', 'warning')
                return redirect(url_for('login'))
            
            # Update login count
            conn = get_db_connection()
            conn.execute(
                'UPDATE users SET login_count = login_count + 1 WHERE id = ?', 
                (user['id'],)
            )
            conn.commit()
            conn.close()
            
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not password or not confirm_password:
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed_password)
            )
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'danger')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
        finally:
            if 'conn' in locals():
                conn.close()
    
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    categories = conn.execute(
        'SELECT DISTINCT category FROM models ORDER BY category'
    ).fetchall()
    conn.close()
    return render_template('dashboard.html', categories=categories)

@app.route('/category/<category_name>')
@login_required
def category(category_name):
    conn = get_db_connection()
    models = conn.execute(
        'SELECT * FROM models WHERE category = ?', 
        (category_name,)
    ).fetchall()
    conn.close()
    
    if not models:
        flash('Category not found', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('category.html', 
                         category_name=category_name,
                         models=models)

@app.route('/model/<model_id>')
@login_required
def model(model_id):
    conn = get_db_connection()
    model = conn.execute(
        'SELECT * FROM models WHERE id = ?', 
        (model_id,)
    ).fetchone()
    conn.close()
    
    if not model:
        flash('Model not found', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check if user has subscription
    conn = get_db_connection()
    has_subscription = conn.execute(
        'SELECT 1 FROM subscriptions WHERE user_id = ? AND model_id = ?',
        (session['user_id'], model_id)
    ).fetchone() is not None
    
    # Get login count
    login_count = conn.execute(
        'SELECT login_count FROM users WHERE id = ?', 
        (session['user_id'],)
    ).fetchone()['login_count']
    conn.close()
    
    return render_template('model.html', 
                         model=model,
                         has_subscription=has_subscription,
                         login_count=login_count)

@app.route('/run-model/<model_id>')
@login_required
def run_model(model_id):
    # Check subscription status
    conn = get_db_connection()
    has_subscription = conn.execute(
        'SELECT 1 FROM subscriptions WHERE user_id = ? AND model_id = ?',
        (session['user_id'], model_id)
    ).fetchone() is not None
    
    if not has_subscription:
        # Check login count
        login_count = conn.execute(
            'SELECT login_count FROM users WHERE id = ?', 
            (session['user_id'],)
        ).fetchone()['login_count']
        
        if login_count > 3:
            conn.close()
            flash('You have reached your free usage limit. Please subscribe to continue using this model.', 'warning')
            return redirect(url_for('model', model_id=model_id))
    
    model = conn.execute(
        'SELECT render_url FROM models WHERE id = ?', 
        (model_id,)
    ).fetchone()
    conn.close()
    
    if not model:
        flash('Model not found', 'danger')
        return redirect(url_for('dashboard'))
    
    return redirect(model['render_url'])

@app.route('/subscribe/<model_id>', methods=['POST'])
@login_required
def subscribe(model_id):
    try:
        conn = get_db_connection()
        # Verify model exists
        model_exists = conn.execute(
            'SELECT 1 FROM models WHERE id = ?', 
            (model_id,)
        ).fetchone() is not None
        
        if not model_exists:
            flash('Model not found', 'danger')
            return redirect(url_for('dashboard'))
        
        # Add subscription
        conn.execute(
            'INSERT OR IGNORE INTO subscriptions (user_id, model_id) VALUES (?, ?)', 
            (session['user_id'], model_id)
        )
        conn.commit()
        flash('Subscription successful! You now have unlimited access to this model.', 'success')
    except sqlite3.Error as e:
        flash('Error processing subscription', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('model', model_id=model_id))

@app.route('/model-info/<model_id>')
@login_required
def model_info(model_id):
    conn = get_db_connection()
    model = conn.execute(
        'SELECT * FROM models WHERE id = ?', 
        (model_id,)
    ).fetchone()
    conn.close()

    if not model:
        flash('Model not found', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('model_info.html', model=model)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)