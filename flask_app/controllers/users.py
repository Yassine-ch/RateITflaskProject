from flask_app import app
from flask_app import TODAY
from flask import render_template,request, redirect, session,flash
from flask_app.models.user import User
from flask_app.models.review import Review
from flask_app.models.company import Company
from flask_app.models.sector import Sector

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Home page
@app.route('/')
def index():
    sectors = Sector.get_all()
    companies = Company.get_all()
    return render_template('index.html', sectors=sectors, companies=companies)

# LogReg
@app.route('/connection')
def logreg():
    sectors = Sector.get_all()
    return render_template("login.html", sectors = sectors)


@app.route('/company/dashboard')
def companydashboard():
    if 'company_id' in session:
        company= Company.get_by_id({'id': session['company_id']})
        reviews = Review.get_company_reviews({'id': session['company_id']})
        return render_template('company/company_dashboard.html', company=company, reviews= reviews)
    else:
        redirect('/connection')


@app.route('/user/dashboard')
def userdashboard():
    if 'user_id' in session:
        user= User.get_by_id({'id': session['user_id']})
        reviews = Review.get_by_user_id({'id': session['user_id']})
        return render_template('user/user_dashboard.html', user=user, reviews=reviews)
    else:
        return redirect('/connection')
    

@app.route('/admin/dashboard')
def admindashboard():
    if 'user_id' not in session:
        return redirect('/')
    user= User.get_by_id({'id': session['user_id']})
    if user.is_admin == 0:
        return redirect('/user/dashboard')
    cr = Review.count()
    cu = User.count()
    cc = Company.count()
    cs = Sector.count()
    return render_template('admin/admin_dashboard.html', user=user, cr=cr,cu=cu,cc=cc,cs=cs, date=TODAY)


@app.route('/user/register', methods=['post'])
def register():
    if not User.validate(request.form):
        return redirect('/connection')
    data={
        **request.form,
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
    user = User.create_user(data)
    session['user_id'] = user
    return redirect('/user/dashboard')

@app.route('/user/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password',"Login")
        return redirect('/connection')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password',"Login")
        return redirect('/connection')
    session['user_id']=user.id
    if user.is_admin == 1:
        return redirect('/admin/dashboard')
    else:
        return redirect('/user/dashboard')
    
@app.route('/edit_profil/<int:user_id>')
def edit_profil(user_id):
    data = {
        'id':user_id
    }
    user = User.get_by_id(data)
    return render_template("user/edit_user_profil.html", user = user)

@app.route('/user/<int:user_id>/update', methods=["post"])
def update_user(user_id):
    print(request.form,'*/*'*20)
    # if not User.validate(request.form):
    #     return redirect(f'/edit_profil/{user_id}')
    if request.form['newpsw'] == request.form['confnewpsw']:
        data = {
            **request.form,
            'id': user_id,
            'password':bcrypt.generate_password_hash(request.form['newpsw'])
        }
        User.update_user(data)
        return redirect('/user/dashboard')
    else:
        flash("Your are not sure about your password?!")
        return redirect(f'/edit_profil/{user_id}')

@app.route('/admin/users')
def see_all_users():
    users = User.get_all()
    return render_template('/admin/users/show_users.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')