from flask import Flask, jsonify, request, render_template, session, redirect, url_for, flash
from backend.models import init_db, insert_incident, get_incidents_recent
from backend.algorithms import Graph, dijkstra
from backend.config import GOOGLE_MAPS_API_KEY
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session security
CORS(app)
init_db()

# -----------------------
# AUTHENTICATION
# -----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Muneeb Farid' and password == 'CR380':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Try: admin / traffic2024', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# -----------------------
# FRONTEND ROUTES
# -----------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', api_key=GOOGLE_MAPS_API_KEY)

@app.route('/route-planner')
@login_required
def route_planner():
    return render_template('route-planner.html')

@app.route('/report')
@login_required
def report():
    return render_template('report.html')

@app.route('/about')
def about():
    return render_template('about.html')

# -----------------------
# API ENDPOINTS (Your existing code)
# -----------------------
@app.route('/api/health')
def health():
    return jsonify({"status": "TrafficFlow Pro API is LIVE", "developer": "Muneeb Farid"})

@app.route('/api/incidents', methods=['GET'])
def list_incidents():
    rows = get_incidents_recent()
    result = []
    for r in rows:
        result.append({
            'id': r.get('id'),
            'lat': float(r.get('lat')),
            'lng': float(r.get('lng')),
            'severity': r.get('severity'),
            'description': r.get('description'),
            'timestamp': r.get('timestamp')
        })
    return jsonify(result)

@app.route('/api/incidents', methods=['POST'])
def post_incident():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    severity = data.get('severity', 1)
    description = data.get('description')
    if lat is None or lng is None:
        return jsonify({'error': 'lat and lng required'}), 400
    id = insert_incident(lat, lng, severity, description)
    return jsonify({'status': 'ok', 'id': id})

@app.route('/api/route', methods=['POST'])
def compute_route():
    data = request.json
    source = data.get('source')
    target = data.get('target')
    if not source or not target:
        return jsonify({'error': 'source and target required'}), 400
    g = Graph()
    g.add_edge('A', 'B', 5)
    g.add_edge('B', 'C', 2)
    g.add_edge('A', 'C', 10)
    dist, _ = dijkstra(g, source)
    return jsonify({'distance': dist.get(target, "No route found")})

# At the VERY BOTTOM of app.py
if __name__ == '__main__':
    try:
        print("Initializing database...")
        init_db()
        print("Starting Flask app on http://127.0.0.1:5000")
        app.run(host='127.0.0.1', port=5000, debug=True)
    except Exception as e:
        print("❌ FATAL ERROR:", str(e))
        import traceback
        traceback.print_exc()