import re 
import json
import urllib.parse
from icalendar import Calendar, Event, prop, Alarm
from datetime import datetime, timedelta

def find_timetable_data_in_file(filename):
    with open(filename, "r") as file:
        result = re.search("""(?<=JSON.parse\(").+(?="\))""", file.read())
        if result != None:
            return json.loads(result.group().replace("\\/", "/").encode().decode('unicode-escape').replace("\\\\", "\\"))
    return None

def get_emoji_for_event_type(event_type):
    EVENT_EMOJIS = {"Practical":"👨‍💻", "Tutorial": "👨‍💻", "Lecture": "🎓", "Drop-In Class": "⬇", "Online Lecture":"🌐", "Online Computer Class": "🌐", "Seminar":"⌛", "Computer Class": "🖥️"}
    if event_type in EVENT_EMOJIS:
        return EVENT_EMOJIS[event_type]
    return "❓"

def get_maps_url(latitude, longitude, pin_name, use_google):
    if latitude == None or longitude == None:
        return None
    param_pin_name = urllib.parse.quote(pin_name or "Unknown Building")
    if use_google:
        return "https://www.google.com/maps/search/?api=1&query={0},{1}".format(latitude, longitude)
    else:
        return "https://maps.apple.com/?ll={0},{1}&q={2}".format(latitude, longitude, param_pin_name)

def format_staff_members(staff_members):
    if len(staff_members) == 0:
        return None
    
    formatted_staff_members = ""
    for i in range(len(staff_members)):
        if i > 0:
            if i == len(staff_members) - 1:
                formatted_staff_members += " and "
            else:
                formatted_staff_members += ", "
        formatted_staff_members += "{0} ({1})".format(staff_members[i][0], staff_members[i][1])
    return formatted_staff_members

def parse_datetime(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def create_ics_file(input_filename, use_google_maps):
    cal = Calendar()
    timetable_data = find_timetable_data_in_file(input_filename)

    if timetable_data == None:
        print("ERR - Could not find timetable in input.html.")

    for item in timetable_data:
        # Get item data.
        item_emoji = get_emoji_for_event_type(item["type"])
        item_type = item["type"]
        item_name = item["description"]
        item_module_code = item["module"]["name"]
        item_start_time = item["start_datetime"]
        item_end_time = item["end_datetime"]
        item_room_code, item_building_name, item_latitude, item_longitude = None, None, None, None
        if item["location"]:
            item_room_code = item["location"]["name"][2:]
            item_building_name = item["location"]["building"]["name"][2:]
            item_latitude = item["location"]["building"]["latitude"]
            item_longitude = item["location"]["building"]["longitude"]
        item_staff = [(staff_member["name"].title(), staff_member["email"]) for staff_member in item["staff"]]
        item_staff_string = "" if item_staff == [] else " with " + format_staff_members(item_staff)

        # Prepare event data.
        event_name = item_emoji + item_name
        event_location = (item_room_code or "Unknown Room") + ", " + (item_building_name or "Unknown Building")
        event_start_time = parse_datetime(item_start_time)
        event_end_time = parse_datetime(item_end_time)
        event_description = item_name + " (" + item_module_code + ") " + item_type.lower() + item_staff_string + "."
        event_url = get_maps_url(item_latitude, item_longitude, item_building_name, use_google=use_google_maps)

        # Create event and add it to calendar.
        event = Event()
        event.add("summary", event_name)
        event.add("dtstart", event_start_time)
        event.add("dtend", event_end_time)
        event.add("dtstamp", datetime.now())
        event.add("location", event_location)
        event.add("description", event_description)
        if event_url and event_url != "":
            event.add("URL;VALUE=URI", prop.vUri(event_url))
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alert_time = timedelta(minutes=-30)
        alarm.add('trigger', alert_time)
        event.add_component(alarm)
        cal.add_component(event)

    # Write calendar to file.
    with open("output.ics", "wb") as ical_file:
        ical_file.write(cal.to_ical())

def main():
    print("-" * 40)
    print("MyTimetable iCal Generator by Amren Stephenson")
    print("-" * 40)
    print("Go to MyTimetable and select the month view. Then choose 'File>Save Page As' and select the format 'Web Page, HTML Only'. Put that file in the same folder as this script, and rename the file 'input.html'.")
    print("-" * 40)
    use_google_maps = input("Use Google Maps? Y - Google, N - Apple\n").lower() == "y"
    create_ics_file("input.html", use_google_maps)
    print("Created 'output.ical'. It is recommened you create a new calendar for these events in your calendar app when you import this file.")
    print("-" * 40)

main()