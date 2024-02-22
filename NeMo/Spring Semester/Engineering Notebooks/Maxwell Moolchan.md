# Engineering Notebook - Maxwell Moolchan

## Semester 2 (Spring)
### Week 1 (10 January 2024 - 13 January 2024)
    - (11 January 2024) Discussion with Akbas regarding changes in second semester senior design & discussed with group current position in project and expectations for the semester.
        - Some people want to switch roles on the team.
        - OpenskyAPI Difficulties.
        - Product Vision statement.
### Week 2 (14 January 2024 - 20 January 2024)
    - (16 January 2024) Discussion with TA regarding where we are in the project, where we are going, items that need to be completed this sprint, and issues we have had.
        - OpenskyAPI Difficulties
        - Discussion of moving to a different flight data API
    - (18 January 2024) Found temporary solution for saving data from opensky
        - temporary save file with each successful call to opensky for days when opensky is down.
### Week 3 (21 January 2024 - 27 January 2024)
    - (25 January 2024) 
        - Fixed zoom locking not working on certain map modes, should no longer be able to zoom in to blackout.
        - Commited needed background to main since the remote copy of main did not have it.
### Week 4 (28 January 2024 - 3 February 2024)
    - (30 January 2024) Bug fixes and zoom icon changes.
        - Bug Fix, plane rotation was throwing off correct position location of aircraft, rotation origin should be set to center center, rather than the default bottom center.
    - (1 February 2024) icon size changes and bug fixes.
        - Implemented icon size change with zoom to lower the amount of crowding on the map.
        - Bug fix aircraft showing through the zoomout message.
### Week 5 (4 February 2024 - 10 February 2024)
    - (7 February 2024) Added settings pane and settings button as discussed with Taylor for future settings.
        - Added settings pane within the information pane.
        - Added settings button on the right side of map screen with other map buttons, button is togglable and when other panes are activated button works as intended.
    - (8 February 2024) Presented Spring Demo in IC.
        - Discussed new information pane design with Taylor.
        - Presented presentation in IC and accomplishments for Spring Sprint 1.
### Week 6 (11 February 2024 - 17 February 2024)
    - (12 February 2024) Did much work updating information pane, preparing for connection with NeMo backend, adding additional buttons needed.
        - Added button on right of map screen to reach homepage as requested by Maegan.
        - Added button on right of map screen to indicate audio source, currently only the button was created not the functionality of centering screen on audio source
        - Readded models.py and wrote code to check for NVIDIA GPU and log in console on start of webapp
        - Added function "transcribe()" within models.py and established a connection between map.js, currently function only provides result of the NVIDA GPU check.
        - Added additional subsection within information pane for transcription output when daytona beach airport.
        - Updated appearance of information pane.
        - Tested models.py NVIDIA GPU check with Darian since my laptop does not have NVIDIA GPU.
    - (13 February 2024) Discussed new information pane appearance with frontend group (Maegan and Taylor) in addition to backlog items and task assignment.
        - Discussed new information pane appearance with Maegan and Taylor.
        - Implemented new information pane appearance based on discussion.
        - Discussed and put in scrumwise backlog items for Spring Sprint 2.
        - Discussed with frontend group how we wish to divide backlog items.
        - Discussed removing approval needed for documentation repo to easier update engineering notebooks with Maegan.
    - (14 February 2024) Fixed Minor bugs.
        - Fixed Minor bug introduced with right buttons on map screen having rounded corners when unintended.
    - (15 February 2024) Worked with Tyler (Research Assistant) to get access on lab computer setup.
        - Worked with Tyler to get lab computer access setup.
        - Worked on updating engineering notebook.
        - Worked on updating UI further.
### Week 7 (18 February 2024 - 24 February 2024)
    - (20 February 2024)
        - Discovered OpenskyAPI major incorrect data, flight paths are outdated by several months and flights that currently appear live are indeed a few hours behind. This may make the flight route and communication feature impossible to be completed and highlighting active speaker from tower communications impossible as of now.
        - Discovered Bug/Undesired Behavior: Zoom out to highest level able to scroll to other worlds, Maximum zoom lock is needed.
        - Notified other frontend members need for right control panel panel icons such as Home (Homepage), Gear (settings), and Audio (Active audio) Icons.
        - Discussed and researched into color changing SVGs, determined that they can only be color changed via filter or manual image replacement.
        - Was able to sucessfully change hover icon for aircraft to temporary icon for testing but a solution for speaker and onclick coolor changing is needed.
    - (21 February 2024)
        - Presented project at EWeek in the Student Union for the EECS department along with Taylor Sumlin.
        - Discussed with Taylor Sumlin about previous day problems with opensky API and alternatives, said ADS-B Exchange antenna was viable and we should pursue based on what information they got back to him with.
        - Crude temporary demonstration of page darkening feature, currently unimplemented, to be worked on.
    - (22 February 2024)
        - 
