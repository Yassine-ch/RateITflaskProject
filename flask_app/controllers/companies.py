from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.company import Company
from flask_app.models.review import Review
from flask_app.models.adress import Adress

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/company/register', methods = ['post'])
def add_company():
    if not Company.validate(request.form):
        return redirect('/connection')
    adr = Adress.add_adress(request.form)

    data = {
            **request.form,
            'password':bcrypt.generate_password_hash(request.form['password']),
            'adress_id': adr
            }
    print(data,"*"*25)
    company = Company.add_company(data)
    if company:
        session['company_id'] = company
        return redirect('/dashboard')
    else:
        return redirect('/')
    

@app.route('/company/login', methods=['POST'])
def loginComp():
    company = Company.get_by_email(request.form)
    if not company:
        flash('Invalid email or password',"LoginComp")
        return redirect('/connection')
    if not bcrypt.check_password_hash(company.password, request.form['password']):
        flash('Invalid email or password',"LoginComp")
        return redirect('/connection')
    session['company_id']=company.id
    reviews = Review.get_company_reviews({'id': company.id})
    print(reviews,"-*-"*20)
    return redirect('/dashboard', reviews = reviews)


@app.route('/company/<int:id>')
def show_one(id):
    data = {
        'id':id
    }
    company = Company.get_by_id(data)
    general_rate = Review.get_company_avg(data)
    reviews = Review.get_company_reviews(data)
    return render_template("show_company.html", company=company, reviews=reviews, general_rate=general_rate)


@app.route('/admin/companies')
def see_all():
    companies = Company.get_all_with_sector()
    return render_template('show_companies.html', companies=companies)