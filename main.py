from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from flask_cors import CORS
import base64

KEY_SIZE = 4096
PUBLIC_EXPONENT = 65537

app = Flask(__name__)

CORS(app)

@app.route('/generar_claves', methods=['POST'])
def generar_claves():
    try:
        password = request.form['password']

        if not password:
            raise Exception('Debe proporcionar una contraseña.')

        private_key = rsa.generate_private_key(
            public_exponent=PUBLIC_EXPONENT,
            key_size=KEY_SIZE,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
        )

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        clave_privada_str = private_key_pem.decode('utf-8')
        clave_publica_str = public_key_pem.decode('utf-8')

        return jsonify({
            'mensaje': 'Par de claves RSA generado correctamente.',
            'clave_privada': clave_privada_str,
            'clave_publica': clave_publica_str
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/firmar', methods=['POST'])
def firmar_archivo():
    try:
        if 'archivo' not in request.files:
            raise Exception('Debe proporcionar un archivo.')
        
        if 'clave_privada' not in request.files:
            raise Exception('Debe proporcionar una clave privada.')
        
        if 'password' not in request.form:
            raise Exception('Debe proporcionar una contraseña.')

        archivo = request.files['archivo']
        private_key_pem = request.files['clave_privada']
        password = request.form['password']

        private_key_pem_decoded = private_key_pem.read()

        private_key = serialization.load_pem_private_key(
            private_key_pem_decoded,
            password=password.encode(),
            backend=default_backend()
        )

        archivo_data = archivo.read()

        signature = private_key.sign(
            archivo_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        signature_base64 = base64.b64encode(signature)

        return jsonify({
            'mensaje': 'Firma digital generada correctamente',
            'firma':signature_base64.decode('utf-8')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400
        

@app.route('/verificar_firma', methods=['POST'])
def verificar_firma():
    try:
        if 'archivo_original' not in request.files:
            raise Exception('Debe proporcionar el archivo original.')
        
        if 'clave_publica' not in request.files:
            raise Exception('Debe proporcionar la clave publica.')
        
        if 'firma' not in request.files:
            raise Exception('Debe proporcionar la firma.')
        
        archivo_original = request.files['archivo_original']
        firma_file = request.files['firma']
        public_key_pem = request.files['clave_publica']

        archivo_original_data = archivo_original.read()
        firma_data = firma_file.read()
        public_key_pem_data = public_key_pem.read()

        firma_data_bytes = base64.b64decode(firma_data)

        public_key = serialization.load_pem_public_key(
            public_key_pem_data,
            backend=default_backend()
        )

        public_key.verify(
            firma_data_bytes,
            archivo_original_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return jsonify({'mensaje': 'Firma verificada correctamente'})
    except InvalidSignature as e:
         return jsonify({'error': 'Firma invalida.'}), 400
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Error de formato en los datos proporcionados.'}), 400
    except (Exception, ValueError, TypeError) as e:
        return jsonify({'error': f'Error al verificar la firma: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)