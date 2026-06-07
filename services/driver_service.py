from apps.drivers.models import Driver
class DriverService:
    @staticmethod
    def list_for_vendor(vendor):
        return Driver.objects.filter(vendor=vendor, is_active=True)
