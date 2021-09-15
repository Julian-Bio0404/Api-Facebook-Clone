# Api-Facebook-Clone
REST API que simula todas las funcionalidades de Facebook

![](https://img.shields.io/badge/python-v3.9-blue)
![](https://img.shields.io/badge/django-v3.2.5-blue)
![](https://img.shields.io/badge/djangorestframework-v3.12.4-blue)
![](https://img.shields.io/badge/psycopg2-v2.9.1-blue)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Julian-Bio0404/Api-Facebook-Clone)

## Features
### :bust_in_silhouette: Users 
  + **User** 
    + Sign-Up
    + Verificación de cuenta
    + Refrescar token de verificación de cuenta
    + Sign-In
    + Generación de token para recuperar contraseña
    + Recuperación o Actualización de contraseña
    + Detalle de Usuario
    + Actualización de datos de usuario
  + **Profile**
    + Detalle de un perfil
    + Follow o unfollow de usuario
    + Listar followers y following de un perfil
    + Listar amigos de un usuario
    + Actualización completa o parcial de perfil
    + Actualización completa o parcial de detalles de perfil
  + **Friend request**
    + Enviar, aceptar o eliminar solicitud de amistad
    + Detalle de una solicitud de amistad
    + Listar solicitudes de amistad de un usuario
    
### :newspaper: Posts
  + **Post**
    + Publicar post en biografía, biografía de una amigo, FbPage o grupo
    + Actualizar, reaccionar, compartir o eliminar un post
    + Detalle de un post
    + Etiquetar amigos en un post
    + Listar posts
    + Listar compartidas de un post
    + Eliminar rección
    + Listar reacciones de un post
 + **Comment**
    + Crear, actualizar o eliminar un comentario de un post
    + Detalle de un comentario
    + Listar comentarios de un post
    + Reaccionar a un comentario
    + Eliminar una reaccion de un comentario
    + Listar reacciones de un comentario
 + **Saved**
    + Crear, actualizar o eliminar una categoria de guardado
    + Detalle de una categoria
    + Guardar un post
    + Listar posts guardados
    + Detalle de un post guardado
    + Eliminar post de guardados

### :busts_in_silhouette: Groups
  + **Group**
    + Crear, actualizar o eliminar un grupo
    + Detalle de un grupo
    + Listar grupos
    + Listar posts de un grupo
    + Enviar invitación para unirse a un grupo
    + Aceptar invitación 
  + **Membership**
    + Listar miembros de un grupo
    + Confirmar una membresía
    + Eliminar miembro de un grupo
    + Listar solicitudes de union del grupo
    
### :green_book: Fbpages
  + **Fbpage**
    + Crear, actualizar o eliminar una página
    + actualización parcial o completa de detalles de una página
    + Detalle de una página
    + Listar páginas
    + Seguir una página
    + Crear un post desde una página
    + Listar posts de una página
    + Añadir o eliminar admin de una página
  
## Features faltantes
  - [ ] Invitación a dar like a una Fbpage :heart:
  - [ ] Eventos :date:
  - [ ] Hashtags :pushpin:
  - [ ] Sistema de configuración de privacidad de usuario :lock:
  - [ ] Tareas asíncronas y periódicas con Celery :hourglass:
  - [ ] Sistema de notificaciones :bell:
  - [ ] Chat :speech_balloon:
  - [ ] Sistema de OAuth2 :warning::octocat:
  - [ ] Dockerizar :whale: