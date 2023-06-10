from flask_app import app
from flask import render_template,request, redirect, session,flash
from flask_app.models.review import Review
from flask_app.models.company import Company


@app.route('/reviews/new')
def new_review():
    companies = Company.get_all()
    return render_template("new_review.html", companies = companies)

@app.route('/review/create', methods=["post"])
def add_review():
    data = {
            **request.form,
            "user_id" : session["user_id"]
        }
    print(data)
    Review.add_review(data)
    return redirect('/dashboard')

@app.route('/admin/reviews')
def see_all_reviews():
    reviews = Review.get_all()
    return render_template("show_reviews.html")