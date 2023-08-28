from rest_framework_simplejwt.token_blacklist.models import OutstandingToken , BlacklistedToken
import datetime

def refresh_token_delete():
    date =  datetime.date.today()
    print(date)
    # token = BlacklistedToken.objects.filter(expires_at = userid).delete()