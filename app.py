from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Временное хранилище для объявлений
ads = []

class Ad(Resource):
    @app.route('/ads', methods=['GET'])
    @app.route('/ads/<int:ad_id>', methods=['GET'])
    def get_ad(ad_id=None):
        if ad_id:
            ad = next((ad for ad in ads if ad['id'] == ad_id), None)
            if ad:
                return jsonify(ad)
            return jsonify({'message': 'Ad not found'}), 404
        return jsonify(ads)

    @app.route('/ads', methods=['POST'])
    def post():
        new_ad = request.get_json()

        # Проверка на наличие всех необходимых полей
        required_fields = ['title', 'description', 'owner']
        for field in required_fields:
            if field not in new_ad:
                return jsonify({'error': f'Missing field: {field}'}), 400

        new_ad['id'] = len(ads) + 1
        new_ad['created_at'] = datetime.now().isoformat()
        ads.append(new_ad)
        return jsonify(new_ad), 201
    @app.route('/ads/<int:ad_id>', methods=['DELETE'])
    def delete(ad_id):
        global ads
        ads = [ad for ad in ads if ad['id'] != ad_id]
        return {'message': 'Ad deleted'}

    @app.route('/ads/<int:ad_id>', methods=['PUT'])
    def put(ad_id):
        ad = next((ad for ad in ads if ad['id'] == ad_id), None)
        if not ad:
            return {'message': 'Ad not found'}, 404
        updated_data = request.get_json()
        ad.update(updated_data)
        return jsonify(ad)

api.add_resource(Ad, '/ads', '/ads/<int:ad_id>')

if __name__ == '__main__':
    app.run(debug=True)
