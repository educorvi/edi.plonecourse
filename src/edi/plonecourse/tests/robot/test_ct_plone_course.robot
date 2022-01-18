# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.plonecourse -t test_plone_course.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.plonecourse.testing.EDI_PLONECOURSE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/plonecourse/tests/robot/test_plone_course.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a PloneCourse
  Given a logged-in site administrator
    and an add PloneCourse form
   When I type 'My PloneCourse' into the title field
    and I submit the form
   Then a PloneCourse with the title 'My PloneCourse' has been created

Scenario: As a site administrator I can view a PloneCourse
  Given a logged-in site administrator
    and a PloneCourse 'My PloneCourse'
   When I go to the PloneCourse view
   Then I can see the PloneCourse title 'My PloneCourse'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add PloneCourse form
  Go To  ${PLONE_URL}/++add++PloneCourse

a PloneCourse 'My PloneCourse'
  Create content  type=PloneCourse  id=my-plone_course  title=My PloneCourse

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the PloneCourse view
  Go To  ${PLONE_URL}/my-plone_course
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a PloneCourse with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the PloneCourse title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
