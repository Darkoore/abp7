# ABP 7
- Esto es un fork realizado de https://github.com/josehermosillaa/django_crud_alk
  
Cambios realizados:
* Solucion de 404 al iniciar sesion
* Programa ya no redirige a dashboard administrador al hacer logout
* se aplica validacion de autenticacion en navbar para una mejor experiencia de usuario
* Se implementa postgreSQL cuando sea un ambiente de produccion(debug= False)
* Se añade algo de css para mejorar experiencia de usuario


## Como utilizar postgreSQL
* Se debe instalar postgreSQL desde https://www.postgresql.org/download/
* tras instalar postgreSQL se debe inicializar pgadmin4 utilizando la contraseña creada durante la instalacion luego click derecho en database -> create -> alkewalle_db
* Realizar la instalacion en Visual Studio Code -> pip install psycopg2-binary
* ejecutar el siguiente comando en la consola de visual -> python manage.py migrate
* lanzar el programa django mediante -> python manage.py runserver
