import datetime
import io

import avro.schema
from avro.io import DatumWriter
from kafka import KafkaProducer

SCHEMA_PATH = "user.avsc"
SCHEMA = avro.schema.parse(open(SCHEMA_PATH).read())


def json_to_pb(jsonStringResponse):
    writer = DatumWriter(SCHEMA)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write(jsonStringResponse, encoder)
    raw_bytes = bytes_writer.getvalue()
    return raw_bytes


time1 = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
json_obj = {'name': 'fcao', 'value': '0.74', 'descibe': time1}
request = json_to_pb(json_obj)
producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092', key_serializer=str.encode)
producer.send('sample', key=time1, value=request)
producer.flush()
