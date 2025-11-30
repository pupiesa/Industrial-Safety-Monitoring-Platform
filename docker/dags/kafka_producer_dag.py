from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import time
import random
from kafka import KafkaProducer
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

def produce_dummy_data():
    # Connect to broker1 on the confluent network
    producer = KafkaProducer(
        bootstrap_servers=['broker1:29092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    # Send 10 messages
    def random_number(detected):
        numbers = int(random.randint(0,detected))
        return numbers
    for i in range(10):
        detected = int(random.randint(1, 15))
        data = {
            'Id': random.randint(1, 100),
            "location": "office",
            'detect': detected,
            "img_path": f"/aws/x/img{i}{random_number(detected)}.jpg",
            'violation': {
                "Person": detected,
                "helmet": random_number(detected),
                "gloves": random_number(detected),
                "vest": random_number(detected),
                "boots": random_number(detected), 
                "goggles": random_number(detected),
                "none": random_number(detected),
                "no_helmet": random_number(detected),
                "no_goggle": random_number(detected),
                "no_gloves": random_number(detected),
                "no_boots": random_number(detected)
            },
            'timestamp': time.time(),
            'status': 'OK' if random.random() > 0.1 else 'CRITICAL'
        }
        producer.send('sensor_data', value=data)
        logging.info(f"Sent: {data}")
        time.sleep(1)
        
    producer.flush()
    producer.close()

with DAG(
    'kafka_producer',
    default_args=default_args,
    description='A simple DAG to produce dummy Kafka json data',
    schedule=timedelta(minutes=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    produce_task = PythonOperator(
        task_id='produce_dummy_data',
        python_callable=produce_dummy_data,
    )
    