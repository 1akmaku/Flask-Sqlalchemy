import flask
from flask import Flask,request,render_template,make_response,jsonify,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///myapp.sqllite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
ma=Marshmallow(app)

class Myapp(db.Model):
    order_id=db.Column(db.Integer,primary_key=True)
    size=db.Column(db.Float)
    toppings=db.Column(db.String(50))
    crust=db.Column(db.String(50))


class Myschema(ma.Schema):
    class Meta:
        fields=('order_id','size','toppings','crust')



schema_obj=Myschema(many=True)

@app.route('/')
def hello():
    return make_response(jsonify('Hello world'),200)



@app.route('/orders')
def get_order():
    queries=Myapp.query.all()
    result=schema_obj.dump(queries)
    return jsonify(result)


@app.route('/orders',methods=['POST'])
def post_order():
    req=request.get_json()
    order_id=req['order_id']
    size=req['size']
    toppings=req['toppings']
    crust=req['crust']
    new_entry=Myapp(order_id=order_id,size=size,toppings=toppings,crust=crust)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for("get_order"))




if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='0.0.0.0',port=5000)