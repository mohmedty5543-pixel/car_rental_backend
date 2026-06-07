# ERD (textual)

```
User (id, email, role, ...)
  1---* Booking
  1---* Review
  1---* FavoriteVehicle
  1---* Notification
  1---* VendorMember
  1---0..1 Vendor (as owner, INDIVIDUAL)

Vendor (id, type, owner_user_id?, ...)
  1---* Vehicle
  1---* Driver
  1---* VendorMember   (COMPANY only)

Vehicle (id, vendor_id, ...)
  1---* VehicleImage
  1---* VehicleAvailability
  1---* Booking
  1---* FavoriteVehicle

Booking (id, user_id, vehicle_id, driver_id?, ...)
  1---* Payment
  1---0..1 Delivery
  1---0..1 Review

Driver (id, vendor_id) 0..1---* Booking
```
