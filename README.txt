SEMANA 11 - API S3 - Proyecto ampliado a 5 funciones
======================================================
BASADO EN EL ZIP ORIGINAL api-s3.zip adjuntado por el estudiante.
Se preservan los dos endpoints y nombres de las funciones originales.
Se modificaron los dos handlers originales para usar respuesta HTTP
lambda-proxy, manejo correcto de JSON y buckets vacios; las rutas se conservan.

NO SE HA DESPLEGADO EN AWS. Debes hacerlo desde tu EC2.

ARCHIVOS: serverless.yml, common.py, lista_buckets.py,
lista_objetos_bucket.py, crear_bucket.py, crear_directorio.py,
subir_archivo.py, prueba.txt y coleccion Postman.

1. Si descargas este ZIP en tu computadora, subelo a S3 usando AWS Console
   en un bucket donde tengas acceso. Luego en EC2:
   aws s3 cp s3://NOMBRE_BUCKET/api-s3-s11-completo.zip ~/api-s3-s11-completo.zip
   mkdir -p ~/lambdas
   unzip -o ~/api-s3-s11-completo.zip -d ~/lambdas
   cd ~/lambdas/api-s3

2. Verifica AWS:
   aws sts get-caller-identity
   aws iam get-role --role-name LabRole
   [Si el ultimo falla por AccessDenied, verificar IAM en consola]

3. serverless.yml contiene org: renzoliang, rol LabRole y account ID
   tomados DEL ARCHIVO ORIGINAL. Asegura que correspondan a tus recursos.
   Serverless Framework v4 puede exigir login: serverless login.

4. Comprueba YAML y despliega:
   serverless print --stage dev
   serverless deploy --stage dev
   serverless info --stage dev
   serverless deploy --stage test
   serverless info --stage test
   serverless deploy --stage prod
   serverless info --stage prod

5. Formato de las peticiones de prueba:
   POST /dev/s3/bucket/crear
   {"bucket":"renzoliang-s11-dev-NUMERO"}

   POST /dev/s3/bucket/crear-directorio
   {"bucket":"renzoliang-s11-dev-NUMERO","directorio":"evidencias"}

   POST /dev/s3/bucket/subir-archivo
   {"bucket":"renzoliang-s11-dev-NUMERO","directorio":"evidencias","archivo":"prueba.txt","contenido":"Prueba desde Postman"}

   GET /dev/s3/lista-buckets
   POST /dev/s3/bucket/lista-objetos {"bucket":"renzoliang-s11-dev-NUMERO"}

   Reemplaza dev por test/prod, la URL base por la de serverless info,
   y usa un bucket distinto en cada etapa.

6. Prueba de verificacion en la instancia:
   aws s3 ls s3://NOMBRE_BUCKET/evidencias/ --recursive

SEGURIDAD: endpoints sin autenticacion solo para el laboratorio;
no publicar las URLs; eliminar datos de prueba al finalizar.
