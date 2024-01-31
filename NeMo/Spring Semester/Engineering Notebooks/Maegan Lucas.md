# Engineering Notebook - Maegan Lucas

## Semester Two - Spring 2024
### Week One (Jan. 10 - Jan. 14)
  - Talked amongst group about reassigning roles within the group
  - Expressed desire to work on front-end development
  - Was reassigned to front end tasks

### Week Two (Jan. 15 - Jan. 21)
  <i> Was absent due to illness Jan. 16 - Communicated remotely </i>
  - Created a cheat sheet for the database development done last semester to help Darian and Adam
  - Presented poster on project at the Student Poster Session at the Boeing Center of Aviation Safety
  - Shared knowledge on previous database development with Darian
  - Emailed OpenSky to inquire about API maintence
  - Concurred with group that it will probably be best to look into other APIs
  - Uploaded updated project vision to GitHub

    <strong>BLOCKER(S):</strong>
    OpenSky API down for maintence which can run for months intermittantly. After emailing, they said that it can go down at anytime. We are looking into other API's such as Flight Radar.

### Week Three (Jan. 22 - Jan. 28)
  - Determined that I will be doing tasks:
    - Riddle Aesthetic Colors (Changing the color scheme of the website to match Embry-Riddle colors)
    - Contact Us Page (Creating a contact page)
    - About Us Page (Updating About page to most up-to-date information)
    - Homepage Rounded Buttons (Round the square buttons on the homepage for design consistency)
  - Continued talks with team about alternative APIs
  - Created merge request [#5](https://github.com/TheCreepOfWar/asr-webapp/pull/5) (Update color scheme)
  - Started initial changes to About page
  - Reviewed pull requests [#6](https://github.com/TheCreepOfWar/asr-webapp/pull/6) (Background image fix) and [#7](https://github.com/TheCreepOfWar/asr-webapp/pull/7) (Map Zoom fix)
  - Merged pull requests [#5](https://github.com/TheCreepOfWar/asr-webapp/pull/5) (Update color scheme) and [#6](https://github.com/TheCreepOfWar/asr-webapp/pull/6) (Background image fix)

  - Updated the template and home page with the following changes:
    - Make header title bigger and moved the location down to the bottom of the header
    - Removed unnecessary "Site Map" link from footer
    - Changed footer links to match Embry-Riddle colors
    - Changed layout of footer links
    - Changed color gradient of header and footer bar to be lighter
    - Removed unnecessary "Details" from footer bar in template
    - Changed color of "Load Maps" button to navy blue to match Embry-Riddle color scheme
    - Rounded corners of "Load Maps" button to match map toggle roundness for design consistency
    - Fixed some spelling/capitalization errors
    - Changed fonts from Arial, Helvetica to Arial for design consistency with Embry-Riddle scheme

      <strong>Initial Template:</strong>
      ![old_1](https://github.com/maeganlucas/CS490-ATC/assets/92832062/c00446e3-a9e1-4c2d-8522-d429caf2a1a1)
      ![old_2](https://github.com/maeganlucas/CS490-ATC/assets/92832062/e1866676-aa6a-449e-8257-8e807244689f)

      <strong>Template Revision 1:</strong>
      ![rev1_1](https://github.com/maeganlucas/CS490-ATC/assets/92832062/3f832455-7f2f-4b02-9689-a4d5dfe9d73f)
      ![rev1_2](https://github.com/maeganlucas/CS490-ATC/assets/92832062/0064dd96-c786-400a-b59e-e1f1ea0204bc)

      #### <strong><i>Bug Introduced</i></strong><br>
      <i>Bug Name (for identification purposes):</i> White Box Bug
      <br><i>Description:</i> By removing the unnecessary "Details" from the footer bar, it has introduced an issue that the navy footer does not expand fully to the bottom of the screen on screens of different size or zoom levels.
      ![bug1](https://github.com/maeganlucas/CS490-ATC/assets/92832062/405994f7-5eac-4bd4-a497-7cf5034e10ba)
      <br><i>Status:</i> In Progress

      &emsp;<strong><i>Bug Revision 1:</i></strong><br>
      &emsp;<i>Description:</i> Changed the height of the lower footer block to be 100% of the viewport height.<br>
      &emsp;<i>Problems/Notes:</i> Adds extra length to the website that would normally not be seen. Not the biggest fan and will try to find a<br>
      &emsp;better solution.
      ![bug1_rev1](https://github.com/maeganlucas/CS490-ATC/assets/92832062/3d5a37f6-e761-4324-855b-a26a574c4afd)

### Week Four (Jan. 29 - Feb. 3)
  <i><strong>White Box Bug</strong> still remains</i>
  - Merged pull request [#7](https://github.com/TheCreepOfWar/asr-webapp/pull/7) (Map Zoom Fix)
  - Created pull request [#8](https://github.com/TheCreepOfWar/asr-webapp/pull/8) (About Page
  - Merged pull request [#8](https://github.com/TheCreepOfWar/asr-webapp/pull/8) (About Page)
  - Reviewed pull request [#9](https://github.com/TheCreepOfWar/asr-webapp/pull/9) (Zoom button changes)
  - Created pull request [#10](https://github.com/TheCreepOfWar/asr-webapp/pull/10) (Changing Schneider's blurb slightly)
  - Updated the About page with the following updates:
    - Changed text to navy font
    - Changed size of header setting 1
    - Added new description of application
    - Updated application instructions
    - Updated both team descriptions
    - Added team member names to team sections
    - Added blurbs to professor sections
    - Update section about Aaron's work

    <strong>Initial About Page:</strong>
    ![about1](https://github.com/maeganlucas/CS490-ATC/assets/92832062/c40bf6e4-0451-41c8-8742-eab0f07169f9)
    ![about2](https://github.com/maeganlucas/CS490-ATC/assets/92832062/23a08560-540e-4a55-b566-c47ec108b371)

    <strong>About Page Revision 1:</strong>
    ![about_rev1_1](https://github.com/maeganlucas/CS490-ATC/assets/92832062/eedbae2c-daa7-4dd1-9134-ed9d654ecff0)
    ![about_rev1_2](https://github.com/maeganlucas/CS490-ATC/assets/92832062/2ca637d5-4f73-4219-b70d-562a7a2dae5f)
    
  - Created the initial Contact page with the following steps:
    - Created new HTML page, `contact.html`
      - Uses the template layout from `template.html`
      - Added a <i>Contact Us</i> header
      - Added a message to the page about contacting the team
      - Added Dr. Liu's contact information
    - Created a blueprint to render the Contact template, contact.py
    - Imported the Contact blueprint to `__init__.py`. Specific line:
      ```python
      from .blueprints import index, about, map, data, models, replay, site_map, contact
      ```
    - Registered the Contact blueprint in `__init__.py`. Specific line:
      ```python
      app.register_blueprint(contact.bp)
      ```
    - Modified the template layout to include a link to the Contact page. Specific line:
      ```html
      <li><a class="navy-font" href="{{ url_for('contact.contact') }}">Contact</a></li>
      ```
    <strong>Initial Contact Page:</strong>
    ![contact1](https://github.com/maeganlucas/CS490-ATC/assets/92832062/3126d317-62e8-41cb-b365-eaa36e4837ad)
    <i>Note: This initial contact page has residual effects of the White Box Bug.</i>
    <br><br>
    <strong>Template Revision 2:</strong>
    ![rev2](https://github.com/maeganlucas/CS490-ATC/assets/92832062/7bc2f0c7-2c88-42b2-9105-1e58d35b758f)

  - Updated Andrew Schneider's blurb on the About page to include "Embry-Riddle Aeronautical University" instead of just "College of Aviation"
    
    <strong>About Page Revision 2:</strong>
    ![about_rev2](https://github.com/maeganlucas/CS490-ATC/assets/92832062/df327ef7-f327-4cf1-9b0b-ea4e5e9359cc)

    <strong><i>Bug Resolved</i></strong><br>
      <i>Bug Name (for identification purposes):</i> [White Box Bug](#bug-introduced)
      <br><i>Description:</i> By removing the unnecessary "Details" from the footer bar, it has introduced an issue that the navy footer does not expand fully to the bottom of the screen on screens of different size or zoom levels.
      <br><i>Status:</i> Finished

      &emsp;<strong><i>Bug Revision 2:</i></strong><br>
      &emsp;<i>Description:</i> Removed height change of 100 viewport height and set a minimum height of 200px. Set the background color of HTML <br>
      &emsp;to be Embry-Riddle Navy to match footer, so when a different screen size is encountered, or a zoom-out occurs, the HTML <br> 
      &emsp;background blends seamlessly with the footer creating the illusion that the footer is expanding to fill the screen without adding extra <br>
      &emsp;length.
      ![bug1_rev2](https://github.com/maeganlucas/CS490-ATC/assets/92832062/9b285806-8198-4580-866b-123e202f37c7)
