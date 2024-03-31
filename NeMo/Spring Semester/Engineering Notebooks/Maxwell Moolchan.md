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
### Week 8 (25 February 2024 - 2 March 2024)
    - (26 February 2024)
        - Fixed bugged brightness slider with dragging events
    - (27 February 2024)
        - Discussed who will be available for Discovery Day Presentation
    - (28 February 2024)
        - Edited right control buttons to have images instead of letters to be more user friendly
        - Started Adding append transcription message function and formatting how messages will look in the transcription output box
    - (29 February 2024)
        - Reactivated models file and added check for NVIDIA GPU needed to run NeMo models
        - modified css files to be cleaner
        - Updated right icons from Taylor as previously not centered.
### Week 9 (3 March 2024 - 9 March 2024)
    - (5 March 2024)
        - Spent nearly the entire class time working to fixed messed up CSS files from merge issues from previously incorrectly merged work.
    - (6 March 2024)
        - worked on sprint 2 presentation slides, worked on front end slides about new features and UI changes.
    - (7 March 2024)
        - finalized sprint 2 presentation slides, updated future development slides.
        - Sprint 2 Presentation
        - Started work on settings pane toggle setting sliders.
### Week 10 (10 March 2024 - 16 March 2024)
    - Spring Break
### Week 11 (17 March 2024 - 23 March 2024)
    - (18 March 2024)
        - Worked with aaron over discord to resolve/figure out github pages issues, more work needs to be done on updating internal documentation but should now know how to do so.
    - (19 March 2024)
        - Boeing Presentation in class.
    - (21 March 2024)
        - Worked with Tyler on further setting up and learning how to utilize computer in LB370 to get NeMo working.
            - Able to SSH into computer from my own laptop.
            - Successfully ran application as-is (without NeMo) running on computer
            - covered some of the previous files written by Aaron, previous years group, etc.
            - Updated github and github pages documentation as needed.
### Week 12 (24 March 2024 - 30 March 2024)
    - (26 March 2024)
        - Taylor provided smaller icons for webapp, need to be uploaded.
        - Had to temporarily switch to live atc feed for testing because Near Aero seems to not be working correctly for me.
        - Worked on getting transcription working in terminal with Tyler
    - (28 March 2024)
        - Discussed with Tyler transcription output to website, future hosting, future mobile design, & working on webapp over summer break for Dr. Liu
        - Spent class time helping Darian learn and utilize XMLHTTP request to get form input to backend.
    - (29 March 2024)
        - Started Setup of Flask-SocketIO to make live transcription output to website feasible.
        - Setup basic events for Flask-SocketIO such as connect, disconnect, sending stream URL, etc.
    - (30 March 2024)
        - Got NeMo transcription Output to website.
        - Running NeMo transcription as seperate process does not work as intended presumably because of GPU locking issues.
        - Rewrote code to work without starting other process for NeMo transcription and eliminate stopping NeMo trancription by killing process, ie killing the whole webapp.
        - NeMo transcription now occours and is returned on a per client basis, ie only the transcription you started is now displayed.
        - Need to work on following issues:
            - When client is closed without manually stopping transcription the transcription continues to run and consume resources.
