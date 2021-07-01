from flask_app import app
from flask import render_template, request, session, redirect
from flask_app.models.band import Band
from flask_app.models.user import User


@app.route('/create_page')
def new_band_page():
    if "user_id" not in session:
        return redirect('/')
    return render_template('band_new.html')


@app.route('/create/process',methods=['POST'])
def insert_band():
    if not User.validate_create(request.form):
        return redirect('/create_page')
    data = {
        "name":request.form['name'],
        "genre":request.form['genre'],
        "home_city":request.form['home_city'],
        "user_id":session['user_id']
    }
    Band.insert_band(data)

    return redirect('/dashboard')


@app.route('/edit/<int:id>')
def update_band_page(id):
    if "user_id" not in session:
        return redirect('/')
    band = Band.get_one_by_id({"id":id})
    return render_template('band_edit.html',band=band)


@app.route('/update/process',methods=['POST'])
def update_band():

    if not User.validate_create(request.form):
        return redirect(f"/edit/{request.form['id']}")
    data = {
        "name":request.form['name'],
        "genre":request.form['genre'],
        "home_city":request.form['home_city'],
        "id":request.form['id']
    }
    Band.update_band(data)
    return redirect('/dashboard')


@app.route('/bands/<int:id>')
def view_band(id):
    if "user_id" not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    bands = Band.get_one_by_id({"id":id})
    return render_template('band_page.html',user=user,bands=bands)


# Possibly the app route for JOINING a band or creating a band
# change purchase in app route
@app.route('/member/<int:id>') #id here is the id of the band
def join(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "user_id":session['user_id'],
        "band_id":id
    }
    User.join(data)
    return redirect('/dashboard')






# quit should run redirect to user page
@app.route('/quit/<int:id>')
def quit(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "user_id":session['user_id'],
        "band_id":id
    }
    Band.quit(data)
    return redirect(f"/user/{session['user_id']}")




@app.route('/delete/<int:id>')
def delete(id):
    if "user_id" not in session:
        return redirect('/')
    Band.delete({"id":id})
    return redirect('/dashboard')