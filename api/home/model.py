from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from api.core.db_manager import db, get_db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('user.uuid'))

    created_at = db.Column(db.DateTime, unique=False, nullable=False, index=True, default=func.now())
    updated_at = db.Column(db.DateTime, unique=False, nullable=False, index=True, default=func.now())

    @classmethod
    def deserialize(cls, data: dict, save: bool = False) -> 'Note':
        """
        Deserialize a dictionary with format:
        {
            "data": "something written in the new note",
            "user_uuid": "3f838cf7-4360-4847-8c83-7f53165bef4c"
        }
        And create an session with it

        If you want to save the instance in the database then send the save option to True

        :param data: serialize dict with the data for the Note object
        :type data: dict
        :param save: says if need to perform the save into the database
        :type save: bool
        :return: User instance
        """
        note = Note(
            data=data.get("note"),
            user_uuid=data.get("user_uuid")
        )

        if save:
            note.save()

        return note

    def save(self) -> None:
        db_instance = get_db()
        db_instance.session.add(self)
        db_instance.session.commit()

    def update(self):
        self.updated_at = func.now()
        self.save()

    def delete(self) -> None:
        db_instance = get_db()
        db_instance.session.delete(self)
        db_instance.session.commit()

    def __repr__(self) -> str:
        return f"Note>>> {self.id} {self.data} - {self.date}"

