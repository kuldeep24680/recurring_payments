from __future__ import absolute_import
import datetime
import logging

import bcrypt
from flask_login import UserMixin

from oracle import db
import mongoengine.signals as mongoengine_signals
from mongoengine import DateTimeField, StringField

from organisation.utils import generate_bcrypt_hash

logger = logging.getLogger(__name__)


def update_modified(sender, document, **kwargs):
    """
    Adds a modified date to the document
    :param sender: The sending class
    :param document: the instance document
    :param kwargs:
    :return:
    """
    document._ctl_modified = datetime.datetime.now()


class OracleDocumentABC(db.Document):
    """
    Base class for documents.
    All fields will begin with _ctl
    All properties will begin with ctl_
    """

    _ctl_modified = DateTimeField()
    created_at = DateTimeField()

    meta = {"abstract": True, "strict": False}

    @property
    def ctl_last_updated(self):
        return self._ctl_modified


def get_subclasses(cls):
    result = []
    classes_to_inspect = [cls]
    while classes_to_inspect:
        class_to_inspect = classes_to_inspect.pop()
        for subclass in class_to_inspect.__subclasses__():
            if subclass not in result:
                result.append(subclass)
                classes_to_inspect.append(subclass)
    return result


def attach_signal_to_all_subclasses():
    """'
    Search for all direct classes of the base document and attach the signal handlers
    """
    for subclass in get_subclasses(OracleDocumentABC):
        mongoengine_signals.pre_save.connect(update_modified, subclass)


class BaseUser(db.Document,UserMixin):
    email_id = StringField(unique=True)
    password = StringField(max_length=128)

    meta = {"abstract": True}

    def set_password(self, raw_password):
        """Sets the user's password - always use this rather than directly as the
        password is hashed before storage.
        """
        self.password = generate_bcrypt_hash(raw_password)

    def check_password(self, raw_password):
        """Checks the user's password against a provided password - always use
        this rather than directly comparing to
        :attr:`~mongoengine.django.auth.User.password` as the password is
        hashed before storage.
        """

        return str(self.password).encode() == bcrypt.hashpw(
            str(raw_password).encode("utf-8"), str(self.password).encode("utf-8")
        )

