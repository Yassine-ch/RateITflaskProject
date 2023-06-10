from flask_app import app
from flask import render_template,request, redirect, session,flash
from flask_app.models.review import Review
from flask_app.models.company import Company
from flask_app.models.sector import Sector




@app.route('/admin/sector/new')
def new():
    return render_template("new_sector.html")


@app.route('/admin/sector/create', methods=["post"])
def create():
    Sector.add_sector(request.form)
    return redirect('/admin/sectors')

@app.route('/admin/sectors')
def show_all_sectors():
    sectors = Sector.get_all()
    return render_template('show_sectors.html', sectors = sectors)

@app.route('/admin/sector/<int:sector_id>/edit')
def edit(sector_id):
    sector= Sector.get_by_id({'id': sector_id})
    return render_template('edit_sector.html',sector=sector)

@app.route('/admin/sector/<int:sector_id>/update', methods=['post'])
def update(sector_id):
    data =  {
        **request.form,
        "id" : sector_id
    }
    Sector.edit_sector(data)
    return redirect('/admin/sectors')

@app.route('/admin/sector/<int:sector_id>/delete')
def delete(sector_id):
   data =  {
        **request.form,
        "id" : sector_id
    }
   Sector.delete_sector({'id':sector_id})
   return redirect('/admin/sectors')
