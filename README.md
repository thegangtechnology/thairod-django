# thairod-django

## Documentation

Run server then access url below

```
http://localhost:8000/docs/open_api/
http://localhost:8000/docs/redoc/
http://tg.localhost:8000/docs/open_api.yaml
http://tg.localhost:8000/docs/open_api.json
```

## Development

Some of the functionality requires celery to run in background. For this you need

```
brew services start rabbitmq
celery -A thairod worker
```

For testing you don't really need rabbitmq. 
It will spawn a new thread with a worker and  in memory que for you.

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
   SHIPPOP_EMAIL="xxxx@yyyy.com"
   
   TELEMED_WHITELIST="127.0.0.1"
   LINE_CHANNEL_ACCESS_TOKEN=""
   
   CELERY_BROKER_URL="ampq://localhost"
   CELERY_RESULT_BACKEND="rpc"
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

AddressData()  # You need this to create order

ParcelData()  # You need this to create order

OrderLineData()  # You need this to create order

OrderData()  # You need this to create order

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

# Get pricelist - befo
# re create order you need to choose 1 courier code
shippop_api.get_pricing(OrderData)

# Get label - Shippop HTML Label generated
shippop_api.print_label(purchase_id)

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

# Print label - Shippop HTML Label generated
shippop_api.get_label(purchase_id)

# Print multiple label
# tracking_code is list of tracking code
shippop_api.print_multiple_labels(tracking_codes)
```

```
=======
## Print Label
To test print label we can't just use the seed. We have provided a method
```python
from thairod.utils.load_seed import load_meaningful_seed
load_meaningful_seed()
```

to populate the data base with data consistent with shippop side.

http://localhost:8000/shipment/printlabel?shipments=1&shipment=2

## Deployment

### Docker Run

```bash
# with .env
docker run -d -p 8000:8000 --env-file ./.env  [DOCKER_IMAGE_URL]:latest

# with variable
docker run -d -p 8000:8000 
  --env DJANGO_SETTINGS_MODULE="./thairod/environments/develop" 
  --env DB_URL="postgres://postgres:postgres@127.0.0.1:5432/thairod"
  --env SHIPPOP_API_KEY="key"
  --env SHIPPOP_URL="url"
  --env SHIPPOP_DEFAULT_COURIER_CODE="SPE"  
  [DOCKER_IMAGE_URL]:latest
