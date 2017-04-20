import collections
import csv

def generate_bicycle_deaths():
	# get all the bicyclist deaths
	rows = []
	idx_by_col = {}
	rows_by_case_year = collections.defaultdict(list)
	with open("person.csv") as person_f:
		header_row = None

		for person_row in csv.reader(person_f):
			if header_row == None:
				person_row.append("FIPS")
                                person_row.append("CITY")
				person_row.append("LATITUDE")
				person_row.append("LONGITUD")
				header_row = person_row
				rows.append(header_row)
				for i in range(len(header_row)):
					col_name = header_row[i]
					idx_by_col[col_name] = i
				continue

			per_type = person_row[idx_by_col["PER_TYP"]]
			if per_type != "6" and per_type != "7":
				continue

			sev = person_row[idx_by_col["INJ_SEV"]]
			if sev != "4": # only consider fatal injuries
				continue

			state = int(person_row[idx_by_col["STATE"]])
			county = int(person_row[idx_by_col["COUNTY"]])

			case = person_row[idx_by_col["ST_CASE"]]
			year = person_row[idx_by_col["YEAR"]]

			fips = "%02d%03d" % (state, county)
			person_row.append(fips)
			rows.append(person_row)
			rows_by_case_year[case + "-" + year].append(person_row)

	# get the lat/long
	with open("accident.csv") as accident_f:
		for accident in csv.DictReader(accident_f):
			case_year = accident["ST_CASE"] + "-" + accident["YEAR"]
			deaths = rows_by_case_year[case_year]
			for row in deaths:
                                row.append(accident["CITY"])
				row.append(accident["LATITUDE"])
				row.append(accident["LONGITUD"])

	# write it out
	with open("bicycle_deaths.csv", "w+") as deaths_f:
		deaths_writer = csv.writer(deaths_f)
		for row in rows:
			deaths_writer.writerow(row)


if __name__ == "__main__":
	generate_bicycle_deaths()
