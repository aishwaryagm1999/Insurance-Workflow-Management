from flask import Flask, render_template, request, redirect, session,flash
from flask_sqlalchemy import SQLAlchemy
import json
import qrcode
import os
import datetime
from werkzeug.utils import secure_filename
from flask_migrate import Migrate


POLICIES_FILE = 'policies.json'  
from sqlalchemy.exc import IntegrityError


from twilio.rest import Client

# Twilio account SID and auth token masked (replace with token from twilio)
TWILIO_ACCOUNT_SID = '************************'
TWILIO_AUTH_TOKEN = '*************************'
TWILIO_PHONE_NUMBER = '+10000000000' #twilio number (replace)
TWILIO_TARGET_NUMBER = '+910000000000'  # Number to send messages (replace)


app = Flask(__name__) # Feature -> Inheritance (Creating a Flask instance which is a WSGI application)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # Feature -> Dictionary (Storing configuration settings)
app.config['SECRET_KEY'] = 'secret123abcd4567qwerty'

db = SQLAlchemy(app) # Feature -> Inheritance (Creating a SQLAlchemy instance for ORM)
migrate = Migrate(app, db) # Feature -> Inheritance (Setting up migrations)
class User(db.Model): # Feature -> Inheritance (Defining a model by inheriting db.Model)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(15), nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_photo = db.Column(db.String(150))  
@app.route('/') # Feature -> Decorators (Defining route for the application)
def home():
    user_info = get_user_info()
    return render_template('index.html', user_info=user_info)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    phone = request.form['phone']
    email = request.form['email']

   
    new_user = User(name=name, username=username, password=password, phone=phone, email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Success ! Account created!', 'success')
        return redirect('/')
    except IntegrityError as e:  # Feature -> Exception handling (Handling database integrity errors)
        db.session.rollback()
        flash('Username already exists. Please choose another username.', 'error')
        return redirect('/signup')
import json
from uuid import uuid4

def add_policy_ids():
    
    try:
        with open(POLICIES_FILE, 'r') as file:
            policies = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error reading policies file.")
        return

    
    for policy in policies:
        policy['policy_id'] = str(uuid4())  

    
    try:
        with open(POLICIES_FILE, 'w') as file:
            json.dump(policies, file, indent=4)  
    except Exception as e:
        print(f"Error writing to policy file try again: {e}")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id  # Feature -> Storing user information in session

            session['user_name'] = user.name
            return redirect('/')
        else:
            return 'Login Failed - Error'
    return render_template('login.html')



def get_user_info():
    user_info = {}
    if 'user_id' in session:
        user_info['name'] = session.get('user_name', '')
    return user_info

def setup_database(app):
    with app.app_context():
        db.create_all()
@app.route('/info')
def info_centre():
    return render_template('info_centre.html')
@app.context_processor
def inject_user_info():
    return dict(user_info=get_user_info())

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback = request.form['feedback']
    with open('feedback.txt', 'a') as file:
        file.write(feedback + "\n")
    return redirect('/support')
@app.route('/policies', methods=['GET', 'POST'])
def policies():
    update_all_expiry_dates()
    user_info = get_user_info()
    if 'user_id' not in user_info:
        return redirect('/login')

    user_policies = get_user_policies(user_info['user_id'])
    return render_template('policies.html', user_policies=user_policies)

def get_user_policies(user_id):
   
    try:
        with open(POLICIES_FILE, 'r') as file:
            all_policies = json.load(file)
        return [policy for policy in all_policies if policy.get('user_id') == user_id]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@app.route('/register_policy')
def register_policy():
    user_info = get_user_info()
    if 'user_id' not in user_info:
        return redirect('/login')

    policy_type = request.args.get('policy', 'default')
    return render_template(f'{policy_type}_form.html', user_info=user_info)



@app.route('/submit_policy', methods=['POST'])
def submit_policy():
    user_info = get_user_info()
    if 'user_id' not in user_info:
        return redirect('/login')

    
    policy_data = request.form.to_dict()
    policy_data['user_id'] = user_info['user_id']
    policy_type = policy_data['policy_type']

   
    current_date = datetime.now()
    expiry_date = current_date + timedelta(days=90)
    policy_data['expiry_date'] = expiry_date.strftime("%Y-%m-%d")

    
    qr_data = json.dumps(policy_data)
    qr_directory = os.path.join('static', 'qr_codes')
    os.makedirs(qr_directory, exist_ok=True)
    qr_code_path = os.path.join(qr_directory, f"{user_info['user_id']}_{policy_type}.png")
    
    qr = qrcode.make(qr_data)
    qr.save(qr_code_path)
    policy_data['qr_code_path'] = qr_code_path.replace('\\', '/')

    
    save_policy_data(user_info['user_id'], policy_data, policy_type)

   
   
    user = User.query.get(user_info['user_id'])
    if user and user.phone:
        send_sms(user.phone, f"Your {policy_data['policy_type']} policy has been successfully created.")
    
    if 'expiry_date' in policy_data:
        send_sms(TWILIO_TARGET_NUMBER, f"New policy created: {policy_data['policy_type']} with expiry on {policy_data['expiry_date']}")
    else:
        print("Error: expiry_date not found in policy_data")

    return redirect('/confirmation')

@app.route('/confirmation')
def confirmation():
    return "Policy Submitted Successfully!"

def get_user_info():
    user_info = {}
    if 'user_id' in session:
        user_info['user_id'] = session['user_id']
        user_info['name'] = session.get('user_name', '')
    return user_info
def send_sms(to_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"Message sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

  
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=TWILIO_TARGET_NUMBER
        )
    except Exception as e:
        print(f"Failed to send SMS: {e}")



def save_policy_data(user_id, policy_data, policy_type):
    
    try:
        with open(POLICIES_FILE, 'r') as file:
            policies = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        policies = []

    
    policy_data['user_id'] = user_id
    policy_data['policy_type'] = policy_type
    policies.append(policy_data)
    
    qr_data = json.dumps(policy_data)
    qr_directory = os.path.join('static', 'qr_codes')
    os.makedirs(qr_directory, exist_ok=True)

    qr_code_filename = f"{user_id}_{policy_type}.png"
    qr_code_path = os.path.join(qr_directory, qr_code_filename)

 
    qr = qrcode.make(qr_data)
    qr.save(qr_code_path)

 
    web_friendly_qr_code_path = qr_code_path.replace('\\', '/').lstrip('/').replace('static/', '')
    print("Simplified Web Friendly Path:", web_friendly_qr_code_path)



    
    policy_data['qr_code_path'] = web_friendly_qr_code_path

    with open(POLICIES_FILE, 'w') as file:
        json.dump(policies, file)
    user = User.query.get(user_id)
    if user and user.phone:
        send_sms(user.phone, f"Your {policy_type} policy has been successfully created.")
    else:
        print("SMS not sent: User or user's phone number not found.")
    add_policy_ids()

def setup_database(app):
    with app.app_context():
        db.create_all()


@app.route('/policy_registration')
def policy_registration():
    return render_template('policy_registration.html')

@app.route('/submit_claim', methods=['POST'])
def submit_claim():
    user_info = get_user_info()
    if 'user_id' not in user_info:
        return redirect('/login')

    
    policy_type = request.form.get('policy_type')
    claim_amount = float(request.form['claim_amount'])

    update_policy_after_claim(user_id=user_info['user_id'], policy_type=policy_type, claim_amount=claim_amount)
    send_sms(TWILIO_TARGET_NUMBER, f"Claim made on policy {policy_type} for amount {claim_amount}")

    return redirect('/policies')

def update_policy_after_claim(user_id, policy_type, claim_amount):
    try:
        with open(POLICIES_FILE, 'r') as file:
            policies = json.load(file)

        for policy in policies:
            if policy['user_id'] == user_id and policy['policy_type'] == policy_type:
                policy['insurance_amount'] = max(0, float(policy['insurance_amount']) - claim_amount)
                if 'claims' not in policy:
                    policy['claims'] = []
                policy['claims'].append(claim_amount)
                break

        with open(POLICIES_FILE, 'w') as file:
            json.dump(policies, file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

@app.route('/logout')
def logout():
    
    session.pop('user_id', None)
    session.pop('user_name', None)
    
    return redirect('/')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/update_expiry', methods=['POST'])
def update_expiry():
    policy_id = request.form.get('policy_id')
    new_expiry_date = request.form.get('new_expiry_date')

    try:
        with open(POLICIES_FILE, 'r+') as file:
            try:
                policies = json.load(file)
            except json.JSONDecodeError:
                print("JSON file is empty/invalid.")
                return "Error reading the policy file. Please check the server logs and resolve the issue."

            
            updated = False
            for policy in policies:
                if policy.get('policy_id') == policy_id:
                    policy['expiry_date'] = new_expiry_date
                    updated = True
                    break

            if not updated:
                print(f"No policy found with given ID: {policy_id}")
                return f"No policy found with given ID: {policy_id}"

            
            file.seek(0)
            json.dump(policies, file)
            file.truncate()

    except FileNotFoundError:
        print("The policies file doesn't exist.")
        return "Policies file not found...."

    return "Policy updated successfully!"


from datetime import datetime, timedelta

def update_all_expiry_dates():
    with open(POLICIES_FILE, 'r+') as file:
        policies = json.load(file)
        current_date = datetime.now().date()
        for policy in policies:
            
            if 'expiry_date' in policy:
                expiry_date = datetime.strptime(policy['expiry_date'], "%Y-%m-%d").date()
                if expiry_date > current_date:
                    policy['expiry_date'] = (expiry_date - timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                
                default_expiry = current_date + timedelta(days=90)
                policy['expiry_date'] = default_expiry.strftime("%Y-%m-%d")
                
        file.seek(0)
        json.dump(policies, file)
        file.truncate()

def check_and_notify_expiry():
    with open(POLICIES_FILE, 'r') as file:
        policies = json.load(file)
        current_date = datetime.now().date()
        for policy in policies:
            if 'expiry_date' in policy:
                expiry_date = datetime.strptime(policy['expiry_date'], "%Y-%m-%d").date()
                if expiry_date == current_date:
                    send_sms(TWILIO_TARGET_NUMBER, f"Policy {policy['policy_type']} is expiring today!")



from pathlib import Path

UPLOAD_FOLDER = 'static/profilepics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_URL'] = '/static'
@app.route('/profile_page')
def profile_page():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    return render_template('profile_page.html', user=user)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    if 'photo' in request.files:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Feature -> Securing filename to prevent path traversal attacks using Regular Expression
            print(filename)
            file_path = Path(app.config['UPLOAD_FOLDER']) / filename
            file.save(file_path)
            user.profile_photo = filename  
            db.session.commit()



    return redirect('/profile_page')




if __name__ == '__main__':
    check_and_notify_expiry()  
    
    setup_database(app)
    app.run(debug=True)

