from application.publicwork.models.publicwork import PublicWork
from pydantic import BaseModel


class QueueItem(BaseModel):
    public_work: PublicWork
    public_work_count: str
    collect_count: str
    photo_count: str
