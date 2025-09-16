

VALID_USER_DATA = {
    "nickname": "testuser",
    "password": "Testpassword*",
    "email": "testuuser@test.com",
    "birthdate": "13-09-1991",
    "name": "User",
    "surname": "Fortesting",
    "description": "Description"

}


INVALID_USER_DATA = {

    "nickname": "testuser2",
    #Invalid password because it doesn't met all the conditions we specified
    "password": "password",
    "photo": "photourl",
    "email": "testuuser2@test.com",
    "birthdate": "13-09-1991",
    "name": "User",
    "surname": "Fortesting",
    "description": "Description"

}

EXISTING_USER_DATA = {
        "nickname": "claralcala",
        "password": "TestPassword*",
        "photo": "photourl",
        "email": "alcalagarciaclara@gmail.com",
        "birthdate": "13-09-1991",
        "name": "Clara",
        "surname": "Alcala",
        "description": "description"
    }

EXISTING_USERNAME_DATA = {
        "nickname": "claralcala",
        "password": "TestPassword*",
        "photo": "photourl",
        "email": "inventedemail@gmail.com",
        "birthdate": "13-09-1991",
        "name": "Clara",
        "surname": "Alcala",
        "description": "description"
    }
MISSING_FIELD_USER_DATA = {
            "nickname": "testuser3",
            "password": "TestPassword*",
            "photo": "photourl",
            # Missing email
            "birthdate": "13-09-1991",
            "name": "User",
            "surname": "Fortesting",
            "description": "Description"
        }

CORRECT_LOGIN = {
    "email": "alcalagarciaclara@gmail.com",
    "password": "jexpsGFD"
}

INCORRECT_LOGIN = {
    "email": "thisemaildoesntexist@email.com",
    "password": "password"
}

FORGOT_PASSWORD = {
    "email": "testuuser@test.com"
}

TRIP_DATA = {
        "photo": "string",
        "origin": 500,
        "destination": 300,
        "start_date": "23-02-2025",
        "end_date": "28-02-2025",
        "description": "This is a test trip",
        "transportation_method_ids": [1, 2]
    }