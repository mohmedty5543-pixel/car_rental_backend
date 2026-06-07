# Architecture

## Clean / Modular Monolith
- `apps/*` — bounded contexts (users, vendors, vehicles, bookings, payments, deliveries, reviews, drivers)
- `services/*` — pure business logic (transaction-safe, framework-light)
- `api/*` — DRF viewsets, routers, schema
- `core/*` — shared base models, permissions, pagination, exceptions
- `config/settings/{base,dev,prod}.py` — layered settings

## Domain rules
- UUID PKs everywhere
- Individual vendor: `owner_user` required, no members
- Company vendor: members via `VendorMember`
- Booking overlap detection at availability service
- One review per completed booking
- Multiple payments per booking
- Optional driver assignment per booking
