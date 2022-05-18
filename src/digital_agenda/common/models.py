from model_utils.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    class Meta:
        abstract = True
