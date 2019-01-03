import logging

from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError

__author__ = 'ahmetdal'

LOGGER = logging.getLogger(__name__)


class RiverApp(AppConfig):
    name = 'river'
    label = 'river'

    def ready(self):

        from river.hooking.backends.database import DatabaseHookingBackend
        from river.hooking.backends.loader import callback_backend
        from river.models.fields.state import workflow_registry

        for field_name in workflow_registry.workflows:
            transition_approval_meta = self.get_model('TransitionApprovalMeta').objects.filter(field_name=field_name)
            if transition_approval_meta.count() == 0:
                LOGGER.warning("%s field doesn't seem have any transition approval meta in database" % field_name)

        if isinstance(callback_backend, DatabaseHookingBackend):
            try:
                self.get_model('Callback').objects.exists()
                callback_backend.initialize_callbacks()
            except (OperationalError, ProgrammingError):
                LOGGER.debug('Database hookings are not registered. Because database is not created yet.')
        LOGGER.debug('RiverApp is loaded.')
