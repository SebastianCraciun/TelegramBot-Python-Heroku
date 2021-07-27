@echo off
:MENU
ECHO ...............................................
ECHO Selecciona '1', '2', '3', '4', '5', '6', o '7' para salir.
ECHO ...............................................
ECHO.
ECHO 1 - Login Heroku Container
ECHO 2 - Crear el contenedor con los cambios
ECHO 3 - Pushear los cambios a Heroku despues de crear el contenedor
ECHO 4 - Desplegar la aplicacion
ECHO 5 - Borrar el despliegue de la aplicacion
ECHO 6 - Logs de la aplicacion
ECHO 7 - Salir
ECHO.

SET /P M=Selecciona '1', '2', '3', '4', '5', '6', '7', y despues ENTER: 
IF %M%==1 GOTO LOGIN
IF %M%==2 GOTO CRTCONT
IF %M%==3 GOTO PUSH
IF %M%==4 GOTO DEPLOY
IF %M%==5 GOTO DEL
IF %M%==6 GOTO LOGS
IF %M%==7 GOTO EOF


:LOGIN
heroku container:login
GOTO MENU

:CRTCONT
docker build -t image-bot-python .
GOTO MENU

:PUSH
heroku container:push web -a elcybercurioso-bot
GOTO MENU

:DEPLOY
heroku container:release web -a elcybercurioso-bot
GOTO MENU

:DEL
heroku container:release web -a elcybercurioso-bot
GOTO MENU

:LOGS
heroku logs -t -a elcybercurioso-bot

:EOF
@cls&exit