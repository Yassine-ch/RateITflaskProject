from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.company import Company
from flask_app.models.review import Review
from flask_app.models.adress import Adress
from flask_app.models.company import Company
from flask_app.models.sector import Sector

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/company/dashboard')
def dashboard_company():
    if 'company_id' in session:
        company= Company.get_by_id({'id': session['user_id']})
        reviews = Review.get_company_reviews({'id': session['user_id']})
        return render_template('company/company_dashboard.html', company=company, reviews=reviews)
    else:
        return redirect('/connection')

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
        return redirect('/company/dashboard')
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
    # eli fsa5ha dali
    reviews = Review.get_company_reviews({'id': company.id})
    print(reviews,"-*-"*20)
    # 
    return redirect('/company/dashboard')


@app.route('/company/<int:id>')
def show_one(id):
    data = {
        'id':id
    }
    company = Company.get_by_id(data)
    general_rate = Review.get_company_avg(data)
    reviews = Review.get_company_reviews(data)
    return render_template("company/show_company.html", company=company, reviews=reviews, general_rate=general_rate)

@app.route('/edit/company/<int:company_id>')
def edit_comp(company_id):
    data = {
        'id': company_id
    }
    company = Company.get_by_id(data)
    sectors = Sector.get_all()
    return render_template("company/edit_company.html", company=company, sectors=sectors)

@app.route('/admin/companies')
def see_all():
    companies = Company.get_all()
    return render_template('admin/companies/show_companies.html', companies=companies)

@app.route('/admin/company/<int:company_id>/update')
def admin_updating_company(company_id):
    if request.form['newpsw'] == request.form['confnewpsw']:
        data = {
            **request.form,
            'id': company_id,
            'password':bcrypt.generate_password_hash(request.form['newpsw'])
        }
        Company.edit_company(data)
        return redirect('/admin/companies')
    else:
        flash("Your are not sure about your password?!")
        return redirect(f'/admin/company/{company_id}/edit')



@app.route('/admin/company/<int:company_id>/edit')
def edit_company_admin(company_id):
    company= Company.get_by_id({'id': company_id})
    sectors = Sector.get_all()
    return render_template('admin/companies/edit_company.html',company=company ,sectors=sectors)

@app.route('/admin/company/<int:company_id>/update', methods=['post'])
def admin_update_company(company_id):
    data =  {
        **request.form,
        "id" : company_id
    }
    Company.edit_company(data)
    return redirect('/admin/companies')
