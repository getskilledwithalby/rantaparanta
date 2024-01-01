from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_net_worth_and_breakdown(initial_amount, monthly_savings, annual_return, years):
    future_value = initial_amount
    total_contributions = initial_amount
    yearly_net_worth = []
    yearly_contributions = []

    for year in range(1, years + 1):
        total_contributions += monthly_savings * 12
        future_value = future_value * (1 + annual_return / 100) + monthly_savings * 12
        yearly_net_worth.append(future_value)
        yearly_contributions.append(total_contributions)

    interest_earned = future_value - total_contributions
    return future_value, total_contributions, interest_earned, yearly_net_worth, yearly_contributions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()  # Get data sent as JSON
    initial_amount = data.get('initial_amount', 0)
    monthly_savings = data.get('monthly_savings', 0)
    annual_return = data.get('annual_return', 0)
    years = data.get('years', 0)

    try:
        initial_amount = float(initial_amount)
        monthly_savings = float(monthly_savings)
        annual_return = float(annual_return)
        years = int(years)

        if initial_amount < 0 or monthly_savings < 0 or annual_return < 0 or years < 0:
            raise ValueError("Input values cannot be negative.")

        net_worth, total_contributions, interest_earned, yearly_net_worth, yearly_contributions = calculate_net_worth_and_breakdown(
            initial_amount, monthly_savings, annual_return, years)

        # Create yearly data with both net worth and contributions
        yearly_data = [
            {'year': year, 'netWorth': yearly_net_worth[year - 1], 'contributions': yearly_contributions[year - 1]}
            for year in range(1, years + 1)
        ]

        # Return the results as JSON
        return jsonify({
            'net_worth': net_worth,
            'total_contributions': total_contributions,
            'interest_earned': interest_earned,
            'years_data': yearly_data
        })
    except (ValueError, TypeError) as e:
        # If an error occurs, return the error message as JSON
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
    



