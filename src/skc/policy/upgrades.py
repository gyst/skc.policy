import logging
import transaction
from plone import api
from plone.browserlayer.utils import unregister_layer

log = logging.getLogger(__name__)

REMOVE_PRODUCTS = [
    'Products.ContentWellPortlets',
    'collective.improvedbyline',
    'sc.social.like',
    'collective.quickupload',
    'collective.smartkeywordmanager',
    'eea.tags',
    'eea.jquery',
    'collective.js.jqueryui',
    'collective.doormat',
    'collective.opengraph',
    'collective.cover',
    'collective.contentleadimage',
    'sc.contentrules.groupbydate',
    'plone.app.blocks',
]

REMOVE_CONTENT = {
    'collective.cover': 'collective.cover.content',
}


def plone4_cleanup(context):
    """Trigger all the uninstallers for to-be-removed products."""
    portal = api.portal.get()
    qi_tool = api.portal.get_tool('portal_quickinstaller')

    # first, make sure all our new un-installers are installed :-)
    installed = [p['id'] for p in qi_tool.listInstalledProducts()]
    reinstall = [p for p in REMOVE_PRODUCTS if p not in installed]
    for p in reinstall:
        log.info("Reinstalling first: %s", p)
        qi_tool.installProducts([p])

    # nuke content that we will not support after upgrade
    catalog = api.portal.get_tool('portal_catalog')
    for (p, ctype) in REMOVE_CONTENT.items():
        if p not in REMOVE_PRODUCTS:
            continue
        log.info("Removing content: %s", p)
        for brain in catalog(portal_type=ctype):
            api.content.delete(brain.getObject())

    # sjeez TTW persistent interface references
    pvc = portal.portal_view_customizations
    log.info("Removing portal_view_customizations TTW cruft")
    pvc.manage_delObjects(pvc.objectIds())

    # remove all the unwanted cruft packages themselves
    for p in REMOVE_PRODUCTS:
        log.info("Uninstalling: %s", p)
        qi_tool.uninstallProducts([p])

    # clear the archetypes reference catalog
    log.info("Clearing reference catalog")
    portal.reference_catalog.manage_catalogClear()

    # migrate to plone.app.contenttypes
    log.info("Enabling plone.app.contenttypes")
    qi_tool.installProducts(['plone.app.contenttypes'])

    log.info("Committing changes.")
    transaction.commit()
