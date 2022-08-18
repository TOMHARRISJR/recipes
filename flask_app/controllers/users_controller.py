from flask_app import app
from flask import flash ,render_template, request, redirect ,session
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )


# created home page
@app.route('/')
def display_login():
    return render_template('login.html')

# action method to process and validate user info
@app.route('/user/registration', methods = ['POST'])
def process_registration():
    # validate registration form
    if not User.validate_registration( request.form ):
        return redirect('/')
    # validate if the user already exists
    user_exists = User.get_one_to_validate_email(request.form)
    if user_exists != None:
        flash('This email already exists',"error_registration_email")
        return redirect('/')
    #proceed to create the user
    data = {
        **request.form,
        "password": bcrypt.generate_password_hash( request.form["password"])

    }
    print( data )
    user_id = User.create( data )

    session['first_name'] = data['first_name']
    session['email'] = data['email']
    session['user_id'] = user_id 

    return redirect('/recipes')

@app.route('/user/login',methods = ['POST'])
def process_login():
    user = User.get_one_to_validate_email( request.form )
    if user != None:
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Wrong credantials', 'error_login_credentials')
            return redirect('/')
        
        session['first_name'] = user.first_name
        session['email'] = user.email
        session['user_id'] = user.id 

        return redirect('/recipes')
    else:
        flash('Wrong credantials', 'error_login_credentials')
        return redirect('/')

@app.route('/user/logout')
def process_logout():
    session.clear()
    return redirect('/')
    





