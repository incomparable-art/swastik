from swastikapp import *


def index():
    if request.method == 'POST':
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
            service_team = os.getenv("SERVICE_TEAM")
            sales_team = os.getenv("SALES_TEAM")

            msg = Message(
                subject="🔧 New Service Request | Swastik Technology & Services",
                sender=formataddr(("Swastik Technology & Services", "247668.swastik@gmail.com")),
                recipients=[
                    formataddr(("Service Team", service_team))
                ],
                cc=[
                    formataddr(("Customer", email)),
                    formataddr(("Sales Team", sales_team))
                ]
            )

            msg.html = html
            mail.send(msg)
            flash('Email Sent Successfully!')
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            return render_template('index.html')
    else:
        return render_template('index.html')
