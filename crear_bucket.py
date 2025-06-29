import base64
import boto3
import json

def upload_base64_to_s3(s3_bucket_name, s3_file_key, base64_str):
    """
    Sube un archivo codificado en base64 a un bucket de S3.
    :param s3_bucket_name: Nombre del bucket
    :param s3_file_key: Ruta completa dentro del bucket (puede incluir "directorio/")
    :param base64_str: Contenido en base64 del archivo
    :return: Tuple (bucket, key)
    """
    s3 = boto3.resource('s3')
    objeto = s3.Object(s3_bucket_name, s3_file_key)
    objeto.put(Body=base64.b64decode(base64_str))
    return s3_bucket_name, s3_file_key

def lambda_handler(event, context):
    try:
        # Parsear el body si viene como string
        if isinstance(event.get("body"), str):
            body = json.loads(event["body"])
        elif isinstance(event.get("body"), dict):
            body = event["body"]
        else:
            body = event  # fallback (ejecución local)

        # Entrada
        bucket = body.get("bucket")
        directorio = body.get("directorio", "")
        nombre_archivo = body.get("nombre_archivo")
        contenido_base64 = body.get("contenido_base64")

        # Validación de campos obligatorios
        if not bucket or not nombre_archivo or not contenido_base64:
            return {
                'statusCode': 400,
                'mensaje': "Faltan campos requeridos: 'bucket', 'nombre_archivo' o 'contenido_base64'."
            }

        # Asegurar que el directorio termine con "/"
        if directorio and not directorio.endswith("/"):
            directorio += "/"

        # Clave final para S3
        clave_s3 = directorio + nombre_archivo

        # Subida
        bucket_name, key = upload_base64_to_s3(bucket, clave_s3, contenido_base64)

        return {
            'statusCode': 200,
            'mensaje': f"✅ Archivo '{nombre_archivo}' subido correctamente a '{key}' en el bucket '{bucket_name}'."
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'mensaje': f"❌ Error al subir archivo: {str(e)}"
        }
