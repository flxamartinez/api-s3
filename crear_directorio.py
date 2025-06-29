import boto3

def lambda_handler(event, context):
    # Entrada
    bucket = event.get("bucket")
    directorio = event.get("directorio")  # Por ejemplo: "nueva_carpeta/"

    # Proceso
    s3 = boto3.client('s3')

    try:
        # Subimos un objeto vacío con una clave que termina en "/"
        s3.put_object(Bucket=bucket, Key=directorio)
        status = f"Directorio '{directorio}' creado exitosamente en el bucket '{bucket}'."
        codigo = 200
    except Exception as e:
        status = f"Error al crear el directorio: {str(e)}"
        codigo = 500

    # Salida
    return {
        'statusCode': codigo,
        'mensaje': status
    }
