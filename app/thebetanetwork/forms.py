from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, validators, ValidationError, PasswordField
import M2Crypto
import string

class LeadForm(Form):
    firstname    = TextField("First Name", [validators.Required("Please enter your first name.")])
    lastname     = TextField("Last Name", [validators.Required("Please enter your last name.")])
    email        = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your correct email address.")])
    submit       = SubmitField("Submit")


class SignupForm(Form):
    firstname = TextField("First name", [validators.Required("Please enter your first name.")])
    lastname  = TextField("Last name", [validators.Required("Please enter your last name.")])
    email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True

    def random_password(length=10):
        chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
        password = ''
        for i in range(length):
            password += chars[ord(M2Crypto.m2.rand_bytes(1)) % len(chars)]
        return password


class SigninForm(Form):
    email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter your password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False
