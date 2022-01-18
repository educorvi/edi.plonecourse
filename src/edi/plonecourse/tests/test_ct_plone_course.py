# -*- coding: utf-8 -*-
from edi.plonecourse.content.plone_course import IPloneCourse  # NOQA E501
from edi.plonecourse.testing import EDI_PLONECOURSE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class PloneCourseIntegrationTest(unittest.TestCase):

    layer = EDI_PLONECOURSE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_plone_course_schema(self):
        fti = queryUtility(IDexterityFTI, name='PloneCourse')
        schema = fti.lookupSchema()
        self.assertEqual(IPloneCourse, schema)

    def test_ct_plone_course_fti(self):
        fti = queryUtility(IDexterityFTI, name='PloneCourse')
        self.assertTrue(fti)

    def test_ct_plone_course_factory(self):
        fti = queryUtility(IDexterityFTI, name='PloneCourse')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPloneCourse.providedBy(obj),
            u'IPloneCourse not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_plone_course_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='PloneCourse',
            id='plone_course',
        )

        self.assertTrue(
            IPloneCourse.providedBy(obj),
            u'IPloneCourse not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('plone_course', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('plone_course', parent.objectIds())

    def test_ct_plone_course_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PloneCourse')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_plone_course_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PloneCourse')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'plone_course_id',
            title='PloneCourse container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
