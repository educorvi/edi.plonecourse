# -*- coding: utf-8 -*-
from edi.plonecourse.content.plone_course_question import IPloneCourseQuestion  # NOQA E501
from edi.plonecourse.testing import EDI_PLONECOURSE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class PloneCourseQuestionIntegrationTest(unittest.TestCase):

    layer = EDI_PLONECOURSE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'PloneCourse',
            self.portal,
            'parent_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_plone_course_question_schema(self):
        fti = queryUtility(IDexterityFTI, name='PloneCourseQuestion')
        schema = fti.lookupSchema()
        self.assertEqual(IPloneCourseQuestion, schema)

    def test_ct_plone_course_question_fti(self):
        fti = queryUtility(IDexterityFTI, name='PloneCourseQuestion')
        self.assertTrue(fti)

    def test_ct_plone_course_question_factory(self):
        fti = queryUtility(IDexterityFTI, name='PloneCourseQuestion')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPloneCourseQuestion.providedBy(obj),
            u'IPloneCourseQuestion not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_plone_course_question_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='PloneCourseQuestion',
            id='plone_course_question',
        )

        self.assertTrue(
            IPloneCourseQuestion.providedBy(obj),
            u'IPloneCourseQuestion not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('plone_course_question', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('plone_course_question', parent.objectIds())

    def test_ct_plone_course_question_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PloneCourseQuestion')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )

    def test_ct_plone_course_question_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PloneCourseQuestion')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'plone_course_question_id',
            title='PloneCourseQuestion container',
         )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
