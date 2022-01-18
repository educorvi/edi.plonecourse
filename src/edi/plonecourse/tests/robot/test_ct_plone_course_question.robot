# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.plonecourse -t test_plone_course_question.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.plonecourse.testing.EDI_PLONECOURSE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/plonecourse/tests/robot/test_plone_course_question.robot
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

Scenario: As a site administrator I can add a PloneCourseQuestion
  Given a logged-in site administrator
    and an add PloneCourse form
   When I type 'My PloneCourseQuestion' into the title field
    and I submit the form
   Then a PloneCourseQuestion with the title 'My PloneCourseQuestion' has been created

Scenario: As a site administrator I can view a PloneCourseQuestion
  Given a logged-in site administrator
    and a PloneCourseQuestion 'My PloneCourseQuestion'
   When I go to the PloneCourseQuestion view
   Then I can see the PloneCourseQuestion title 'My PloneCourseQuestion'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add PloneCourse form
  Go To  ${PLONE_URL}/++add++PloneCourse

a PloneCourseQuestion 'My PloneCourseQuestion'
  Create content  type=PloneCourse  id=my-plone_course_question  title=My PloneCourseQuestion

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the PloneCourseQuestion view
  Go To  ${PLONE_URL}/my-plone_course_question
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a PloneCourseQuestion with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the PloneCourseQuestion title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
