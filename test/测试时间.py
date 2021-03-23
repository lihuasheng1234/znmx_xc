import datetime
import settings

now = datetime.datetime.now()
print(type(now + datetime.timedelta(milliseconds=settings.TOOLHEALTH_COMPUTE_BLANKING_TIME)))
