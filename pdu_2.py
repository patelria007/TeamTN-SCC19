from easysnmp import Session
from influxdb import InfluxDBClient
import sys, time, io
import datetime as dt
import pytz

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('pdu2')

session2 = Session(hostname='192.168.123.4', community='public', version=2)

starttime = time.time()

def pduTotalFunc():
	pdu2Total = session2.walk('1.3.6.1.4.1.21239.5.2.3.1.1')
	for item in pdu2Total:
		tot2(item)

def phaseTotalFunc():
	phase2Total = session2.walk('1.3.6.1.4.1.21239.5.2.3.2.1')
	for item in phase2Total:
		phase2(item)
	
def tot2(item):
	if item.oid in ['enterprises.21239.5.2.3.1.1.9.1', 'enterprises.21239.5.2.3.1.1.10.1', 'enterprises.21239.5.2.3.1.1.11.1', 'enterprises.21239.5.2.3.1.1.12.1']:
		real2PowDict = [ {
			"measurement": item.oid,
			"fields": {"value": int(item.value)},
			"time": now
		} ]
		client.write_points(real2PowDict)

def phase2(item):
	if item.oid in ['enterprises.21239.5.2.3.2.1.8.1', 'enterprises.21239.5.2.3.2.1.12.1', 'enterprises.21239.5.2.3.2.1.13.1', 'enterprises.21239.5.2.3.2.1.14.1', 'enterprises.21239.5.2.3.2.1.15.1']:
		phase2PowDict = [ {
			"measurement": item.oid,
			"fields": {"value": int(item.value)},
			"time": now
		} ]
		client.write_points(phase2PowDict)


while 1:
	utc_now = pytz.utc.localize(dt.datetime.utcnow())
	now = utc_now.isoformat()
	print(now + '\n')
	pduTotalFunc()
	phaseTotalFunc()
	print('_____________________________________________________\n')
	time.sleep(1.0 - ((time.time() - starttime) % 1.0))

