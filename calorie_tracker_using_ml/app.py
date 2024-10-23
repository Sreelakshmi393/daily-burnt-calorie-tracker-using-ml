from flask import Flask, render_template, request, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import date,time
import datetime
import pickle



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym_management.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'dailyburntcalorietracker'


class Member(db.Model):
    uname = db.Column(db.String(50), primary_key=True)  # Primary Key
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)  # Height in cm
    weight = db.Column(db.Integer, nullable=False)  # Weight in kg
    kind = db.Column(db.String(20), nullable=False)  # Could represent membership type or other info


#Define the Workouts model
class Workout(db.Model):
    workout_id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # Primary Key
    uname = db.Column(db.String(50), db.ForeignKey('member.uname'), nullable=False)  # Foreign Key referencing Members
    date = db.Column(db.Date, nullable=False, default=date.today)  # Date of the workout
    calorie = db.Column(db.Float, nullable=False)  # Calories burnt

class Workouts(db.Model):
    workout_id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # Primary Key
    uname = db.Column(db.String(50), db.ForeignKey('member.uname'), nullable=False)  # Foreign Key referencing Members
    date = db.Column(db.Date, nullable=False, default=date.today)  # Date of the workout
    calorie = db.Column(db.Integer, nullable=False)  # Calories burnt

class Remark(db.Model):
    remark_id = db.Column(db.Integer, primary_key=True)  # Primary Key
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.workout_id'), nullable=False)  # Foreign Key referencing Workouts
    uname = db.Column(db.String(50), db.ForeignKey('member.uname'), nullable=False)  # Foreign Key referencing Members
    feedback = db.Column(db.Text, nullable=False)  # Feedback text

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        password = request.form['password']
        user = Member.query.filter_by(uname=uname, password=password).first()

        if user:
            session['username'] = uname
            if user.kind == 'trainer':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('member_dashboard'))  # Redirect to member's dashboard
        else:
            return "Invalid credentials"
    
    return render_template('login.html')



# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        uname = request.form['username']
        password = request.form['password']
        name = request.form['name']
        gender = request.form['gender']
        age = int(request.form['age'])
        height = int(request.form['height'])
        weight = int(request.form['weight'])
        
        # Set kind to 'member'
        kind = 'member'
        
        # Create new member object
        new_member = Member(uname=uname, password=password, name=name, gender=gender, age=age, height=height, weight=weight, kind=kind)
        
        # Add to the database
        db.session.add(new_member)
        db.session.commit()

        return redirect(url_for('login'))  # Redirect to login page after successful registration
    
    return render_template('register.html')


# Admin Dashboard Route
@app.route('/admin')
def admin_dashboard():
    if 'username' in session and Member.query.filter_by(uname=session['username']).first().kind == 'trainer':
        return render_template('admin.html')  # Render the admin page
    else:
        return redirect(url_for('login'))

# Member Dashboard Route (Optional)
@app.route('/member')
def member_dashboard():
    if 'username' in session:
        return render_template('member_dashboard.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/calculate_calorie', methods=['GET', 'POST'])
def calculate_calorie():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Fetch user details from database based on session username
    user = db.session.query(Member).filter_by(uname=session['username']).first()
    
    if request.method == 'POST':
        # Collect the form data and pass it to your ML model here
        # ...
        return redirect(url_for('member_dashboard'))

    # Set the minimum date to today for the date input
    min_date = datetime.date.today().isoformat()  
    return render_template('calculate_calorie.html', user=user, min_date=min_date)




# Load the trained model
with open('calories-prediction-data/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Mapping for categorical input
gender_mapping = { 
    'male': 0,
    'female': 1
}

@app.route('/calculations')
def calculation():
    return render_template('calculate_calorie.html')


@app.route('/calculate', methods=['POST'])
def predict():
    
    # Get user input from the form
    gender_input = request.form['gender'].lower()
    age = int(request.form['age'])
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    duration = float(request.form['duration'])
    heart_rate = float(request.form['heart_rate'])
    temperature = float(request.form['body_temp'])
  

    # Convert categorical input to numerical
    if gender_input in gender_mapping:
        gender_numeric = gender_mapping[gender_input]
    else:
        return "Invalid input for gender."

    # Prepare input for the model (modify according to your model's input structure)
    model_input = [[gender_numeric, age, height, weight, duration, heart_rate, temperature]]  # If other features are needed, include them as well

    # Make prediction
    prediction = model.predict(model_input)
    rounded_prediction = round(prediction[0], 2)

    #  # Retrieve username from session and store the predicted calorie value in the workout table
    uname = session['username']
    workout_date = date.today()  # You can also use request.form['date'] if date is provided in the form

   
    new_workout = Workout(uname=uname, date=workout_date, calorie=rounded_prediction)
        
    # Add to the database
    db.session.add(new_workout)
    db.session.commit()

    # Return the prediction result
    # return f'The predicted output is: {prediction[0]}'
    return render_template('result.html', predicted_calories=rounded_prediction)

# @app.route('/view_performance')
# def view_performance():
#     # Fetch all unique usernames from the workouts table
#     users = db.session.query(Workout.uname).distinct().all()
#     users = [user[0] for user in users]  # Extract usernames from tuples

#     return render_template('view_performance.html', users=users)

@app.route('/view_performance', methods=['GET', 'POST'])
def view_performance():
    if request.method == 'POST':
        selected_user = request.form['uname']
        # Fetch workouts for the selected user
        workouts = Workout.query.filter_by(uname=selected_user).all()

        users = db.session.query(Workout.uname).distinct().all()
        users = [user[0] for user in users]  # Extract usernames from tuples

        return render_template('view_performance.html', users=users, workouts=workouts, selected_user=selected_user)

    # Initial GET request
    users = db.session.query(Workout.uname).distinct().all()
    users = [user[0] for user in users]  # Extract usernames from tuples

    return render_template('view_performance.html', users=users)

@app.route('/feedback/<int:workout_id>')
def feedback(workout_id):
    return render_template('feedback.html', workout_id=workout_id)

@app.route('/submit_feedback/<int:workout_id>', methods=['POST'])
def submit_feedback(workout_id):
    feedback = request.form['feedback']
    selected_user = request.form['uname']
    # You can store the feedback in the database (create a feedback model)
    new_feedback = Remark(workout_id=workout_id, uname=selected_user, feedback=feedback)
    db.session.add(new_feedback)
    db.session.commit()
    
    return redirect(url_for('view_performance'))


if __name__ == '__main__':
    app.run(debug=True)
