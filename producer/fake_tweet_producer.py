from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
import datetime

fake = Faker()
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                            value_serializer=lambda x: json.dumps(x).encode('utf-8'))

hashtags = ['#AI', '#ML', '#DataScience', '#BigData', '#Kafka', '#Python', '#Programming']

def generate_fake_tweet():
    tweet = {
        'user': fake.user_name(),
        'text': fake.sentence(),
        'timestamp': datetime.datetime.now().isoformat(),
        'hashtags': random.sample(hashtags, random.randint(1, 3)),
        'likes': random.randint(0, 1000),
        'retweets': random.randint(0, 500)
    }
    return tweet

if __name__ == "__main__":
    while True:
        tweet = generate_fake_tweet()
        producer.send('tweets', value=tweet)
        print(f"Produced: {tweet}")
        time.sleep(random.randint(1, 3))  # Sleep for a random time between 1 and 5 seconds