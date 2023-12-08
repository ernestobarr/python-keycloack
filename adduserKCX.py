import requests


def create_users(user_list):
    # URL para obtener el token de acceso en Keycloak
    accessTokenUrl = "http://localhost:8080/realms/master/protocol/openid-connect/token"
    username = 'admin'
    password = 'admin'

    # Construir el payload para la solicitud de token
    payload = f'client_id=admin-cli&username={username}&password={password}&grant_type=password'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Imprimir mensaje informativo
    print('Retrieving Access token from Keycloak')

    # Enviar solicitud POST para obtener el token de acceso
    response = requests.post(accessTokenUrl, headers=headers, data=payload)

    # Extraer el token de acceso del cuerpo de la respuesta JSON
    access_token = response.json()['access_token']

    # Imprimir el token de acceso
    print('Here is the access token', access_token)

    # URL para añadir usuarios en Keycloak
    addUserUrl = "http://localhost:8080/admin/realms/master/users"

    # Configurar encabezados para la solicitud de añadir usuario
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Imprimir mensaje informativo
    print('Creating users in Keycloak')

    for user_info in user_list:
        # Enviar solicitud POST para añadir un usuario con la información proporcionada
        response = requests.post(addUserUrl, headers=headers, json=user_info)

        # Verificar el código de estado de la respuesta para cada usuario
        if response.status_code == 201:
            # Obtener el nombre del usuario del diccionario user_info (si está presente)
            user_name = user_info.get('username', 'Unknown')

            # Imprimir mensaje de éxito para cada usuario
            print(f'User {user_name} added successfully')
        elif response.status_code == 409:
            # Imprimir mensaje si el usuario ya existe en Keycloak
            print(f'User {user_info.get("username", "Unknown")} already exists in Keycloak')
        else:
            # Imprimir mensaje de error y detalles de la respuesta en caso de error
            print('Error adding user. Status code:', response.status_code)
            print('Response:', response.text)

    # Mensaje final de creacion de usuarios
    print('Finished creating users')


# Añadir varios usuarios al mismo tiempo
users_to_add = [
    {
        "email": "user1@example.com",
        "username": "user1@example.com",
        "enabled": True,
        "firstName": "User",
        "lastName": "One",
        "credentials": [{"value": "secret1", "type": "password"}],
        "realmRoles": ["user_default"],
        "attributes": {"example": "1,2,3,3"}
    },
    {
        "email": "user2@example.com",
        "username": "user2@example.com",
        "enabled": True,
        "firstName": "User",
        "lastName": "Two",
        "credentials": [{"value": "secret2", "type": "password"}],
        "realmRoles": ["admin"],
        "attributes": {"example": "1,2,3,3"}
    },
    {
        "email": "user3@example.com",
        "username": "user3@example.com",
        "enabled": True,
        "firstName": "User",
        "lastName": "Three",
        "credentials": [{"value": "secret3", "type": "password"}],
        "realmRoles": ["user_default"],
        "attributes": {"example": "1,2,3,3"}
    }
]

# Llamar a la función con la lista de usuarios
create_users(users_to_add)
