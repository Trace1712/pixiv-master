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
for i in range(2):
    producer.send('sample', key=time1, value=request)
producer.flush()

# java post
# public Map<String, KolStoredReporter> batchAddKols(List<KolUser> users, String platform) throws IOException {
#         List<BatchAddKolParam.Kol> kols = users.stream()
#                 .map(this::buildBatchAddKol)
#                 .collect(Collectors.toList());
#         BatchAddKolParam param = BatchAddKolParam.builder()
#                 .source(STORED_KOL_SOURCE_CRAWLER)
#                 .platform(platform)
#                 .kols(kols)
#                 .build();
#
#         String result = HttpUtils.post(WITAKE_BATCH_ADD_API, GSON.toJson(param));
#         return GSON.fromJson(result, new TypeToken<Map<String, KolStoredReporter>>() {
#         }.getType());
#     }