from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from email.utils import formataddr


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False

app.config['MAIL_USERNAME'] = '247668.swastik@gmail.com'
app.config['MAIL_PASSWORD'] = 'gkcumndybwazevzi'
app.config['MAIL_DEFAULT_SENDER'] = '247668.swastik@gmail.com'

app.config['SECRET_KEY'] = '467d862ed9fcd13bbabe41f76946c9202418bc6566fc9631'

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("lllll")
        name = request.form.get('name')
        company = request.form.get('company')
        phone = request.form.get('phone')
        email = request.form.get('email')
        model = request.form.get('model')
        service = request.form.get('service')
        detail = request.form.get('detail')

        try:
            html = render_template(
                "emails/service_request.html",
                name = name,
                company = company,
                phone = phone,
                email = email,
                model = model,
                service = service,
                detail = detail
            )

            msg = Message(
                subject="🔧 New Service Request | Swastik Technology & Services",
                sender=formataddr(("Swastik Technology & Services", "247668.swastik@gmail.com")),
                recipients=[
                    formataddr(("Service Team", "info.swastik@gmail.com"))
                ],
                cc=[
                    formataddr(("Customer", email)),
                    formataddr(("Sales Team", "gauravdhiman1142@gmail.com"))
                ]
            )

            msg.html = html
            mail.send(msg)
            flash('Email Sent Successfully!')
            return redirect(url_for('index'))

            return "Email Sent Successfully!"
        except Exception as e:
            print(e)
            return render_template('index.html')
    else:
        return render_template('index.html')


# def appointment():
#     if request.method == 'POST':
#         print("data")
#         return render_template('index.html')
#     else:
#         return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)