import csv
import requests
import sqlite3
import time

conn = sqlite3.connect("temperature.db")

def temperature_for_lat_long_hr(lat, lng, year, month, day, hr):
	if lat == "99.99990000":
		return ("", False)

	url = "http://api.wunderground.com/api/0b74fd7ebdce2b1b/history_%d%02d%02d/q/%s,%s.json" % (year, month, day, lat, lng)
	cached = conn.execute("SELECT temp FROM temperatures WHERE url='%s'" % url).fetchone()
	if cached is not None:
		return (cached[0], False)

	temp = None
	print "requesting url: " + url
	resp = requests.get(url).json()
	if not resp.has_key("history"):
		print "Error reading response for (%s, %s)" % (lat, lng)
		print resp
		return ("", True)
	observations = resp["history"]["observations"]
	hr_str = "%02d" % hr
	for observation in observations:
		if observation["date"]["hour"] == hr_str:
			temp = observation["tempi"]
			break

	if temp == None:
		#print observations
		print "Couldn't find temp for hour %s with url %s", hr_str, url
		return ("", True)

	conn.execute("INSERT INTO temperatures (url, temp) VALUES('%s', '%s')" % (url, temp))
	conn.commit()
	return (temp, True)


def generate_bicycle_deaths_with_temp():
	with open("bicycle_deaths_with_temps.csv", "w+") as outfile:
		writer = csv.writer(outfile)

		idx_by_col = {}
		header_row = None
		with open("bicycle_deaths.csv") as infile:
			for row in csv.reader(infile):
				if header_row is None:
					header_row = row
					for i in range(len(header_row)):
						idx_by_col[header_row[i]] = i

					row.append("TEMP_F")
					writer.writerow(row)
					continue

				lat = row[idx_by_col["LATITUDE"]]
				lng = row[idx_by_col["LONGITUD"]]
				year = int(row[idx_by_col["YEAR"]])
				month = int(row[idx_by_col["MONTH"]])
				day = int(row[idx_by_col["DAY"]])
				hour = int(row[idx_by_col["HOUR"]])

				(temp, made_request) = temperature_for_lat_long_hr(lat, lng, year, month, day, hour)
				row.append(temp)
				writer.writerow(row)
				if made_request:
					time.sleep(2.5)

if __name__ == "__main__":
	#print temperature_for_lat_long_hr("30.26576667", "-87.649669440000", 2015, 5, 27, 9)
	#print temperature_for_lat_long_hr("33.28613056", "-87.17944722", 2015, 6, 3, 23)
	generate_bicycle_deaths_with_temp()
	conn.close()