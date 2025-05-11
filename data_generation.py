import pandas as pd
import numpy as np
import random
from faker import Faker

def gen_cust_data(num_cust=100, num_pri_cust=60, periods=90):
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
    date_range = pd.date_range(end=pd.Timestamp.today(), periods=periods).to_list()

    # Generate trip data
    trip_records = []
    for cust_id in cust_ids:
        num_trips = random.randint(1, 30)
        trip_dates = sorted(random.sample(date_range, num_trips))
        for trip_date in trip_dates:
            trip_distance = round(np.random.exponential(scale=5), 2)  # Avg ~5 miles
            trip_duration = round(trip_distance / np.random.uniform(0.5, 1.5), 2)  # Speed variability
            trip_tip = round(np.random.uniform(0, 10), 2)  # Tips $0–$10
            trip_fare = round(np.random.uniform(5, 50), 2)
            wait_time = round(np.random.exponential(scale=3), 0)  # Avg ~3 minutes wait
            trip_rating = np.random.choice([1,2,3,4,5,np.nan], p=[0.05, 0.2, 0.1, 0.3, 0.25, 0.1])  # Ratings with NaN

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

    

    household = []
    pri_ids = random.sample(cust_ids, num_pri_cust)
    sampled_pri_ids = [i for i in pri_ids]
    for cust_id in cust_ids:
        if cust_id in pri_ids:
            household.append({'pri_id': np.nan, 'cust_id': cust_id})
    for cust_id in cust_ids:
        if cust_id not in pri_ids:
            pri = np.random.choice(sampled_pri_ids)
            sampled_pri_ids.remove(pri)
            household.append({'pri_id': pri, 'cust_id': cust_id})
    household_df = pd.DataFrame(household)

    cust_names = pd.DataFrame()
    cust_names['cust_id'] = cust_ids
    fake = Faker()
    cust_names['cust_name'] = [fake.name() for _ in range(len(cust_names))]

    uber_df = pd.merge(uber_df, household_df, on='cust_id', how='left')
    uber_df = pd.merge(uber_df, cust_names, on='cust_id', how='left')
    uber_df['trip_id'] = [f'T{i}' for i in range(1,len(uber_df) + 1)]
    uber_df['driver_id'] = np.random.choice([i for i in range(1, 151)], size=len(uber_df))
    uber_df.to_csv('./data/cust.csv', index=False)
    return uber_df

def gen_driver_data(num_drivers=150):
    """
    Generate a synthetic dataset for driver data.

    Parameters:
    - num_drivers: Number of driver IDs to generate.

    Returns:
    - driver_df: Pandas DataFrame
    """
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Create base driver list
    driver_ids = [i for i in range(1, num_drivers+1)]  # 100 drivers

    # Generate trip data
    driver_df = pd.DataFrame()
    driver_df['driver_id'] = driver_ids
    driver_df['vehicle'] = np.random.choice(['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan','Telsa'], size=len(driver_df))
    driver_df['test_control'] = np.random.choice([True, False], size=len(driver_df))
    
    # Save to CSV
    driver_df.to_csv('./data/driver.csv', index=False)
    
    return driver_df


if __name__ == "__main__":
    gen_cust_data()
    gen_driver_data()
    print("Data generation complete.")

    