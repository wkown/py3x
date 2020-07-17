#!/usr/bin/python3
# -*- coding:utf-8 -*-
from kafka import TopicPartition, KafkaConsumer
consumer = KafkaConsumer('test', bootstrap_servers='192.168.112.131:9092')
print('start')
for msg in consumer:
    print(msg)
print('end')
