import SQLAlchemy as SQLAlchemy
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLALchemy
from sqlalchemy import func
# After many constant efforts I still could not install postgresql in my pc it is 10 yrs old and wiht many softwares it gets slow quickly
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/database_name'

db = SQLAlchemy(app)
# creating a SQLAlchemy model for the housing data table
class HousingData(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Float)
    Square_footage = db.Column(db.Integer)
    location = db.Column(db.String)
    sale_price = db.Column(db.Float)

#creating an end point to handle the json data and store it in the database
@app.route('/api/housing', methods=['POST'])
def store_housing_data():
    try:
        data= request.get_json()
        for item in data:
            housing = HousingData(
                bedrooms = item['Bedrooms'],
                Bathrooms=item['Bathrooms'],
                square_footage=item['SquareFootage'],
                location=item['Location'],
                sale_price=item['SalePrice']

            )
            db.session.add(housing)
        db.session.commit()
        return jsonify({'message':'Data Stored successfully'}),201
    except Exception as e:
        return jsonify({'error': str(e)}),400


# creating end points for the desired output
@app.route('/api/housing/average', methods=['GET'])
def get_average_sale_price():
    try:
        overall_avg = db.session.query(func.avg(HousingData.sale_price)).scalar()
        return jsonify({'average_sale_price': overall_avg}),200
    except Exception as e:
        return jsonify({"error": str(e)}),400

@app.route('/api/housing/average_by_location', methods=['GET'])
def get_average_sale_price_by_location():
    try:
        avg_by_location = db.session.query(HousingData.location,func.avg(HousingData.sale_price)).group_by(HousingData.location).all()
        avg_dict = {location:avg for location, avg in avg_by_location}
        return jsonify({'average_sale_price_by_location':avg_dict}),200
    except Exception as e:
        return jsonify({'error':str(e)}),400


@app.route('/api/housing/max', methods=['GET'])
def get_max_sale_price():
    try:
        max_sale_price = db.session.query(func.max(HousingData.sale_price)).scalar()
        return jsonify({'max_sale_price': max_sale_price}),200
    except Exception as e:
        return jsonify({'error':str(e)}),400


@app.route('/api/housing/min', methods=['GET'])
def get_min_sale_price():
    try:
        min_sale_price = db.session.query(func.min(HousingData.sale_price)).scalar()
        return jsonify({'min_sale_price': min_sale_price}),200
    except Exception as e:
        return jsonify({'error':str(e)}),400




# run the flask application

if __name__=='__main__':
    app.run(debug=True)

