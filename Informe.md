# Informe

El proyecto se trata de una desarrollo de software que busca dar solución a los siguientes requerimientos:

El programa debe tener tres opciones: 
1) Generación de un par de claves RSA. Debe generar la clave pública y la privada en dos archivos separados. El archivo de la clave privada debe quedar protegido con una contraseña.
2) Firmar archivo. Esta opción recibe como entradas un archivo cualquiera, y el archivo de clave privada. Una vez comprobada la contraseña de bloqueo de la clave privada, el programa debe generar la firma digital del archivo, y guardarla en un archivo aparte.
3) Verificación de firma. Esta opción debe recibir como entradas el archivo original, el archivo que contiene la firma y el archivo de clave pública. Con estas tres entradas, debe verificarse que la firma sea correcta.

## ¿Cómo se realizó el proyecto?

Este código es una implementación básica de un servicio web con Flask que ofrece funcionalidades relacionadas con la generación y verificación de firmas digitales utilizando criptografía asimétrica RSA. Aquí hay una explicación paso a paso del código:

### Importaciones:
**Flask, request, jsonify:** Importa las clases y funciones necesarias de Flask para crear un servidor web, manejar solicitudes HTTP y devolver respuestas JSON.  
**cryptography:** Importa las funciones necesarias de la biblioteca [cryptography](https://cryptography.io/en/latest/) para trabajar con criptografía asimétrica.  
**flask_cors:** Importa la extensión CORS de Flask para permitir solicitudes de recursos desde otro dominio.  

### Parámetros de Configuración:  
**KEY_SIZE:** Tamaño de bits para las claves RSA.  
**PUBLIC_EXPONENT:** Exponente público para la generación de claves RSA.  

### Rutas del Servicio Web:  
1. Ruta /generar_claves (Método POST):  
**Objetivo:** Generar un par de claves RSA (pública y privada).  
**Implementación:**  
Lee la contraseña proporcionada en la solicitud.  
Genera un par de claves RSA.  
Convierte las claves a formato PEM y las codifica en base64.  
Devuelve las claves en formato JSON.  
2. Ruta /firmar (Método POST):  
**Objetivo:** Firmar un archivo utilizando una clave privada RSA.  
**Implementación:**  
Verifica la presencia de archivos y parámetros necesarios en la solicitud.  
Lee el archivo, la clave privada y la contraseña proporcionados.  
Descodifica la clave privada y carga la clave privada RSA.  
Lee el archivo, firma los datos y devuelve la firma en formato base64.  
3. Ruta /verificar_firma (Método POST):  
**Objetivo:** Verificar la firma digital de un archivo utilizando una clave pública RSA.  
**Implementación:**  
Verifica la presencia de archivos y parámetros necesarios en la solicitud.  
Lee el archivo original, la firma y la clave pública proporcionados.  
Descodifica la firma y carga la clave pública RSA.  
Verifica la firma y devuelve el resultado.  
### Manejo de Excepciones:  
Se manejan excepciones para responder a situaciones de error con mensajes informativos en formato JSON.  

## Dificultades

## Conclusiones
El proyecto ha logrado implementar de manera funcional las tres principales características solicitadas:

Generación de Claves RSA:
La aplicación genera un par de claves RSA (pública y privada) y las almacena en archivos separados, protegiendo la clave privada con una contraseña.

Firma de Archivos:
Permite firmar archivos mediante la clave privada, generando una firma digital que se guarda en un archivo aparte.

Verificación de Firmas:
Ofrece la capacidad de verificar la firma digital de un archivo utilizando la clave pública correspondiente.
La implementación se basa en un servicio web construido con Flask y utiliza la biblioteca cryptography para operaciones criptográficas. El código aborda los requisitos planteados de manera clara y efectiva.

Las dificultades identificadas durante el desarrollo incluyen aspectos relacionados con la seguridad de contraseñas y archivos, validación de entradas y manejo de errores. Sin embargo, en términos de funcionalidad, el proyecto cumple con los objetivos establecidos.
En conclusión, la aplicación actual logra satisfacer los requisitos del proyecto al proporcionar una solución completa para la generación, firma y verificación de claves digitales utilizando criptografía RSA.

