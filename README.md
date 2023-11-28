# RSA Signature Service

## Overview

This Flask application provides a simple web service for generating and verifying digital signatures using RSA (Rivest–Shamir–Adleman) asymmetric cryptography. The service exposes three main functionalities:

1. **Generar Claves (/generar_claves):** Generates an RSA key pair (public and private keys) and returns them in PEM format.

2. **Firmar Archivo (/firmar):** Signs a file using a provided private key and password. The digital signature is returned in base64 format.

3. **Verificar Firma (/verificar_firma):** Verifies the digital signature of an original file using a provided public key.

## Prerequisites

- [Docker](https://www.docker.com/)
- Git

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Dev-Pachon/icesi.security.signature-management.backend.git
    cd icesi.security.signature-management.backend
    ```

2. Build the Docker image:

    ```bash
    docker build -t rsa-signature-service .
    ```

3. Run the Docker container:

    ```bash
    docker run -p 5000:5000 rsa-signature-service
    ```

    The application will start running on `http://127.0.0.1:5000/`.


2. Use a tool like [Postman](https://www.postman.com/) or `curl` to interact with the service. Below are examples for each functionality:

    - **Generar Claves:**
        - Endpoint: `http://127.0.0.1:5000/generar_claves`
        - Method: `POST`
        - Form Data:
            - `password`: Your chosen password

    - **Firmar Archivo:**
        - Endpoint: `http://127.0.0.1:5000/firmar`
        - Method: `POST`
        - Form Data:
            - `archivo`: Select a file
            - `clave_privada`: Select the private key file
            - `password`: Your chosen password

    - **Verificar Firma:**
        - Endpoint: `http://127.0.0.1:5000/verificar_firma`
        - Method: `POST`
        - Form Data:
            - `archivo_original`: Select the original file
            - `firma`: Select the signature file
            - `clave_publica`: Select the public key file

## Responses

- Successful responses will include a JSON object with a 'mensaje' (message) field.
- Error responses will include a JSON object with an 'error' field.

## Notes

- For security reasons, this application is intended for educational purposes and should not be used as-is in a production environment without proper security measures.

- Ensure that you handle private keys and passwords securely.

- When interacting with the service, be mindful of the input types and requirements specified for each endpoint.
