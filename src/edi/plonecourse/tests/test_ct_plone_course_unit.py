# -*- coding: utf-8 -*-
from edi.plonecourse.content.plone_course_unit import IPloneCourseUnit  # NOQA E501
from edi.plonecourse.testing import EDI_PLONECOURSE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class PloneCourseUnitIntegrationTest(unittest.TestCase):

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

    def test_ct_plone_course_unit_schema(self):
        fti = queryUtility(IDexterityFTI, name='PloneCourseUnit')
        schema = fti.lookupSchema()
        self.assertEqual(IPloneCourseUnit, schema)

    def test_ct_plone_course_unit_fti(self):
        fti = queryUtility(IDexterityFTI, name='PloneCourseUnit')
        self.assertTrue(fti)

    def test_ct_plone_course_unit_factory(self):
        fti = queryUtility(IDexterityFTI, name='PloneCourseUnit')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPloneCourseUnit.providedBy(obj),
            u'IPloneCourseUnit not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_plone_course_unit_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='PloneCourseUnit',
            id='plone_course_unit',
        )

        self.assertTrue(
            IPloneCourseUnit.providedBy(obj),
            u'IPloneCourseUnit not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('plone_course_unit', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('plone_course_unit', parent.objectIds())

    def test_ct_plone_course_unit_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PloneCourseUnit')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )

    def test_ct_plone_course_unit_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PloneCourseUnit')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'plone_course_unit_id',
            title='PloneCourseUnit container',
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
