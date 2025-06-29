import base64
import boto3

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
        # Entrada
        bucket = event.get("bucket")
        directorio = event.get("directorio", "")
        nombre_archivo = event.get("nombre_archivo")
        contenido_base64 = event.get("contenido_base64")

        if not bucket or not nombre_archivo or not contenido_base64:
            raise ValueError("Faltan datos obligatorios: bucket, nombre_archivo o contenido_base64.")

        # Aseguramos que el "directorio" termine en /
        if directorio and not directorio.endswith("/"):
            directorio += "/"

        clave_s3 = directorio + nombre_archivo

        # Subimos el archivo
        bucket_name, key = upload_base64_to_s3(bucket, clave_s3, contenido_base64)

        # Salida
        mensaje = f"✅ Archivo '{nombre_archivo}' subido a '{key}' en el bucket '{bucket_name}'."
        return {
            'statusCode': 200,
            'mensaje': mensaje
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'mensaje': f"❌ Error al subir archivo: {str(e)}"
        }
