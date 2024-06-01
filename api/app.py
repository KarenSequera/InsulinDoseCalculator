from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate_insulin', methods=['POST'])
def calculate_insulin():
    data = request.get_json()
    
    try:
        current_glucose_level = data['current_glucose_level']
        target_glucose_level = data['target_glucose_level']
        isf = data['isf']
        total_carbs = data['total_carbs']
        icr = data['icr']
        iob = data.get('iob', 0)  # IOB is optional, default to 0 if not provided

        # Calculate the Correction Dose
        correction_dose = (current_glucose_level - target_glucose_level) / isf
        
        # Calculate the Carbohydrate Coverage Dose
        carb_coverage_dose = total_carbs / icr
        
        # Total Insulin Dose
        total_insulin_dose = correction_dose + carb_coverage_dose - iob
        
        return jsonify({
            'correction_dose': correction_dose,
            'carb_coverage_dose': carb_coverage_dose,
            'total_insulin_dose': total_insulin_dose
        })
    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {e}'}), 400
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)