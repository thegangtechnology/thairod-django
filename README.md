# thairod-django

## Documentation
Run server then access url below
```
http://localhost:8000/docs/open_api/
http://localhost:8000/docs/redoc/
http://tg.localhost:8000/docs/open_api.yaml
http://tg.localhost:8000/docs/open_api.json
```




## Getting Started

### Installation

1. Have Postgres running on your machine (or docker)
2. Setup your python environment with env (recommend: pipenv). Read more at https://pipenv.pypa.io/en/latest/install/
3. in `thairod` folder, create `.env` file with 
   ```
   DB_URL="postgres://user:secret@localhost:5432/dbname"
   ```
   or
   ```
   DB_HOST="dbhost"
   DB_NAME="dbname"
   DB_USER="dbuser"
   DB_PASSWORD="password"
   SHIPPOP_API_KEY="key"
   SHIPPOP_URL="https://mkpservice.shippop.dev"
   SHIPPOP_DEFAULT_COURIER_CODE="SPE"
   ```
   *Make sure to have database connection with your specified user.
4. Run migration files
   ```sh
   python manage.py migrate
   ```
5. Run the application 
   ```
   python manage.py runserver
   ```
   
## Shippop Usage

### Dataclass
```python
from thairod.services.shippop.data import *


# Note: For better understanding of each classes, please read the code 

AddressData() # You need this to create order

ParcelData() # You need this to create order

OrderLineData() # You need this to create order

OrderData() # You need this to create order

OrderLineResponse()

OrderResponse()

TrackingState()

TrackingData()

Pricing()
```

### Service

```python
from thairod.services.shippop.api import ShippopAPI

shippop_api = ShippopAPI()

# Step 1 - create order
shippop_api.create_order(OrderData)

# Step 2 - Confirm order
shippop_api.confirm_order(purchase_id)

# Get order detail - after create order
shippop_api.get_order_detail(purchase_id)

# Get tracking data - after confirm order
shippop_api.get_tracking_data(tracking_code)

# Get pricelist - before create order you need to choose 1 courier code
shippop_api.get_pricing(OrderData)

# Get label - Shippop HTML Label generated
shippop_api.print_label(purchase_id)

#Step 1 - create order
shippop_api.create_order(OrderData)

#Step 2 - Confirm order
shippop_api.confirm_order(purchase_id)

#Get order detail - after create order
shippop_api.get_order_detail(purchase_id)

#Get tracking data - after confirm order
shippop_api.get_tracking_data(tracking_code)

#Get pricelist - before create order you need to choose 1 courier code
shippop_api.get_pricing(OrderData)

#Get label - Shippop HTML Label generated
shippop_api.get_label(purchase_id)
```