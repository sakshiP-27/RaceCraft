import flask
import fastf1
import datetime

app = flask.Flask(__name__)


@app.route('/drivers', methods=['GET'])
def get_drivers() -> flask.Response:
    """
    Fetches a list of Formula 1 drivers from the FastF1 API
    """
    try:
        fastf1.Cache.enable_cache('fastf1_cache')

        current_year = datetime.datetime.now().year
        now = datetime.datetime.now(datetime.timezone.utc)

        # Fetching the complete schedul for the current year
        schedule = fastf1.get_event_schedule(current_year)

        # Filtering out all the races that have already happened
        past_events = schedule[schedule['Session5Date'] < now]
        if past_events.empty:
            return flask.jsonify({'warning': 'No past events found for the current year.'}), 404

        # Gettting the latest race that happened
        latest_event = past_events.iloc[-1]
        event_name = latest_event['EventName']

        # Fetching the list of drivers
        session = fastf1.get_session(current_year, event_name, 'Qualifying')
        session.load()

        drivers = session.drivers

        drivers_list: list = []
        for driver in drivers:
            driver_info = session.get_driver(driver)
            drivers_list.append({
                'name': driver_info['FullName'],
                'code': driver_info['Abbreviation'],
                'team': driver_info['TeamName'],
            })

        return flask.jsonify(drivers_list), 200

    except Exception as e:
        print(f'Error occured: {e}')
        return flask.jsonify({'error': str(e)}), 500


@app.route('/circuits', methods=['GET'])
def get_circuits() -> flask.Response:
    """
    Fetches a list of Formula 1 circuits from the FastF1 API
    """
    try:
        fastf1.Cache.enable_cache('fastf1_cache')

        current_year = datetime.datetime.now().year
        now = datetime.datetime.now(datetime.timezone.utc)

        # fetching the complete schedule for the current year
        schedule = fastf1.get_event_schedule(current_year)

        # traversing the schedue to get the circuit details
        gp_list: list = []
        for _, row in schedule.iterrows():
            gp_list.append({
                'name': row['EventName'],
                'circuit': row['Location'],
                'country': row['Country'],
            })

        return flask.jsonify(gp_list), 200

    except Exception as e:
        print(f'Error occured: {e}')
        return flask.jsonify({'error': str(e)}), 500


@app.route('/quali-prediction', methods=['POST'])
def quali_prediction() -> flask.Response:
    """
    Predicts the qualifying results for the latest F1 Grand Prix
    """
    return flask.jsonify({'message': 'This endpoint is under construction.'}), 501


@app.route('/strategy-recommendation', methods=['POST'])
def strategy_recommenndation() -> flask.Response:
    """
    Suggests a tyre strategy for the upcoming F1 Grand Prix
    """
    return flask.jsonify({'message': 'This endpoint is under construction.'}), 501


@app.route('/')
def home():
    return "Welcome for the Formula1 API!"


if __name__ == '__main__':
    app.run(port=4000, debug=True)
