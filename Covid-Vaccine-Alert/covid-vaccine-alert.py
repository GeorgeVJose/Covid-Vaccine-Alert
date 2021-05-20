import datetime
import json
import time
import winsound

import pandas as pd
import requests
from tabulate import tabulate


def start_alert():
    frequency = 2000
    duration = 300
    while True:
        winsound.Beep(frequency, duration)
        time.sleep(.1)


def get_tommorow_date():
    return (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d-%m-%Y')


def display_table(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

date = get_tommorow_date()


tamilnadu_district_data = {
    'District Name': ['Aranthangi', 'Ariyalur', 'Attur', 'Chengalpet', 'Chennai', 'Cheyyar', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kanchipuram', 'Kanyakumari', 'Karur', 'Kovilpatti', 'Krishnagiri', 'Madurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Palani', 'Paramakudi', 'Perambalur', 'Poonamallee', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Sivakasi',
                      'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukudi (Tuticorin)', 'Tiruchirappalli', 'Tirunelveli', 'Tirupattur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore', 'Viluppuram', 'Virudhunagar'],
    'District ID': [779, 555, 578, 565, 571, 778, 539, 547, 566, 556, 563, 552, 557, 544, 559, 780, 562, 540, 576, 558, 577, 564, 573, 570, 575, 546, 567, 781, 545, 561, 580, 551, 541, 569, 554, 560, 548, 550, 568, 572, 553, 574, 543, 542, 549]
}
display_table(tamilnadu_district_data)

kerala_district_data = {
    "District Name": ["Alappuzha", 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad'],
    "District ID": [301, 307, 306, 297, 295, 298, 304, 305, 302, 308, 300, 296, 303, 299, ]
}
display_table(kerala_district_data)

district_ids = [x for x in input(
    "Enter District IDs (with space separated): ").split()]
min_dose = int(input("Enter minimum dose: "))
wait_time = int(input("Enter wait time (minutes): "))

while True:
    hospital_data = []
    for district_id in district_ids:
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}"
        result = requests.get(url=url, headers=header)
        if result.status_code == 200:
            res_json = json.loads(result.text)
            for center in res_json["centers"]:
                if center is not None:
                    for session in center["sessions"]:
                        hospital_data.append(
                            [
                                center['center_id'],
                                center['name'],
                                center['address'],
                                center['district_name'],
                                session['available_capacity_dose1'],
                                session['available_capacity_dose2'],
                                session['min_age_limit'],
                                session['date']
                            ]
                        )
            # print(res_json)
        else:
            print("API Request Failed")
            print(result.text)
            exit(0)

    df_hospital = pd.DataFrame(
        hospital_data,
        columns=["Center ID", "Name", "Address", "District",
                 "Dose 1 Capacity", "Dose 2 Capacity", "Age limit", "Date"]
    )


    display_table(df_hospital.sort_values(
        by=['Dose 1 Capacity', 'Dose 2 Capacity'], ascending=False))

    if (
        (df_hospital["Dose 1 Capacity"] > min_dose) |
        (df_hospital["Dose 2 Capacity"] > min_dose)
    ).any():
        start_alert()

    print(f"\nINFO: Waiting for {wait_time} minutes..\n")
    time.sleep(wait_time*60)
