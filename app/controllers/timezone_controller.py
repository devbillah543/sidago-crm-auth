from sqlalchemy.orm import Session
from app.models.timezone import Timezone

class TimezoneController:
    @staticmethod
    def get_all_timezones(db: Session):
        """
        Returns all timezones.
        """
        timezones = db.query(Timezone).all()
        return [
            {
                "id": tz.id,
                "label": tz.label
            }
            for tz in timezones
        ]
