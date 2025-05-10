import pandas as pd
import numpy as np
import random

def gen_cust_data(num_cust=100, num_pri_cust=60):
    """
    Generate a synthetic dataset for python/pandas basic training.

    Parameters:
    - num_cust: Number of account ID to generate.
    - num_pri_cust: Number of primary account IDs to generate.

    Returns:
    - uber_df: Pandas DataFrame
    """
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Create base customer list
    cust_ids = [i for i in range(1, num_cust+1)]  # 100 customers

    # Generate a list of all possible dates over the past year
    date_range = pd.date_range(end=pd.Timestamp.today(), periods=30).to_list()

    # Generate trip data
    trip_records = []
    for cust_id in cust_ids:
        num_trips = random.randint(1, 15)
        trip_dates = sorted(random.sample(date_range, num_trips))
        for trip_date in trip_dates:
            trip_distance = round(np.random.exponential(scale=5), 2)  # Avg ~5 miles
            trip_duration = round(trip_distance / np.random.uniform(0.5, 1.5), 2)  # Speed variability
            trip_tip = round(np.random.uniform(0, 10), 2)  # Tips $0–$10
            trip_fare = round(np.random.uniform(5, 50), 2)
            wait_time = round(np.random.exponential(scale=3), 0)  # Avg ~3 minutes wait
            trip_rating = np.random.choice([1,2,3,4,5])

            trip_records.append({
                'cust_id': cust_id,
                'trip_date': trip_date.date(),
                'trip_distance': trip_distance,
                'trip_duration': trip_duration,
                'trip_fare': trip_fare,
                'trip_tips': trip_tip,
                'trip_wait_time': wait_time,
                'trip_rating': trip_rating
            })

    # Create DataFrame
    uber_df = pd.DataFrame(trip_records)
    print(uber_df.head())

    pri_ids = random.sample(cust_ids, num_pri_cust)

    household = []
    sampled_pri_ids = [i for i in pri_ids]

    for cust_id in cust_ids:
        if cust_id in pri_ids:
            household.append({'pri_id': cust_id, 'sec_id': cust_id})
    for cust_id in cust_ids:
        if cust_id not in pri_ids:
            pri = np.random.choice(sampled_pri_ids)
            sampled_pri_ids.remove(pri)
            household.append({'pri_id': pri, 'sec_id': cust_id})
    household_df = pd.DataFrame(household)
    uber_df = pd.merge(uber_df, household_df, left_on='cust_id', right_on = 'sec_id', how='left')
    uber_df.to_csv('./data/uber_data.csv', index=False)
    return uber_df

if __name__ == "__main__":
    gen_cust_data()
    print("Data generation complete.")

    