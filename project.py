from flask import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurant.html",rest = restaurants)
@app.route('/restaurant/<int:rest_id>/')
def restaurantMenu(rest_id):
    rest_name = session.query(Restaurant).filter_by(id = rest_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = rest_id)
    return render_template('menu.html',restaurant=rest_name,items=items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:rest_id>/json')
def restaurantMenuJson(rest_id):
    rest_name = session.query(Restaurant).filter_by(id = rest_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = rest_id)
    return jsonify(MenuItems = [i.serialize for i in items])
@app.route('/restaurant/<int:restaurant_id>/add_items/', methods = ['GET','POST'])
def newMenuItem(restaurant_id): 
    if request.method == 'POST':
        n = request.form['name']
        d = request.form['description']
        p = request.form['price']
        c = request.form['course']
        item = MenuItem( name = n ,description = d , price =p, course = c, restaurant_id = restaurant_id)
        session.add(item)
        session.commit()     
        return redirect(url_for('restaurantMenu', rest_id = restaurant_id))  
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('newmenuitem.html',restaurant = restaurant )

# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        print(restaurant_id)
        print(menu_id)
        items = session.query(MenuItem).filter_by( id = menu_id).one()
        return render_template('editmenuitem.html',rest_id = restaurant_id, item = items)
    else:
        item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id =menu_id ).one()
        item.name = request.form['name']
        session.add(item)
        session.commit()
        return redirect(url_for('restaurantMenu', rest_id = restaurant_id))

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        items = session.query(MenuItem).filter_by( id = menu_id).one()
        restaurant = session.query(Restaurant).filter_by( id = restaurant_id).one()
        return render_template('deleteitem.html', restaurant = restaurant , item = items)
    else:

        items = session.query(MenuItem).filter_by( id = menu_id).one()
        session.delete(items)
        session.commit()
        return redirect(url_for('restaurantMenu',rest_id = restaurant_id))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
