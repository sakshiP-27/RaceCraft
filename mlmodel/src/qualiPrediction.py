import fastf1
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error

fastf1.Cache.enable_cache('fastf1_cache')


class QualiPredictionModel:
    def __init__(self):
        self.encoder_driver = LabelEncoder()
        self.encoder_team = LabelEncoder()
        self.encoder_circuit = LabelEncoder()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def get_avg_team_lap_delta(self, session, team_name):
        laps = session.laps
        team_laps = laps[laps['Team'] == team_name]
        if team_laps.empty:
            return None
        team_laps = team_laps.pick_fastest()
        avg_time = team_laps['LapTime'].mean()
        return avg_time.total_seconds() if pd.notna(avg_time) else None

    def get_driver_last_positions(self, year, driver_code, session_type='Q'):
        last_positions: list = []
        past_rounds: list = list(range(1, 23))  # assuming up to 22 rounds

        for rnd in reversed(past_rounds):
            try:
                session = fastf1.get_session(year, rnd, session_type)
                session.load()
                result = session.results
                pos = result[result['Abbreviation'] == driver_code]['Position']
                if not pos.empty:
                    last_positions.append(int(pos.values[0]))
                if len(last_positions) == 3:
                    break
            except Exception:
                continue

        while len(last_positions) < 3:
            last_positions.append(20)  # assign worst pos if missing

        return last_positions

    def collect_training_data(self, year):
        data: list = []
        for rnd in range(1, 23):
            try:
                quali = fastf1.get_session(year, rnd, 'Q')
                quali.load()
                result = quali.results

                for _, row in result.iterrows():
                    driver = row['Abbreviation']
                    driver_name = row['FullName']
                    team = row['TeamName']
                    circuit = quali.event['EventName']
                    pos = row['Position']

                    last_3_q = self.get_driver_last_positions(year, driver, 'Q')
                    last_3_r = self.get_driver_last_positions(year, driver, 'R')
                    avg_delta = self.get_avg_team_lap_delta(quali, team)

                    if avg_delta is None:
                        continue

                    # Dummy values for temp, humidity, rain (random or fixed for now)
                    data.append({
                        'circuit_name': circuit,
                        'driver_name': driver_name,
                        'team_name': team,
                        'temperature': 25.0,
                        'humidity': 60.0,
                        'rain_chance': 0.2,
                        'last_3_quali_positions': sum(last_3_q) / 3,
                        'last_3_race_positions': sum(last_3_r) / 3,
                        'team_avg_lap_time_delta': avg_delta,
                        'qualifying_position': pos
                    })

            except Exception as e:
                print(f"Skipping round {rnd}: {e}")

        return pd.DataFrame(data)

    def train_model(self, df: pd.DataFrame):
        df = df.dropna()

        if df.empty:
            raise ValueError("Collected training data is empty. Check logs for skipped rounds.")

        df['driver_name'] = self.encoder_driver.fit_transform(df['driver_name'])
        df['team_name'] = self.encoder_team.fit_transform(df['team_name'])
        df['circuit_name'] = self.encoder_circuit.fit_transform(df['circuit_name'])

        X = df.drop(columns=['qualifying_position'])
        y = df['qualifying_position']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        preds = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        print(f"Model trained. MAE: {mae:.2f}")

        joblib.dump(self.model, 'quali_predictor.pkl')
        joblib.dump(self.encoder_driver, 'driver_encoder.pkl')
        joblib.dump(self.encoder_team, 'team_encoder.pkl')
        joblib.dump(self.encoder_circuit, 'circuit_encoder.pkl')

        print("Model and encoders saved successfully.")

    def run(self):
        years: list = [2023, 2024, 2025]
        df = {}
        for year in years:
            df.append(self.collect_training_data(year))
        self.train_model(df)


if __name__ == '__main__':
    model = QualiPredictionModel()
    model.run()
