from datetime import datetime
import uuid


class Review:

    def __init__(self, user_id, recipient_id, rating, comment=None):

        self.id = uuid.uuid4()
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.comment = comment
        self.rating = rating
        self.user_id = user_id
        self.recipient_id = recipient_id

