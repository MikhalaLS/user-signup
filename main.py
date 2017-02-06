import webapp2
import re
import cgi




def build_page(error_username, error_password, error_verify, error_email, u, p, v, e):
    header = "<h2>Signup</h2>"

    username_label = "<label>Username:</label>"
    password_label = "<label>Password:</label>"
    verifypassword_label = "<label>Verify Password:</label>"
    email_label = "<label>Email (Optional):</label>"

    input_username = '<input type = "text" name = "username" value= ' + u + '>'
    input_password = '<input type = "password" name = "password" value= ' + p + '>'
    input_verify = '<input type = "password" name = "verify" value = ' + v +'>'
    input_email = '<input type = "text" name = "email" value = ' + e + '>'


    submit = "<input type ='submit' />"

    form = ("<form method='post'>" + header + "<br>" +
            username_label + input_username + error_username + "<br>" +
            password_label + input_password + error_password + "<br>" +
            verifypassword_label + input_verify + error_verify + "<br>" +
            email_label + input_email + error_email + "<br>" + "<br>" +
            submit + '</form>')

    return form


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)



class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = build_page("", "", "", "", "", "", "", "")
        self.response.write(content)

    def post(self):
        username = self.request.get("username")
        username = cgi.escape(username)
        password = self.request.get("password")
        password = cgi.escape(password)
        verify = self.request.get("verify")
        verify = cgi.escape(verify)
        email = self.request.get("email")
        email = cgi.escape(email)


        if valid_username(username) and valid_password(password) and verify == password and (valid_email(email) or email == ""):
            content = "<h2> Welcome " + username + "</h2>"
        else:
            error_username = ""
            error_password = ""
            error_verify = ""
            error_email = ""

            if not valid_username(username):
                error_username = " Username is not valid."
                username = ""

            if not valid_password(password):
                error_password = " Password is not valid."
                password = ""

            if password != verify:
                error_verify = " Passwords do not match."
                verify = ""

            if email != "" and not valid_email(email) :
                error_email = " Email is not valid."
                email = ""

            content = build_page(error_username, error_password, error_verify, error_email, username, password, verify, email)

        self.response.write(content)






app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
