from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('sign-up.html',\
                    title = "Sign up!")

@app.route('/', methods=['POST'])
def validate_user_information():
    name = request.form['username']
    password = request.form['password']
    ver_pass = request.form['verify-pass']
    email = request.form['email']

    name_err, pass_err, ver_pass_err, email_err = '', '', '', ''

    """ The user leaves any of the following fields empty: username, password, verify password."""
    if not name:
        name_err = '*Username required'
    if not password:
        if not ver_pass:
            ver_pass_err = "*Password required"
        pass_err = '*Password required'

    """ 
    The user's username or password is not valid -- for example, it contains a space character
    or it consists of less than 3 characters or more than 20 characters
    (e.g., a username or password of "me" would be invalid). 
    """
    name_len = len(name)
    pass_len = len(password)

    if less_than_3_or_greater_20(name_len):
        name_err = 'Username needs to be at least 3 characters long and less than 20'
        if name_len == 0:
            name_err = '*Username required'            
    
    if contains_character(name, " "):
        name_err = 'Username cannot have any spaces'

    if less_than_3_or_greater_20(pass_len):
        pass_err = 'Password needs to be at least 3 characters and less than 20'
        if pass_len == 0:
            pass_err = '*Password required'
    
    """ 
    The user's password and password-confirmation do not match.
    """

    if not (password == ver_pass):
        ver_pass_err = "*Passwords do not match"

    """
    The user provides an email, but it's not a valid email. Note: the email field may be left empty, 
    but if there is content in it, then it must be validated. The criteria for a valid email address
    in this assignment are that it has a single @, a single ., contains no spaces, and is between 3
    and 20 characters long.
    """

    email_len = len(email)
    if email:
        if less_than_3_or_greater_20(email_len):
            email_err = "Email needs to be at least 3 characters long and less than 20"
        if contains_character(email, " "):
            email_err = "Email cannot contain spaces"
        if not (contains_character(email, "@")) or not (contains_character(email, ".")):
            email_err = "Email missing the @ character or a . character"

    if not name_err and not pass_err and not ver_pass_err:
        if email_err:
                return render_template('sign-up.html', title='Sign up!', name = name, email = email, email_error = email_err)
        return render_template('sign-up-success.html', title="Account creation", name = name,\
                                password = password, email = email)

    return render_template('sign-up.html', title = "Sign up!",\
                            name = name, name_error = name_err,\
                            pass_error = pass_err, ver_pass_error = ver_pass_err,\
                            email_error = email_err, email = email)

def contains_character(name, character):
    return True if character in name else False

def less_than_3_or_greater_20(number):
    return True if number < 3 or number > 20 else False

app.run()