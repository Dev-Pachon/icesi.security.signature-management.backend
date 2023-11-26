from flask import Flask, request, jsonify, send_file
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64

app = Flask(__name__)




@app.route('/generar_claves', methods=['POST'])
def generar_claves():
    try:
        password = request.form['password']

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
        )
        with open('clave_privada.pem', 'wb') as private_key_file:
            private_key_file.write(private_key_pem)

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open('clave_publica.pem', 'wb') as public_key_file:
            public_key_file.write(public_key_pem)

        clave_privada_str = private_key_pem.decode('utf-8')
        clave_publica_str = public_key_pem.decode('utf-8')

        return jsonify({
            'mensaje': 'Par de claves RSA generado y guardado correctamente',
            'clave_privada': clave_privada_str,
            'clave_publica': clave_publica_str,
            'ruta_clave_privada': '/descargar/clave_privada',
            'ruta_clave_publica': '/descargar/clave_publica'
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/descargar/clave_privada')
def descargar_clave_privada():
    return send_file('clave_privada.pem', as_attachment=True)

@app.route('/descargar/clave_publica')
def descargar_clave_publica():
    return send_file('clave_publica.pem', as_attachment=True)


@app.route('/firmar', methods=['POST'])
def firmar_archivo():
    try:
        archivo = request.files['archivo']
        private_key_pem = request.form['private_key']

        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None,
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

        signature_base64 = base64.b64encode(signature).decode('utf-8')

        with open('firma_digital.txt', 'w') as firma_file:
            firma_file.write(signature_base64)

        return jsonify({'mensaje': 'Firma digital generada y guardada correctamente'})

    except Exception as e:
        return jsonify({'error': str(e)})
        

@app.route('/verificar_firma', methods=['POST'])
def verificar_firma():
    try:
        archivo_original = request.files['archivo_original']
        firma_file = request.files['firma_file']
        public_key_pem = request.form['public_key']

        public_key = serialization.load_pem_public_key(
            public_key_pem.encode(),
            backend=default_backend()
        )

        archivo_original_data = archivo_original.read()
        firma_data = firma_file.read()

        signature = base64.b64decode(firma_data)

        public_key.verify(
            signature,
            archivo_original_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return jsonify({'mensaje': 'Firma verificada correctamente'})

    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Error de formato en los datos proporcionados.'})
    except (Exception, ValueError, TypeError) as e:
        return jsonify({'error': f'Error al verificar la firma: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)