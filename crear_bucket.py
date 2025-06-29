import boto3
import json

def lambda_handler(event, context):
    # Decodifica el cuerpo si viene como string JSON
    if isinstance(event.get("body"), str):
        body = json.loads(event["body"])
    else:
        body = event.get("body", {})

    # Entrada
    nombre_bucket = body.get("nombre_bucket")
    region = body.get("region", "us-east-1")

    # Proceso
    s3 = boto3.client('s3', region_name=region)

    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=nombre_bucket)
        else:
            s3.create_bucket(
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