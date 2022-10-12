# timetable-ics
A simple Python script to scrape the JSON data from the month view of a user's [Durham MyTimetable](https://mytimetable.durham.ac.uk/calendar). It then creates a nicely formatted `.ics` file (including emojis!), which can be imported into your preferred calendar app.

## Instructions
1. Download `timetable-ics.py`.
2. Install dependancy: https://pypi.org/project/icalendar/ (Python3 package).
3. Go to MyTimetable and select the **month** view. Then choose 'File>Save Page As' and select the format **'Web Page, HTML Only'**. From this file it will get **all** your calendar data, not just the selected month.
4. Put that file in the **same folder** as the downloaded Python script, and **rename** the file `input.html`.
5. Run the script and choose whether you want a Google Maps or Apple Maps link.
6. Import the generated `output.ics` file into your favourite calendar app (it is **recommend** to create a **new calendar** just for this file so that you can remove/update just these events in the future).

## Example of a Created Event
|Property|Value|
|---|---|
|Name|👨‍💻Data Science|
|Location|CC0007, Chemistry/Geology Building|
|Description|Data Science (COMP2271) practical.|
|URL|\<MAPS LINK\>|
|Start Time|9:00|
|End Time|11:00|
|Alert|30 mins before event|
