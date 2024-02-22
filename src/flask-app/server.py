from flask import Flask,request,render_template,jsonify,make_response

app=Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

#
# @app.route('/get_orders',method=['GET'])
# def orders():
#     return render_template('index.html')



@app.route('/real')
def query_params():
    if request.args:
        req=request.args
        return "".join(f"{k},{v}" for k,v in req.items())
    return "No query passed"


order={
    "order1":{
        "Size":"Small",
        "Toppings":"Bacon",
        "Crust":"Thin"
    },
    "order2":{
        "Size":"Small",
        "Toppings":"Bacon",
        "Crust":"Thin"
    },

    "order3":{
        "Size":"Small",
        "Toppings":"Bacon",
        "Crust":"Thin"
    }
}

@app.route('/orders')
def get_order():
    return make_response(jsonify(order),200)

@app.route('/orders/<id>')
def get_neworder_byid(id):
    if id in order:
        return make_response(jsonify(order[id]),200)
    return make_response(jsonify({'error': 'ID not found'}), 404)

@app.route('/orders/<id>/<item>')
def get_neworder_byid_item(id,item):
    items=order[id].get(item)
    if items:
        return make_response(jsonify(items),200)
    return make_response(jsonify('Error no id'),404)

@app.route('/orders/<id>',methods=['POST'])
def post_new_order(id):
    req=request.get_json()
    if id in order:
        return make_response(jsonify('Orderid already exists'),404)
    order.update({id:req})
    return make_response(jsonify('New order created'),201)




@app.route('/orders/<id>',methods=['PUT'])
def update(id):
    req=request.get_json()
    if id in order:
        order[id]=req
        return make_response(jsonify('New order recieved'),200)
    return make_response(jsonify('Order id doesnt exist'),404)


@app.route('/orders/<id>',methods=['PATCH'])
def patch_records(id):
    req=request.get_json()
    if id in order:
        for k,v in req.items():
            order[id][k]=v
            return make_response(jsonify('Order partially updated'),200)
    order[id]=req
    return make_response(jsonify('Order complete updattion'),201)




if __name__ == "__main__":
    app.run(debug=True,port=5000,host='0.0.0.0')
