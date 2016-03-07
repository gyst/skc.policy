from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class SkcpolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import skc.policy
        xmlconfig.file(
            'configure.zcml',
            skc.policy,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'skc.policy:default')

SKC_POLICY_FIXTURE = SkcpolicyLayer()
SKC_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SKC_POLICY_FIXTURE,),
    name="SkcpolicyLayer:Integration"
)
SKC_POLICY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SKC_POLICY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="SkcpolicyLayer:Functional"
)
