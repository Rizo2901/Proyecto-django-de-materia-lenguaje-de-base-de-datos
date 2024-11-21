from django.shortcuts import get_object_or_404, redirect, render
import cx_Oracle
from django.conf import settings
from django.contrib import messages
from django.db import connection
from django.http import HttpResponse, JsonResponse
from .models import Noticias, Temas, Subtemas, Autores

# Create your views here.

def internacional_view(request):
    return render(request, 'internacional.html')



def noticias_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'edit':
            return editar_noticia(request)
        elif action == 'delete':
            return eliminar_noticia(request)
        elif action == 'add':
            return agregar_noticia(request)
        else:
            return JsonResponse({'status': 'error', 'message': 'Acción no válida'}, status=400)
    
    elif request.method == 'GET':
        id_noticia = request.GET.get('id_noticia')
        if id_noticia:
            return obtener_noticia(request, id_noticia)
        else:
            # Obtener datos para los dropdowns
            temas = listado_temas()
            subtemas = listado_subtemas()
            autores = listado_autores()
            
            # Obtener el listado de noticias
            noticias = listado_noticias()

            context = {
                'noticias': noticias,
                'temas': temas,
                'subtemas': subtemas,
                'autores': autores,
            }
            return render(request, 'noticias.html', context)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


#Obtener id de autor para dropdown 
def obtener_id_autor(primer_nombre_autor, segundo_nombre_autor):
    dsn = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    
    try:
        with connection.cursor() as cursor:
            id_autor = cursor.var(cx_Oracle.NUMBER)
            cursor.callproc('SP_OBTENER_ID_AUTOR', [primer_nombre_autor, segundo_nombre_autor, id_autor])
            return id_autor.getvalue() if id_autor.getvalue() else None
    finally:
        connection.close()


# Función para obtener el listado de noticias
def listado_noticias():
    dsn = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    
    try:
        with connection.cursor() as cursor:
            out_cur = connection.cursor()
            try:
                cursor.callproc("SP_obtener_todas_las_noticias", [out_cur])
                lista = []
                for fila in out_cur:
                    fila = list(fila)
                    if isinstance(fila[4], cx_Oracle.LOB):
                        fila[4] = fila[4].read()
                    lista.append(fila)
                return lista
            except cx_Oracle.DatabaseError as e:
                print("Error al ejecutar el procedimiento:", e)
                return []
            finally:
                out_cur.close()
    finally:
        connection.close()

# Función para editar una noticia
def editar_noticia(request):
    if request.method == 'POST':
        id_noticia = request.POST.get('id_noticia')
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        id_tema = request.POST.get('id_tema')
        id_subtema = request.POST.get('id_subtema')
        nombre_autor = request.POST.get('nombre_autor')

        if all([id_noticia, titulo, contenido, id_tema, id_subtema, nombre_autor]):
            try:
                dsn = settings.DATABASES['default']['NAME']
                user = settings.DATABASES['default']['USER']
                password = settings.DATABASES['default']['PASSWORD']
                
                connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
                with connection.cursor() as cursor:
                    cursor.callproc('sp_editar_noticia', [
                        id_noticia,
                        titulo, 
                        contenido,
                        id_tema, 
                        id_subtema, 
                        nombre_autor
                    ])
                connection.commit()
                return redirect('noticias')
            except cx_Oracle.DatabaseError as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
            finally:
                connection.close()
        else:
            return JsonResponse({'status': 'error', 'message': 'Todos los campos son requeridos'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)



def eliminar_noticia(request):
    if request.method == 'POST':
        id_noticia = request.POST.get('noticia_id')
        
        if not id_noticia:
            return JsonResponse({'status': 'error', 'message': 'ID de noticia no proporcionado'}, status=400)
        
        try:
            with connection.cursor() as cursor:
                cursor.callproc('SP_eliminar_noticia', [id_noticia])
            return redirect('noticias')  
        except Exception as e:
            
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def agregar_noticia(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        nombre_tema = request.POST.get('nombre_tema')
        nombre_subtema = request.POST.get('nombre_subtema')
        nombre_autor = request.POST.get('nombre_autor')  

     
        if nombre_autor:
            nombres_autor = nombre_autor.split(' ', 1)
            if len(nombres_autor) == 2:
                primer_nombre_autor, segundo_nombre_autor = nombres_autor
            else:
                primer_nombre_autor = nombres_autor[0]
                segundo_nombre_autor = ''
        else:
            primer_nombre_autor = ''
            segundo_nombre_autor = ''

        if all([titulo, contenido, nombre_tema, nombre_subtema, primer_nombre_autor]):
            try:
                dsn = settings.DATABASES['default']['NAME']
                user = settings.DATABASES['default']['USER']
                password = settings.DATABASES['default']['PASSWORD']
                
                connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
                with connection.cursor() as cursor:
                    cursor.callproc('SP_insertar_noticia_con_nombres', [
                        nombre_tema, 
                        nombre_subtema, 
                        titulo, 
                        contenido, 
                        primer_nombre_autor, 
                        segundo_nombre_autor
                    ])
                connection.commit()
                return redirect('noticias')
            except cx_Oracle.DatabaseError as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
            finally:
                connection.close()
        else:
            return JsonResponse({'status': 'error', 'message': 'Todos los campos son requeridos'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)



def obtener_noticia(request, id_noticia):
    if request.method == 'GET':
        
        titulo = None
        contenido = None
        id_tema = None
        id_subtema = None
        autor_id = None

        try:
            dsn = settings.DATABASES['default']['NAME']
            user = settings.DATABASES['default']['USER']
            password = settings.DATABASES['default']['PASSWORD']

            
            with cx_Oracle.connect(user=user, password=password, dsn=dsn) as connection:
                with connection.cursor() as cursor:
                    
                    cursor.callproc('sp_obtener_noticia_por_id', [
                        id_noticia,
                        titulo,  
                        contenido,  
                        id_tema,  
                        id_subtema,  
                        autor_id  
                    ])

                    
                    titulo = cursor.var(cx_Oracle.STRING).getvalue()
                    contenido = cursor.var(cx_Oracle.CLOB).getvalue()
                    id_tema = cursor.var(cx_Oracle.NUMBER).getvalue()
                    id_subtema = cursor.var(cx_Oracle.NUMBER).getvalue()
                    autor_id = cursor.var(cx_Oracle.NUMBER).getvalue()

        except cx_Oracle.DatabaseError as e:
            return render(request, 'error.html', {'message': str(e)})

        
        temas = Temas.objects.all()
        subtemas = Subtemas.objects.all()
        autores = Autores.objects.all()

        context = {
            'noticia': {
                'id_noticia': id_noticia,
                'titulo': titulo,
                'contenido': contenido,
                'id_tema': id_tema,
                'id_subtema': id_subtema,
                'autor_id': autor_id
            },
            'temas': temas,
            'subtemas': subtemas,
            'autores': autores
        }

        return render(request, 'noticias.html', context)

    return render(request, 'error.html', {'message': 'Método no permitido'}, status=405)
    
 
def subtemas_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'edit':
            return editar_subtema(request)
        elif action == 'delete':
            return eliminar_subtema(request)
        elif action == 'add':
            return agregar_subtema(request)
    elif request.method == 'GET':
        if 'id_subtema' in request.GET:
            return obtener_subtema(request)
        else:
            subtemas = listado_subtemas()
            temas = Temas.objects.all()  
            return render(request, 'subtemas.html', {'subtemas': subtemas, 'temas': temas})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def listado_subtemas():
    dsn = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    
    try:
        with connection.cursor() as cursor:
            out_cur = cursor.var(cx_Oracle.CURSOR)  
            try:
                cursor.callproc("SP_ver_todos_los_subtemas", [out_cur])
                lista = []
                for fila in out_cur.getvalue():
                    lista.append({
                        'id_subtema': fila[0],
                        'id_tema': fila[1],
                        'nombre': fila[2]
                    })
                return lista
            except cx_Oracle.DatabaseError as e:
                print("Error al ejecutar el procedimiento:", e)
                return []
    finally:
        connection.close()



def obtener_nombre_tema(id_tema):
    dsn = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    
    try:
        with connection.cursor() as cursor:
            nombre_tema = cursor.var(cx_Oracle.STRING)
            cursor.callproc('SP_OBTENER_NOMBRE_TEMA', [id_tema, nombre_tema])
            return nombre_tema.getvalue() if nombre_tema.getvalue() else None
    finally:
        connection.close()


def obtener_id_tema(nombre_tema):
    dsn = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    
    try:
        with connection.cursor() as cursor:
            id_tema = cursor.var(cx_Oracle.NUMBER)
            cursor.callproc('SP_OBTENER_ID_TEMA', [nombre_tema, id_tema])
            return id_tema.getvalue() if id_tema.getvalue() else None
    finally:
        connection.close()

def agregar_subtema(request):
    if request.method == 'POST':
        nombre_subtema = request.POST.get('nombre')
        nombre_tema = request.POST.get('nombre_tema')

        if nombre_subtema and nombre_tema:
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('sp_agregar_subtema', [nombre_subtema, nombre_tema])
                return redirect('subtemas')
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Faltan datos'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def editar_subtema(request):
    if request.method == 'POST':
        id_subtema = request.POST.get('id_subtema')
        nombre_subtema = request.POST.get('nombre', None)
        nombre_tema = request.POST.get('nombre_tema', None)

        if id_subtema:
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('sp_editar_subtema', [id_subtema, nombre_subtema, nombre_tema])
                return redirect('subtemas')
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Faltan datos'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)




def obtener_subtema(request):
    id_subtema = request.GET.get('id_subtema')
    if not id_subtema:
        return JsonResponse({'status': 'error', 'message': 'ID de subtema no proporcionado'}, status=400)
    
    try:
        subtemas = listado_subtemas()  
        
        for subtema in subtemas:
            if str(subtema['id_subtema']) == id_subtema:
                return JsonResponse({'status': 'success', 'id_subtema': subtema['id_subtema'], 'id_tema': subtema['id_tema'], 'nombre': subtema['nombre']})
        
        return JsonResponse({'status': 'error', 'message': 'Subtema no encontrado'}, status=404)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def eliminar_subtema(request):
    if request.method == 'POST':
        id_subtema = request.POST.get('id_subtema')
        
        if id_subtema:
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('SP_eliminar_subtema', [id_subtema])
                return redirect('subtemas')
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Faltan datos'})
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

    
#Vista principal para usuarios
def usuarios_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'edit':
            return editar_usuario(request)
        elif action == 'delete':
            return eliminar_usuario(request)
        elif action == 'add':
            return agregar_usuario(request)
    elif request.method == 'GET':
        if 'id_usuario' in request.GET:
            return obtener_usuario(request)
        else:
            usuarios = listado_usuarios()
            return render(request, 'usuarios.html', {'usuarios': usuarios})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)



def listado_usuarios():
    dsn = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    
    try:
        with connection.cursor() as cursor:
            out_cur = cursor.var(cx_Oracle.CURSOR) 
            cursor.callproc("sp_obtener_todos_los_usuarios", [out_cur])  
            
            lista = []
            for fila in out_cur.getvalue():
                lista.append({
                    'id_usuario': fila[0],  
                    'primer_nombre': fila[1],
                    'segundo_nombre': fila[2],
                    'email': fila[3]     
                })
            return lista
    except cx_Oracle.DatabaseError as e:
        print("Error al ejecutar el procedimiento:", e)
        return []
    finally:
        connection.close()


def agregar_usuario(request):
    if request.method == 'POST':
        primer_nombre = request.POST.get('primer_nombre')
        segundo_nombre = request.POST.get('segundo_nombre')
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')

      
        if not primer_nombre or not segundo_nombre or not email or not contrasena:
            return render(request, 'error.html', {'error': 'Todos los campos son obligatorios.'})

        dsn = settings.DATABASES['default']['NAME']
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        
        try:
            connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
            with connection.cursor() as cursor:
                cursor.callproc(
                    'sp_agregar_usuario', 
                    [primer_nombre, segundo_nombre, email, contrasena]
                )
            connection.commit() 
            return redirect('usuarios') 
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            return render(request, 'error.html', {'error': error.message})
        finally:
            connection.close()
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
    

def eliminar_usuario(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')

        if usuario_id:
            try:
                
                with connection.cursor() as cursor:
                    cursor.callproc('sp_eliminar_usuario', [usuario_id])
                
                messages.success(request, 'Usuario eliminado con éxito.')
            except Exception as e:
                messages.error(request, f'Error al eliminar el usuario: {e}')
        
        return redirect('usuarios')  
    else:
        return redirect('usuarios')


def editar_usuario(request):
    p_id_usuario = request.POST.get('id_usuario')
    primer_nombre = request.POST.get('primer_nombre')
    segundo_nombre = request.POST.get('segundo_nombre')
    email = request.POST.get('email')
    contrasena = request.POST.get('contrasena')

    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'sp_actualizar_usuario',
                [p_id_usuario, primer_nombre, segundo_nombre, email, contrasena]
            )
        return redirect('usuarios')  
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return render(request, 'error.html', {'error': error.message})
    


def temas_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'edit':
            return editar_tema(request)
        elif action == 'delete':
            return eliminar_tema(request)
        elif action == 'add':
            return agregar_tema(request)
    elif request.method == 'GET':
        if 'id_tema' in request.GET:
            return obtener_tema(request)
        else:
            temas = listado_temas()
            return render(request, 'temas.html', {'temas': temas})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def editar_tema(request):
    if request.method == 'POST':
        id_tema = request.POST.get('id_tema')
        nombre = request.POST.get('nombre')
        
        if not id_tema or not nombre:
            return JsonResponse({'status': 'error', 'message': 'ID del tema o nombre no proporcionado'}, status=400)
        
        try:
            with connection.cursor() as cursor:
                cursor.callproc('SP_actualizar_tema', [int(id_tema), nombre])
            return redirect('temas')  
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def eliminar_tema(request):
    if request.method == 'POST':
        id_tema = request.POST.get('id_tema')
        if not id_tema:
            return JsonResponse({'status': 'error', 'message': 'ID de tema no proporcionado'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('SP_eliminar_tema', [id_tema])
            return redirect('temas')  
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def agregar_tema(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if not nombre:
            return JsonResponse({'status': 'error', 'message': 'Nombre del tema no proporcionado'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('SP_insertar_tema', [nombre])
            return redirect('temas') 
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def listado_temas():
    dsn = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    
    try:
        with connection.cursor() as cursor:
            out_cur = cursor.var(cx_Oracle.CURSOR)  
            try:
                cursor.callproc("SP_ver_todos_los_temas", [out_cur])
                lista = []
                for fila in out_cur.getvalue():
                    lista.append({
                        'id_tema': fila[0],
                        'nombre': fila[1]
                    })
                return lista
            except cx_Oracle.DatabaseError as e:
                print("Error al ejecutar el procedimiento:", e)
                return []
    finally:
        connection.close()

def obtener_tema(request):
    if request.method == 'GET':
        id_tema = request.GET.get('id_tema')
        if not id_tema:
            return JsonResponse({'status': 'error', 'message': 'ID de tema no proporcionado'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('SP_obtener_tema', [id_tema])
                tema = cursor.fetchone()
            return render(request, 'tema_detalle.html', {'tema': tema})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)




def autores_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'edit':
            return editar_autor(request)
        elif action == 'delete':
            return eliminar_autor(request)
        elif action == 'add':
            return agregar_autor(request)
    elif request.method == 'GET':
        if 'id_autor' in request.GET:
            return obtener_autor(request)
        else:
            autores = listado_autores()
            return render(request, 'autores.html', {'autores': autores})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def editar_autor(request):
    if request.method == 'POST':
        id_autor = request.POST.get('autor_id')
        primer_nombre = request.POST.get('primer_nombre')
        segundo_nombre = request.POST.get('segundo_nombre')

        if not id_autor:
            return JsonResponse({'status': 'error', 'message': 'ID del autor no proporcionado'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('SP_actualizar_autor', [
                    int(id_autor),
                    primer_nombre if primer_nombre else None,
                    segundo_nombre if segundo_nombre else None
                ])
            return redirect('autores')  
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def eliminar_autor(request):
    if request.method == 'POST':
        id_autor = request.POST.get('id_autor')
        
        if not id_autor:
            return JsonResponse({'status': 'error', 'message': 'ID del autor no proporcionado'}, status=400)
        
        try:
            with connection.cursor() as cursor:
                cursor.callproc('SP_eliminar_autor', [int(id_autor)])
            return redirect ('autores')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def agregar_autor(request):
    if request.method == 'POST':
        primer_nombre = request.POST.get('primer_nombre')
        segundo_nombre = request.POST.get('segundo_nombre')
        
        if not primer_nombre:
            return JsonResponse({'status': 'error', 'message': 'Primer nombre no proporcionado'}, status=400)
        if not segundo_nombre:
            return JsonResponse({'status': 'error', 'message': 'Segundo nombre no proporcionado'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('SP_insertar_autor', [primer_nombre, segundo_nombre])
            return redirect('autores')  
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def listado_autores():
    dsn = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    
    try:
        with connection.cursor() as cursor:
            out_cur = cursor.var(cx_Oracle.CURSOR)  
            try:
                cursor.callproc("SP_obtener_todos_los_autores", [out_cur])
                lista = []
                for fila in out_cur.getvalue():
                    lista.append({
                        'id_autor': fila[0],
                        'primer_nombre': fila[1],
                        'segundo_nombre': fila[2]
                    })
                return lista
            except cx_Oracle.DatabaseError as e:
                print("Error al ejecutar el procedimiento:", e)
                return []
    finally:
        connection.close()

def obtener_autor(request):
    if request.method == 'GET':
        id_autor = request.GET.get('id_autor')
        if not id_autor:
            return JsonResponse({'status': 'error', 'message': 'ID de autor no proporcionado'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('SP_obtener_autor', [id_autor])
                autor = cursor.fetchone()
            return render(request, 'autor_detalle.html', {'autor': autor})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
