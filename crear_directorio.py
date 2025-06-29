import boto3
import json

def lambda_handler(event, context):
    # Parsear el cuerpo del evento
    if isinstance(event.get("body"), str):
        body = json.loads(event["body"])
    elif isinstance(event.get("body"), dict):
        body = event["body"]
    else:
        body = event  # Fallback para pruebas locales o sin API Gateway

    # Entrada
    bucket = body.get("bucket")
    directorio = body.get("directorio")

    # Validaciones
    if not bucket or not directorio:
        return {
            'statusCode': 400,
            'mensaje': "Los campos 'bucket' y 'directorio' son obligatorios."
        }

    # Asegurarse que el directorio termine con "/"
    if not directorio.endswith("/"):
        directorio += "/"

    # Proceso
    s3 = boto3.client('s3')

    try:
        # Crear objeto vacío con clave tipo carpeta
        s3.put_object(Bucket=bucket, Key=directorio)
        status = f"✅ Directorio '{directorio}' creado exitosamente en el bucket '{bucket}'."
        codigo = 200
    except Exception as e:
        status = f"❌ Error al crear el directorio: {str(e)}"
        codigo = 500

    # Salida
    return {
        'statusCode': codigo,
        'mensaje': status
    }
