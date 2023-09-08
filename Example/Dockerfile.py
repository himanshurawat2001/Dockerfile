from flask import Flask, request, jsonify

app = Flask(__name__)

pantry_data = {}

@app.route('/add-item', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        pantry_id = data.get('pantry_id')
        basket_key = data.get('basket_key')
        value = data.get('value')
        
        if pantry_id and basket_key:
            pantry = pantry_data.setdefault(pantry_id, {})
            pantry[basket_key] = value
            return jsonify({"message": "Item added successfully"}), 201
        else:
            return jsonify({"message": "Pantry ID and basket key are required"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/get-item', methods=['GET'])
def get_item():
    try:
        pantry_id = request.args.get('pantry_id')
        basket_key = request.args.get('basket_key')
        
        if pantry_id and basket_key and pantry_id in pantry_data and basket_key in pantry_data[pantry_id]:
            value = pantry_data[pantry_id][basket_key]
            return jsonify({"value": value}), 200
        else:
            return jsonify({"message": "Item not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/list-baskets', methods=['GET'])
def list_baskets():
    try:
        pantry_id = request.args.get('pantry_id')
        filter_name = request.args.get('filter_name')
        
        if pantry_id in pantry_data:
            pantry = pantry_data[pantry_id]
            
            if filter_name:
                filtered_baskets = {k: v for k, v in pantry.items() if filter_name in k}
                return jsonify(filtered_baskets), 200
            else:
                return jsonify(pantry), 200
        else:
            return jsonify({"message": "Pantry not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/update-item', methods=['PUT'])
def update_item():
    try:
        data = request.get_json()
        pantry_id = data.get('pantry_id')
        basket_key = data.get('basket_key')
        new_value = data.get('new_value')
        
        if pantry_id and basket_key and new_value:
            if pantry_id in pantry_data and basket_key in pantry_data[pantry_id]:
                pantry_data[pantry_id][basket_key] = new_value
                return jsonify({"message": "Item updated successfully"}), 200
            else:
                return jsonify({"message": "Item not found"}), 404
        else:
            return jsonify({"message": "Pantry ID, basket key, and new value are required"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/delete-item', methods=['DELETE'])
def delete_item():
    try:
        pantry_id = request.args.get('pantry_id')
        basket_key = request.args.get('basket_key')
        
        if pantry_id and basket_key:
            if pantry_id in pantry_data and basket_key in pantry_data[pantry_id]:
                del pantry_data[pantry_id][basket_key]
                return jsonify({"message": "Item deleted successfully"}), 200
            else:
                return jsonify({"message": "Item not found"}), 404
        else:
            return jsonify({"message": "Pantry ID and basket key are required"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
