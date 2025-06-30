import boto3
import json

def lambda_handler(event, context):
    try:
        if isinstance(event.get("body"), str):
            datos = json.loads(event["body"])
        elif isinstance(event.get("body"), dict):
            datos = event["body"]
        else:
            datos = event  
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'mensaje': f"❌ Error al interpretar los datos de entrada: {str(e)}"
            })
        }

 
    nombre_bucket = datos.get('bucket')
    nombre_directorio = datos.get('directorio')

    if not nombre_bucket or not nombre_directorio:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'mensaje': "❌ Los campos 'bucket' y 'directorio' son obligatorios."
            })
        }

    # Asegurar que termine con "/"
    if not nombre_directorio.endswith('/'):
        nombre_directorio += '/'

    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=nombre_bucket, Key=nombre_directorio)
        estado = 200
        mensaje = f"✅ Directorio '{nombre_directorio}' creado exitosamente en el bucket '{nombre_bucket}'."
    except Exception as e:
        estado = 500
        mensaje = f"❌ Error al crear directorio: {str(e)}"

    return {
        'statusCode': estado,
        'body': json.dumps({
            'mensaje': mensaje
        })
    }
