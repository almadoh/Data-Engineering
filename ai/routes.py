import json
import pandas as pd
from bson import SON, Regex
from flask import render_template, jsonify
from ai import app
from ai.data import collection


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/tophashtags')
def toph():
    pipeline = [
        {
            u"$unwind": {
                u"path": u"$hashtags",
                u"preserveNullAndEmptyArrays": False
            }
        },
        {
            u"$project":
                {
                    u"hashtags": {u"$toLower": u"$hashtags"}
                }
        },
        {
            u"$group": {
                u"_id": u"$hashtags",
                u"tagcount": {
                    u"$sum": 1.0
                }
            }
        },
        {
            u"$sort": SON([(u"tagcount", -1)])
        },
        {
            u"$limit": 100.0
        }
    ]

    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=False
    )
    output = []
    for i in cursor:
        # if i["_id"] == "artificialintelligence":
        #     output.append({"name": i["_id"], "weight": 150000})
        #     continue
        output.append({"name": i["_id"], "weight": i["tagcount"]})
    return jsonify(output)


@app.route('/wordcloud')
def cloud():
    return render_template('wordcloud.html')


@app.route('/verified')
def ver():
    pipeline = [
        {
            u"$unwind": {
                u"path": u"$user.verified",
                u"preserveNullAndEmptyArrays": False
            }
        },
        {
            u"$group": {
                u"_id": u"$user.verified",
                u"count": {
                    u"$sum": 1.0
                }
            }
        }
    ]
    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=False
    )
    output = []
    v = uv = 0
    for i in cursor:
        if i["_id"]:
            v = i["count"]
        else:
            uv = i["count"]
    output.append({"name": "verified", "y": v / (v + uv), "sliced": True, "selected": True})
    output.append({"name": "unverified", "y": uv / (v + uv)})
    return jsonify(output)


@app.route('/piechart')
def pie():
    return render_template('pie.html')


@app.route('/location')
def loc():
    countries = {
        "AF": "Afghanistan",
        "AX": "Åland Islands",
        "AL": "Albania",
        "DZ": "Algeria",
        "AS": "American Samoa",
        "AD": "Andorra",
        "AO": "Angola",
        "AI": "Anguilla",
        "AQ": "Antarctica",
        "AG": "Antigua and Barbuda",
        "AR": "Argentina",
        "AM": "Armenia",
        "AW": "Aruba",
        "AU": "Australia",
        "AT": "Austria",
        "AZ": "Azerbaijan",
        "BS": "Bahamas",
        "BH": "Bahrain",
        "BD": "Bangladesh",
        "BB": "Barbados",
        "BY": "Belarus",
        "BE": "Belgium",
        "BZ": "Belize",
        "BJ": "Benin",
        "BM": "Bermuda",
        "BT": "Bhutan",
        "BO": "Bolivia",
        "BA": "Bosnia and Herzegovina",
        "BW": "Botswana",
        "BR": "Brazil",
        "IO": "British Indian Ocean Territory",
        "VG": "British Virgin Islands",
        "BN": "Brunei Darussalam",
        "BG": "Bulgaria",
        "BF": "Burkina Faso",
        "BI": "Burundi",
        "KH": "Cambodia",
        "CM": "Cameroon",
        "CA": "Canada",
        "CV": "Cape Verde",
        "BQ": "Caribbean Netherlands",
        "KY": "Cayman Islands",
        "CF": "Central African Republic",
        "TD": "Chad",
        "CL": "Chile",
        "CN": "China",
        "CX": "Christmas Island",
        "CC": "Cocos Islands",
        "CO": "Colombia",
        "KM": "Comoros",
        "CG": "Congo",
        "CK": "Cook Islands",
        "CR": "Costa Rica",
        "HR": "Croatia",
        "CU": "Cuba",
        "CW": "Curaçao",
        "CY": "Cyprus",
        "CZ": "Czech Republic",
        "CD": "Democratic Republic of the Congo",
        "DK": "Denmark",
        "DJ": "Djibouti",
        "DM": "Dominica",
        "DO": "Dominican Republic",
        "EC": "Ecuador",
        "EG": "Egypt",
        "SV": "El Salvador",
        "GQ": "Equatorial Guinea",
        "ER": "Eritrea",
        "EE": "Estonia",
        "ET": "Ethiopia",
        "FK": "Falkland Islands",
        "FO": "Faroe Islands",
        "FM": "Federated States of Micronesia",
        "FJ": "Fiji",
        "FI": "Finland",
        "FR": "France",
        "GF": "French Guiana",
        "PF": "French Polynesia",
        "TF": "French Southern Territories",
        "GA": "Gabon",
        "GM": "Gambia",
        "GE": "Georgia",
        "DE": "Germany",
        "GH": "Ghana",
        "GI": "Gibraltar",
        "GR": "Greece",
        "GL": "Greenland",
        "GD": "Grenada",
        "GP": "Guadeloupe",
        "GU": "Guam",
        "GT": "Guatemala",
        "GN": "Guinea",
        "GW": "Guinea-Bissau",
        "GY": "Guyana",
        "HT": "Haiti",
        "HN": "Honduras",
        "HK": "Hong Kong",
        "HU": "Hungary",
        "IS": "Iceland",
        "IN": "India",
        "ID": "Indonesia",
        "IR": "Iran",
        "IQ": "Iraq",
        "IE": "Ireland",
        "IM": "Isle of Man",
        "IL": "Israel",
        "IT": "Italy",
        "CI": "Ivory Coast",
        "JM": "Jamaica",
        "JP": "Japan",
        "JE": "Jersey",
        "JO": "Jordan",
        "KZ": "Kazakhstan",
        "KE": "Kenya",
        "KI": "Kiribati",
        "XK": "Kosovo",
        "KW": "Kuwait",
        "KG": "Kyrgyzstan",
        "LA": "Laos",
        "LV": "Latvia",
        "LB": "Lebanon",
        "LS": "Lesotho",
        "LR": "Liberia",
        "LY": "Libya",
        "LI": "Liechtenstein",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "MO": "Macau",
        "MK": "Macedonia",
        "MG": "Madagascar",
        "MW": "Malawi",
        "MY": "Malaysia",
        "MV": "Maldives",
        "ML": "Mali",
        "MT": "Malta",
        "MH": "Marshall Islands",
        "MQ": "Martinique",
        "MR": "Mauritania",
        "MU": "Mauritius",
        "YT": "Mayotte",
        "MX": "Mexico",
        "MD": "Moldova",
        "MC": "Monaco",
        "MN": "Mongolia",
        "ME": "Montenegro",
        "MS": "Montserrat",
        "MA": "Morocco",
        "MZ": "Mozambique",
        "MM": "Myanmar",
        "NA": "Namibia",
        "NR": "Nauru",
        "NP": "Nepal",
        "NL": "Netherlands",
        "NC": "New Caledonia",
        "NZ": "New Zealand",
        "NI": "Nicaragua",
        "NE": "Niger",
        "NG": "Nigeria",
        "NU": "Niue",
        "NF": "Norfolk Island",
        "KP": "North Korea",
        "MP": "Northern Mariana Islands",
        "NO": "Norway",
        "OM": "Oman",
        "PK": "Pakistan",
        "PW": "Palau",
        "PS": "Palestine",
        "PA": "Panama",
        "PG": "Papua New Guinea",
        "PY": "Paraguay",
        "PE": "Peru",
        "PH": "Philippines",
        "PN": "Pitcairn Islands",
        "PL": "Poland",
        "PT": "Portugal",
        "PR": "Puerto Rico",
        "QA": "Qatar",
        "RE": "Reunion",
        "RO": "Romania",
        "RU": "Russia",
        "RW": "Rwanda",
        "SH": "Saint Helena",
        "KN": "Saint Kitts and Nevis",
        "LC": "Saint Lucia",
        "PM": "Saint Pierre and Miquelon",
        "VC": "Saint Vincent and the Grenadines",
        "WS": "Samoa",
        "SM": "San Marino",
        "ST": "São Tomé and Príncipe",
        "SA": "Saudi Arabia",
        "SN": "Senegal",
        "RS": "Serbia",
        "SC": "Seychelles",
        "SL": "Sierra Leone",
        "SG": "Singapore",
        "SX": "Sint Maarten",
        "SK": "Slovakia",
        "SI": "Slovenia",
        "SB": "Solomon Islands",
        "SO": "Somalia",
        "ZA": "South Africa",
        "GS": "South Georgia and the South Sandwich Islands",
        "KR": "South Korea",
        "SS": "South Sudan",
        "ES": "Spain",
        "LK": "Sri Lanka",
        "SD": "Sudan",
        "SR": "Suriname",
        "SJ": "Svalbard and Jan Mayen",
        "SZ": "Eswatini",
        "SE": "Sweden",
        "CH": "Switzerland",
        "SY": "Syria",
        "TW": "Taiwan",
        "TJ": "Tajikistan",
        "TZ": "Tanzania",
        "TH": "Thailand",
        "TL": "Timor-Leste",
        "TG": "Togo",
        "TK": "Tokelau",
        "TO": "Tonga",
        "TT": "Trinidad and Tobago",
        "TN": "Tunisia",
        "TR": "Turkey",
        "TM": "Turkmenistan",
        "TC": "Turks and Caicos Islands",
        "TV": "Tuvalu",
        "UG": "Uganda",
        "UA": "Ukraine",
        "AE": "United Arab Emirates",
        "GB": "United Kingdom",
        "US": "United States",
        "UM": "United States Minor Outlying Islands",
        "VI": "United States Virgin Islands",
        "UY": "Uruguay",
        "UZ": "Uzbekistan",
        "VU": "Vanuatu",
        "VA": "Vatican City",
        "VE": "Venezuela",
        "VN": "Vietnam",
        "WF": "Wallis and Futuna",
        "EH": "Western Sahara",
        "YE": "Yemen",
        "ZM": "Zambia",
        "ZW": "Zimbabwe"
    }
    pipeline1 = [
        {
            u"$unwind": {
                u"path": u"$user.location",
                u"preserveNullAndEmptyArrays": False
            }
        },
        {
            u"$group": {
                u"_id": u"$user.location",
                u"locationcount": {
                    u"$sum": 1.0
                }
            }
        },
        {
            u"$sort": SON([(u"locationcount", -1)])
        },
        {
            u"$limit": 100000.0
        }
    ]
    pipeline2 = [
        {
            u"$project": {
                u"user.username": 1.0,
                u"user.location": 1.0,
                u"user.followersCount": 1.0
            }
        },
        {
            u"$group": {
                u"_id": u"$user.username",
                u"numberoftweets": {
                    u"$sum": 1.0
                },
                u"loc": {
                    u"$first": u"$user.location"
                }
            }
        },
        {
            u"$sort": SON([(u"numberoftweets", -1)])
        },
        {
            u"$limit": 100000.0
        }
    ]
    cursor1 = collection.aggregate(
        pipeline1,
        allowDiskUse=False
    )
    cursor2 = collection.aggregate(
        pipeline2,
        allowDiskUse=False
    )
    output = {}
    rank = 0
    done = []
    for location in cursor1:
        special = False
        if location == "":
            continue
        for country_dict in countries.items():
            country = country_dict[1]
            countrycode = country_dict[0]
            flag = (location["_id"] == "North Carolina, USA" and countrycode == "US")
            if flag:
                special = True
            maxtweets = 0
            topname = 0
            if country == location["_id"] or special:
                totaltweetsinloc = location["locationcount"]
                if countrycode in done:
                    old = output[countrycode]
                    output.pop(countrycode)
                    old["gdp"] = old["gdp"] + totaltweetsinloc
                    output[countrycode] = old
                    break
                rank += 1
                if special:
                    totaltweetsinloc = 23980
                for user in cursor2:
                    if user["loc"] == location["_id"]:
                        maxtweets = user["numberoftweets"]
                        topname = user["_id"]
                        break
                output[countrycode] = {"gdp": totaltweetsinloc,
                                       "change": topname,
                                       "gdpAdjusted": maxtweets,
                                       "changeAdjusted": rank
                                       }
                done.append(countrycode)
                break

    return jsonify(output)


@app.route('/mapchart')
def maps():
    return render_template('map.html')


@app.route('/totaltweets')
def total():
    pipeline1 = [
        {
            u"$group": {
                u"_id": u"$user.id",
                u"count": {
                    u"$sum": 1.0
                }
            }
        },
        {
            u"$group": {
                u"_id": u"_id",
                u"count": {
                    u"$sum": 1.0
                }
            }
        }
    ]
    pipeline2 = [
        {
            u"$unwind": {
                u"path": u"$user.verified",
                u"preserveNullAndEmptyArrays": False
            }
        },
        {
            u"$group": {
                u"_id": u"$user.verified",
                u"count": {
                    u"$sum": 1.0
                }
            }
        }
    ]
    cursor1 = collection.aggregate(
        pipeline1,
        allowDiskUse=False
    )
    cursor2 = collection.aggregate(
        pipeline2,
        allowDiskUse=False
    )
    output = []
    # total tweets
    output.append({"totaltweets": (collection.count_documents({}))})
    sumOfUsers = 0
    # total users
    for i in cursor1:
        sumOfUsers += i["count"]
    output.append({"totalusers": sumOfUsers})
    # verfied users
    for i in cursor2:
        if i["_id"]:
            output.append({"verified": i["count"]})
    return jsonify(output)


@app.route('/graph')
def bydate():
    pipeline = [
        {
            u"$group": {
                u"_id": u"$date",
                u"count": {
                    u"$sum": 1.0
                }
            }
        },
        {
            u"$project": {
                u"count": 1.0,
                u"date": {
                    u"$split": [
                        u"$_id",
                        u"T"
                    ]
                }
            }
        },
        {
            u"$unwind": {
                u"path": u"$date"
            }
        },
        {
            u"$match": {
                u"date": {
                    u"$regex": Regex(u"^\d{4}-\d{2}-\d{2}")
                }
            }
        },
        {
            u"$project": {
                u"count": 1.0,
                u"date": {
                    u"$split": [
                        u"$date",
                        u"-"
                    ]
                }
            }
        },
        {
            u"$unwind": {
                u"path": u"$date",
                u"includeArrayIndex": u"index",
                u"preserveNullAndEmptyArrays": False
            }
        },
        {
            u"$match": {
                u"index": 1.0
            }
        },
        {
            u"$group": {
                u"_id": u"$date",
                u"count": {
                    u"$sum": u"$count"
                }
            }
        },
        {
            u"$sort": SON([(u"_id", 1)])
        }
    ]
    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=False
    )
    output = []
    j = list(cursor)
    index = 0
    for i in range(1, 13):
        if i == int(j[index]["_id"]):
            output.append(int(j[index]["count"]))
            index += 1
            if index == len(j):
                index = 0
        else:
            output.append(0)
    return jsonify(output)


@app.route('/lang')
def lang():
    pipeline = [
        {
            u"$group": {
                u"_id": u"$lang",
                u"count": {
                    u"$sum": 1.0
                }
            }
        },
        {
            u"$sort": SON([(u"count", -1)])
        },
        {
            u"$limit": 4.0
        }
    ]
    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=False
    )
    output = []
    for record in cursor:
        if (record["_id"] != "qme"):
            output.append({"lang": record["_id"], "count": record["count"]})
    return output


@app.route('/pages-sign-in')
def signin():
    return render_template("pages-sign-in.html")


@app.route('/pages-sign-up')
def signup():
    return render_template("pages-sign-up.html")


@app.route('/hours')
def hour():
    pipeline = [
        {
            u"$group": {
                u"_id": u"$date",
                u"count": {
                    u"$sum": 1.0
                }
            }
        },
        {
            u"$project": {
                u"count": 1.0,
                u"date": {
                    u"$split": [
                        u"$_id",
                        u"T"
                    ]
                }
            }
        },
        {
            u"$unwind": {
                u"path": u"$date"
            }
        },
        {
            u"$match": {
                u"date": {
                    u"$regex": Regex(u"\\+00:00")
                }
            }
        },
        {
            u"$project": {
                u"count": 1.0,
                u"date": {
                    u"$split": [
                        u"$date",
                        u"+00:00"
                    ]
                }
            }
        },
        {
            u"$unwind": {
                u"path": u"$date",
                u"includeArrayIndex": u"index",
                u"preserveNullAndEmptyArrays": False
            }
        },
        {
            u"$project": {
                u"count": 1.0,
                u"date": {
                    u"$split": [
                        u"$date",
                        u":"
                    ]
                }
            }
        },
        {
            u"$unwind": {
                u"path": u"$date",
                u"includeArrayIndex": u"index",
                u"preserveNullAndEmptyArrays": False
            }
        },
        {
            u"$match": {
                u"index": 0.0
            }
        },
        {
            u"$group": {
                u"_id": u"$date",
                u"count": {
                    u"$sum": u"$count"
                }
            }
        },
        {
            u"$sort": SON([(u"_id", 1)])
        }
    ]
    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=False
    )
    output = []
    for record in cursor:
        if record["_id"] != "":
            output.append({"hour": record["_id"], "count": record["count"]})
    return output


@app.route('/sentiment')
def sent():
    # positivetweets=pd.read_csv("static/csv/positive.csv")
    # negativetweets=pd.read_csv("static/csv/negative.csv")
    # neutraltweets=pd.read_csv("static/csv/neutral.csv")
    values = pd.read_csv(open('ai/static/csv/values.csv'))
    output = [{"positive": str(values["Total"][0])},
              {"negative": str(values["Total"][1])},
              {"neutral": str(values["Total"][2])},
              {"total": str(values["Total"][0] + values["Total"][1] + values["Total"][2])}]
    return jsonify(output)


@app.route('/tablevalues')
def tablevalues():
    data1 = pd.read_csv('ai/static/csv/positive.csv')
    data2 = pd.read_csv('ai/static/csv/negative.csv')
    data3 = pd.read_csv('ai/static/csv/neutral.csv')
    data1 = data1.sort_values(by=['pos'], ascending=False).head(20)
    data2 = data2.sort_values(by=['neg'], ascending=False).head(20)
    data3 = data3.sort_values(by=['neu'], ascending=False).head(20)
    frames = [data1, data2, data3]
    result = pd.concat(frames)
    result = result.drop(columns=["0", "polarity", "subjectivity", "compound"])
    result["text"] = result["text"].str.strip()
    result["text"] = result["text"].str.replace("  ", "")
    result["Occurrences"] = 1
    result = result.groupby(["text", "pos", "neu", "neg", "sentiment"])["Occurrences"].count().reset_index()
    print(result.head())
    data = result.to_json(orient="split")
    data = json.loads(data)
    data = json.dumps(data, indent=4)
    return data


@app.route('/table')
def table():
    return render_template("table.html")
