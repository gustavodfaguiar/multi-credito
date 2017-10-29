# Multi-Credit Card Challenge

## Requirements
* Python 3.5

## Development

### Installation

```
git clone https://github.com/gusttavoaguiarr/multi-credito multi-credito
cd multi-credito
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp contrib/env-sample .env
```

### Run application
```
make run
```

### Run Flake8
```
make flake8
```

### Run tests
```
make test
```

### Run coverage
```
make coverage
```

### API Endpoints

#### Parameters Headers
```
Authorization: Basic Z3VzdGF2b0BnbWFpbC5jb206MTIzNDU2
Content-Type: application/json
x-access-token:
```

GET /api/v1/login - Sign in
```
{
    token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo"
}
```

POST /api/v1/user - Create user
```
{
    "email": "user@gmail.com",
    "name": "User name",
    "password": "123456"
}
```

#### Requires authentication

GET /api/v1/user - Get user
```
{
    "user": {
        "email": "user@gmail.com",
        "id": 1,
        "name": "User name"
    }
}
```

POST /api/v1/card - Create card
```
{
    "number": 5165834017429286,
    "expiration_date": "2019-07-5",
    "validity_date": "2017-05-05",
    "cvv": 408,
    "limit": 2000
}
```

GET /api/v1/card/< int: card_id > - Get one card
```
{
    "card": {
        "credit": 2000,
        "cvv": "408",
        "expiration_date": "Fri, 05 Jul 2019 00:00:00 GMT",
        "id": 1,
        "limit": 2000,
        "name": "USER NAME",
        "number": 5165834017429286,
        "validity_date": "Fri, 05 May 2017 00:00:00 GMT",
        "wallet_id": 1
    }
}
```

GET /api/v1/cards - Get all card
```
{
    "cards": [
        {
            "credit": 2000,
            "cvv": "408",
            "expiration_date": "Fri, 05 Jul 2019 00:00:00 GMT",
            "id": 2,
            "limit": 2000,
            "name": "USER NAME",
            "number": 5165834017429286,
            "validity_date": "Fri, 05 May 2017 00:00:00 GMT",
            "wallet_id": 2
        }
    ]
}
```

PUT /api/v1/card/pay/< int: card_id > - Pay card
```
{
   "value_pay": 200
}
```

DELETE /api/v1/card/< int: card_id > - Delete card


GET /api/v1/wallet - Get Wallet
```
{
    "wallet": {
        "available_credit": 0,
        "id": 1,
        "max_limit": 0,
        "user_id": 1,
        "user_limit": 0
    }
}
```

PUT /api/v1/wallet - Update limit user
```
{
    "user_limit": 1000
}
```

PUT /api/v1/wallet/buy - Make purchase
```
{
    "value": 1000
}
```
