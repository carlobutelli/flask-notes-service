#!/usr/bin/env python3
import copy
from datetime import datetime
import uuid

from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from api.core.db_manager import db, get_db


class User(db.Model, UserMixin):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(36), nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=True, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)

    created_at = db.Column(db.DateTime, unique=False, nullable=False, index=True, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, unique=False, nullable=False, index=True, default=datetime.utcnow())
    deleted = db.Column(db.Boolean(), nullable=False, default=False)

    notes = db.relationship('Note')

    name_phone_index = db.Index('name_phone_index', name, phone)
    name_phone_email_index = db.Index('name_phone_email_index', name, phone, email)
    phone_email_index = db.Index('phone_email_index', phone, email)

    def get_id(self):
        return (self.uuid)

    def save(self) -> None:
        db_instance = get_db()
        db_instance.session.add(self)
        db_instance.session.commit()

    def delete(self):
        self.deleted = True
        self.save()

    def serializer(self, password: bool = False):
        attributes = copy.copy(self.__dict__)

        # Remove not needed attributes
        for attribute in ['_sa_instance_state', 'uuid']:
            attributes.pop(attribute, None)
        if not password:
            attributes.pop('password')

        admin_user = {
            'id': self.uuid,
            'attributes': attributes,
            'type': self.__class__.__name__
        }

        return admin_user

    @classmethod
    def deserialize(cls,
                    data: dict,
                    save: bool = False) -> 'User':
        """
        Deserialize a dictionary with format:
        {
            "name": "3f838cf7-4360-4847-8c83-7f53165bef4c",
            "phone": "2020-02-26T10:00:00",
            "email": "some@mail.com"
        }
        And create an session with it

        If you want to save the instance in the database then send the save option to True

        :param data: serialize dict with the data for the User object
        :type data: dict
        :param save: says if need to perform the save into the database
        :type save: bool
        :return: User instance
        """
        user = User(
            name=data.get("name"),
            phone=data.get("phone") or "-",
            email=data.get("email") or None,
            password=data.get('password')
        )

        if save:
            user.save()

        return user

    def update(self):
        self.updated_at = datetime.utcnow()
        self.save()

    # @classmethod
    # def update(cls, guid: str, data: dict):
    #     db = get_db()
    #     data['updated_at'] = datetime.utcnow()
    #     db.session.query(User).filter_by(uuid=guid).update(data)
    #     db.session.commit()

    def __repr__(self) -> str:
        return f"User>>> {self.uuid} {self.name} - {self.email}"
