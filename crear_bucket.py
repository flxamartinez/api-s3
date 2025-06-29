import boto3

def lambda_handler(event, context):
    # Entrada
    nombre_bucket = event.get("nombre_bucket")  # El nombre del bucket debe venir en el evento
    region = event.get("region", "us-east-1")   # Región por defecto es us-east-1

    # Proceso
    s3 = boto3.client('s3', region_name=region)

    try:
        if region == "us-east-1":
            response = s3.create_bucket(Bucket=nombre_bucket)
        else:
            response = s3.create_bucket(
                Bucket=nombre_bucket,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        status = "Bucket creado exitosamente"
        codigo = 200
    except Exception as e:
        status = str(e)
        codigo = 500

    # Salida
    return {
        'statusCode': codigo,
        'mensaje': status
    }
