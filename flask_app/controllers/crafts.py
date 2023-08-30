from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.craft import Craft
from flask_app.models.user import User


@app.route('/crafts')
def shows():
    all_crafts = Craft.get_all()
    data = {
        "id": session['user_id']
        #"progress_id": 
    }
    
    
    return render_template("dashboard.html", crafts = all_crafts, user = User.get_by_id(data)) # The "all_crafts" is the name to use in the jinja in the html
# Create new crafts should have a new craft function first before create button's function
@app.route('/crafts/new')
def new():
    print("Test")
    return render_template("new_craft.html")




# Now we can create it and show it in the table
@app.route('/crafts/create',methods=['POST'])
def create_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Craft.validate_deal(request.form):
        return redirect('/crafts/new')
    print(request.form)
    Craft.save(request.form)
    return redirect('/crafts')



#Edit an exisitng crafts
@app.route('/crafts/edit/<int:id>')
def edit(id):
    data ={ 
        "id":id
    }
    return render_template("edit_craft.html",deal=Craft.get_one(data))





@app.route('/crafts/update',methods=['POST'])
def update():
    showid = request.form['id']
    if 'user_id' not in session:
        return redirect('/logout')
    if not Craft.validate_deal(request.form):
        return redirect('/crafts/edit/' + showid)  # <int:id> is a specific input taking in a number, so it won't be valid to be put here (use string concatenation instead)
    
    print(showid)
    Craft.update(request.form)
    return redirect('/crafts')




# Show details for a craft
@app.route('/crafts/show/<int:id>')
def show_show(id):
    data = {
        "id": id
    }
    postedby = Craft.get_postebyid(data) #Call on the value of the query (nested) to print and show in the details.  The variable declared is all that is going to be called in the Jinja.
    print("D"*50)
    print(postedby)
    return render_template('show_craft.html', deal=Craft.get_one(data), postedby=postedby)


@app.route('/crafts/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Craft.destroy(data)
    return redirect('/crafts')


 



if __name__=="__main__":
    app.run(debug=True)