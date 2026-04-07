# Comandos extras

## comando para obtener un archivo de requerimientos (requirements.txt)

con el entrono virtual activado podemos exportar todas las librerias instaladas en el con el comando

``` pip freeze > requirements.txt ```

esto crea un archivo requirements.txt en la raiz del proyecto similar a este

```
asgiref==3.11.1
asttokens==3.0.1
colorama==0.4.6
decorator==5.2.1
Django==6.0.3
executing==2.2.1
ipython==9.11.0
ipython_pygments_lexers==1.1.1
jedi==0.19.2
matplotlib-inline==0.2.1
mysqlclient==2.2.8
parso==0.8.6
prompt_toolkit==3.0.52
pure_eval==0.2.3
Pygments==2.19.2
sqlparse==0.5.5
stack-data==0.6.3
traitlets==5.14.3
tzdata==2025.3
wcwidth==0.6.0

```
## instalar los paquetes a traves del archivo requirements.txt

teniendo el archivo en la misma ruta que el entorno virtual nuevo, ejecutamos
``` pip install -r requirements.txt```
esto instalra todos los paquetes listados en el archivo, en las versiones que aparecen.