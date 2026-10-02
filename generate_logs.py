import csv
import random
import datetime

# Configuration
NUM_ROWS = 5000
OUTPUT_FILE = 'usage_logs.csv'

# Data pools
USER_IDS = [f"U{str(i).zfill(5)}" for i in range(1, 501)]
ACTIONS = ['login', 'view_item', 'add_to_cart', 'purchase', 'search', 'logout']
ACTION_WEIGHTS = [10, 40, 20, 5, 20, 5] # Relative frequencies
DEVICE_TYPES = ['desktop', 'mobile', 'tablet']
DEVICE_WEIGHTS = [45, 50, 5]

def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_timestamp(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    
    # Add random hours, minutes, seconds
    random_date += datetime.timedelta(
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )
    return random_date.isoformat()

def main():
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = datetime.datetime.now()

    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['timestamp', 'user_id', 'action', 'device_type', 'ip_address', 'session_duration_seconds'])

        for _ in range(NUM_ROWS):
            timestamp = generate_timestamp(start_date, end_date)
            user_id = random.choice(USER_IDS)
            action = random.choices(ACTIONS, weights=ACTION_WEIGHTS, k=1)[0]
            device_type = random.choices(DEVICE_TYPES, weights=DEVICE_WEIGHTS, k=1)[0]
            ip_address = generate_ip()
            session_duration = random.randint(10, 3600) if action != 'login' else 0

            writer.writerow([
                timestamp,
                user_id,
                action,
                device_type,
                ip_address,
                session_duration
            ])

    print(f"Successfully generated {NUM_ROWS} rows of fake data in {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
