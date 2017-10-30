[![Build Status](https://travis-ci.org/gusttavoaguiarr/multi-credito.svg?branch=master)](https://travis-ci.org/gusttavoaguiarr/multi-credito)       [![codecov](https://codecov.io/gh/gusttavoaguiarr/multi-credito/branch/master/graph/badge.svg)](https://codecov.io/gh/gusttavoaguiarr/multi-credito)

# Multi-Credit Card Challenge

## Requirements
* Python 3.5
* SQLite

## Development

### Installation

```
git clone https://github.com/gusttavoaguiarr/multi-credito multi-credito
cd multi-credito
source setup.sh
```

### Run application
```
make run
```

Access: http://localhost:5000/api/v1/login

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

**To begin, it is necessary to register the information in the header**

```
Content-Type: application/json
```

### Create
POST /api/v1/user

To create User, do a `post` HTTP request in `/api/v1/user` endpoint

**Register a user so you can login**

```
{
    "email": "user@gmail.com",
    "name": "User name",
    "password": "123456"
}
```

GET /api/v1/login

To access the other routes, you must login, done that a token will be generated and this token must be added to the header

```
{
    "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE1MDk0MTczNDZ9.BbgOxJSVYEyRx1BnE8-3v8G7LmBufAL-bc-10lY9yco"
}
```

#### Requires authentication

All endpoints are now protected and you must inform in header `x-access-token` header the token. to get token see `/api/v1/login` endpoint

### READ
GET /api/v1/user

To read User, do a `get` HTTP request in `/api/v1/user` endpoint

```
{
    "user": {
        "email": "user@gmail.com",
        "id": 1,
        "name": "User name"
    }
}
```
## Endpoints Card

### CREATE
POST /api/v1/card

To create Card, do a `post` HTTP request in `/api/v1/card` endpoint

```
{
    "number": 5165834017429286,
    "expiration_date": "2019-07-5",
    "validity_date": "2017-05-05",
    "cvv": 408,
    "limit": 2000
}
```

### READ
GET /api/v1/card/< int: card_id >

To read Card, do a `get` HTTP request in `/api/v1/card/< int: card_id >` endpoint

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

### READ
GET /api/v1/cards

To read all cards, do a `get` HTTP request in `/api/v1/cards` endpoint

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

### UPDATE
PUT /api/v1/card/pay/< int: card_id >

To make the payment of the card, do a `put` HTTP request in `/api/v1/card/pay/< int: card_id >` endpoint

```
{
   "value_pay": 200
}
```

### DELETE
DELETE /api/v1/card/< int: card_id >

To delete a card, do a `delete` HTTP request in `/api/v1/card/< int: card_id >` endpoint

## Endpoints Wallet

### READ
GET /api/v1/wallet

To read a wallet, do a `get` HTTP request in `/api/v1/wallet` endpoint

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

### UPDATE
PUT /api/v1/wallet

To update the user limit, do a `put` HTTP request in `/api/v1/wallet` endpoint

```
{
    "user_limit": 1000
}
```

### UPDATE
PUT /api/v1/wallet/buy

To make a purchase, do a `put` HTTP request in `/api/v1/wallet/buy` endpoint

```
{
    "value": 1000
}
```
