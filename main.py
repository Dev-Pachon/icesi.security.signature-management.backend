from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64

app = Flask(__name__)


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