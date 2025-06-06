from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os, env
from werkzeug.utils import secure_filename
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
# Set secret key for session management and flash messages
app.config['SECRET_KEY'] = env.SECRET_KEY
# Set folder for file uploads
app.config['UPLOAD_FOLDER'] = 'uploads'
# Set database URI for SQLAlchemy (SQLite database)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///requests.db')
# Set maximum upload size (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize SQLAlchemy with Flask app
db = SQLAlchemy(app)

# Database model for website requests
class WebsiteRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100))              # Name of requester
    email = db.Column(db.String(120))             # Email of requester
    request_type = db.Column(db.String(50))       # Type of request
    page = db.Column(db.String(100))              # Page related to request
    description = db.Column(db.Text)              # Description of request
    urgency = db.Column(db.String(20))            # Urgency level
    filename = db.Column(db.String(200))          # Uploaded file name
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)  # Submission timestamp
    completed = db.Column(db.Boolean, default=False)  # Add this line

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Route for displaying the request form
@app.route('/')
def form():
    return render_template('form.html')

# Route for handling form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    request_type = request.form['request_type']
    page = request.form['page']
    description = request.form['description']
    urgency = request.form['urgency']
    file = request.files['attachment']

    filename = None
    # If a file is uploaded, save it securely
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Create new WebsiteRequest object
    new_request = WebsiteRequest(
        name=name,
        email=email,
        request_type=request_type,
        page=page,
        description=description,
        urgency=urgency,
        filename=filename
    )
    # Add to database and commit
    db.session.add(new_request)
    db.session.commit()
    # Show success message
    flash('Request submitted successfully!')
    # Redirect back to form
    return redirect(url_for('form'))

# Route for viewing all submitted requests
@app.route('/requests')
def view_requests():
    # Query all requests, most recent first
    requests = WebsiteRequest.query.order_by(WebsiteRequest.submitted_at.desc()).all()
    return render_template('requests.html', requests=requests)

# Route for serving uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Admin route to list all requests
@app.route('/admin')
def list_requests():
    # Get filter values from query parameters
    status = request.args.get('status')
    urgency = request.args.get('urgency')
    date = request.args.get('date')

    # Start with all requests
    query = WebsiteRequest.query

    # Filter by status
    if status == 'pending':
        query = query.filter_by(completed=False)
    elif status == 'done':
        query = query.filter_by(completed=True)

    # Filter by urgency
    if urgency:
        query = query.filter_by(urgency=urgency)

    # Filter by date (submitted_at)
    if date:
        from datetime import datetime, timedelta
        start = datetime.strptime(date, "%Y-%m-%d")
        end = start + timedelta(days=1)
        query = query.filter(WebsiteRequest.submitted_at >= start, WebsiteRequest.submitted_at < end)

    # Order by most recent
    requests = query.order_by(WebsiteRequest.id.desc()).all()
    return render_template('admin.html', requests=requests)

# Route to toggle completion status
@app.route('/toggle/<int:request_id>')
def toggle_request(request_id):
    req = WebsiteRequest.query.get_or_404(request_id)
    req.completed = not req.completed
    db.session.commit()
    return redirect(url_for('list_requests'))

@app.route('/admin/<int:request_id>')
def request_details(request_id):
    req = WebsiteRequest.query.get_or_404(request_id)
    return render_template('details.html', req=req)

# Run the app
if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    # Start Flask development server
    app.run(debug=True)