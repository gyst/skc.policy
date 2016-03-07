import logging
import transaction
from plone import api

log = logging.getLogger(__name__)

REMOVE_PRODUCTS = [
    'Products.ContentWellPortlets',
    'collective.improvedbyline',
    'sc.social.like',
    'collective.quickupload',
    'collective.smartkeywordmanager',
    'eea.tags',
    'eea.jquery',
    'collective.doormat',
    'collective.opengraph',
    'collective.cover',
]

REMOVE_CONTENT = {
    'collective.cover': 'collective.cover.content',
}


def plone4_cleanup(context):
    """Trigger all the uninstallers for to-be-removed products."""
    qi_tool = api.portal.get_tool('portal_quickinstaller')
    installed = [p['id'] for p in qi_tool.listInstalledProducts()]

    reinstall = [p for p in REMOVE_PRODUCTS if p not in installed]
    for p in reinstall:
        log.info("Reinstalling first: %s", p)
        qi_tool.installProducts([p])

    catalog = api.portal.get_tool('portal_catalog')
    for p in REMOVE_PRODUCTS:

        if p in REMOVE_CONTENT:
            log.info("Removing content: %s", p)
            for brain in catalog(portal_type=REMOVE_CONTENT[p]):
                api.content.delete(brain.getObject())

        log.info("Uninstalling: %s", p)
        qi_tool.uninstallProducts([p])

    transaction.commit()
