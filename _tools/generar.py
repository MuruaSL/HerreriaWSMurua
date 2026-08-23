# -*- coding: utf-8 -*-
# =============================================================================
#  CUIDADO: este script SOBREESCRIBE index.html y todo pages/*.html.
#
#  Las paginas del sitio son HTML plano y se pueden editar a mano sin problema.
#  Este script existe solo por comodidad: si hay que tocar el menu, el pie o
#  agregar un rubro, conviene cambiarlo aca y regenerar, en vez de repetir el
#  mismo cambio en once archivos (que es lo que hizo que el pie dijera "2022"
#  durante cuatro anios).
#
#  Si editaste una pagina a mano y despues corres esto, perdes ese cambio.
#  Uso:  python3 _tools/generar.py
# =============================================================================
"""
Genera las paginas HTML del sitio de Herreria WS Murua.

La salida es HTML plano y estatico, sin framework ni dependencias: el repo
sigue siendo HTML a mano. Este script existe solo para no escribir trece veces
el mismo menu y el mismo pie, que es lo que hizo que el pie dijera "2022"
durante cuatro anios.
"""
import os, re, html

RAIZ = '/Users/leonardo/Desktop/HerreriaWSMurua'
os.chdir(RAIZ)

SITIO = 'https://herreria-ws-murua.vercel.app'
TEL_TXT = '351 509-0016'
WA_NUM = '5493515090016'

# Direccion de la ficha de Google. La web nunca la tuvo escrita: solo estaba
# implicita en el embed del mapa, y Google no puede leer una direccion de ahi.
CALLE = 'Felipe Boero 2318'
CP = 'X5010'
CIUDAD = 'Córdoba'
DIRECCION = f'{CALLE}, {CP} {CIUDAD}, Argentina'


def wa(texto):
    from urllib.parse import quote
    return f'https://api.whatsapp.com/send?phone={WA_NUM}&amp;text={quote(texto)}'


WA_GENERAL = wa('Hola Herrería WS Murua, vi la web y quería consultarles por un trabajo.')

# Ficha de Google del negocio. El CID sale del embed del mapa que ya usaba la
# web vieja; en decimal arma un enlace directo a la ficha y sus resenias.
GOOGLE_RESENAS = 'https://maps.google.com/?cid=%d' % int('46dbd73b835083a6', 16)
MENCION_REEL = 'https://www.instagram.com/reel/C15YsbaxzQX/'

# Resenias publicas de la ficha de Google del negocio, con nombre y estrellas.
# Nota: no se marcan como AggregateRating en el schema. Google no permite
# publicar en tu propio sitio, como datos estructurados, resenias tomadas de
# otra plataforma; se muestran como texto y se enlaza la ficha original.
PUNTAJE = '4,7'
CANT_RESENAS = 13

TESTIMONIOS = [
    ('El trabajo realizado es impecable con excelentes terminaciones, son muy '
     'profesionales y confiables, realizan trabajos personalizados hermosos y '
     'con excelentes precios', 'Rocío Sosa', 'Google'),
    ('Nos hicieron un portón automático desde cero. Muy buen precio. '
     'Gente seria. Lo recomiendo.', 'Fer Maristany', 'Google'),
    ('Los trabajos son muy buenos. Creativos. El precio acorde al trabajo. '
     'Recomendables!', 'Laura Viviana Olmedo', 'Google'),
    ('Excelentes, responsables, cumplidores, detallistas, para recomendar!',
     'Andrea Barrionuevo', 'Google'),
    ('Calidad y responsabilidad, precio razonable.', 'Kary Guzmán', 'Google'),
    ('Gente seria y responsable.', 'Miguel Emilio Maristany', 'Google'),
]

ESTRELLAS = '<span class="cita__estrellas" aria-hidden="true">★★★★★</span>'


def citas_html(cuantas=None):
    sel = TESTIMONIOS[:cuantas] if cuantas else TESTIMONIOS
    return '\n'.join(
        f'''        <figure class="cita revelar">
          {ESTRELLAS}<span class="visually-hidden">5 de 5 estrellas</span>
          <blockquote>&ldquo;{t}&rdquo;</blockquote>
          <figcaption>{a} · reseña en {f}</figcaption>
        </figure>''' for t, a, f in sel)


CITAS = citas_html(3)
CITAS_TODAS = citas_html()

# --------------------------------------------------------------------------
# Rubros. El orden es el del sitio: intencion de compra primero, respaldo
# fotografico como desempate.
# --------------------------------------------------------------------------
RUBROS = [
    dict(
        slug='rejas-y-portones',
        nombre='Rejas y portones',
        corto='Rejas y portones',
        carpetas=['rejas', 'barandas'],
        resumen='Rejas de seguridad, portones corredizos y barandas, hechos a medida del frente de tu casa.',
        titulo='Rejas y Portones a Medida en Córdoba',
        meta='Rejas de seguridad, portones corredizos y barandas a medida en Córdoba. '
             'Diseño propio, herrería artesanal y presupuesto sin cargo.',
        h1='Rejas y portones a medida',
        bajada='Seguridad que no parece una jaula. Trabajamos el diseño con vos '
               'para que la reja cuide tu casa y además le quede bien.',
        texto=[
            'Hacemos rejas de frente, rejas para ventanas, portones corredizos y de '
            'abrir, y barandas para escaleras y balcones. Todo a medida: tomamos las '
            'medidas en tu casa y fabricamos según el ancho real, no según un catálogo.',
            'Trabajamos el hierro con torsionados, macizos y detalles intermedios. '
            'Si tenés una idea o una foto de referencia, la usamos de punto de partida. '
            'Si no la tenés, te mostramos lo que hicimos y arrancamos de ahí.',
            'También hacemos portones automáticos desde cero, y adaptamos a corredizo '
            'un portón que ya tengas.',
        ],
        incluye=['Rejas de frente y de ventana', 'Portones corredizos y de abrir',
                 'Portones automáticos, hechos desde cero',
                 'Adaptación de portones existentes a corredizo',
                 'Barandas de escalera y balcón', 'Rejas anti-perro y con detalles torsionados',
                 'Terminación en pintura epoxi, al horno o antióxido'],
    ),
    dict(
        slug='muebles-a-medida',
        nombre='Muebles a medida',
        corto='Muebles a medida',
        carpetas=['muebles'],
        resumen='Mesas, escritorios, bibliotecas y racks combinando hierro y madera maciza.',
        titulo='Muebles a Medida en Hierro y Madera | Córdoba',
        meta='Muebles a medida en Córdoba: mesas de madera maciza con hierro, escritorios, '
             'bibliotecas, racks y botelleros. Diseño propio y fabricación artesanal.',
        h1='Muebles a medida',
        bajada='Hierro y madera maciza, en la medida exacta del espacio que tenés. '
               'Es lo que más nos piden y lo que más disfrutamos hacer.',
        texto=[
            'Mesas de comedor, escritorios, bibliotecas, mesas ratonas, racks, botelleros '
            'y muebles de apoyo. Combinamos estructura de hierro con madera maciza, que es '
            'la mezcla que mejor envejece y la que más nos identifica.',
            'Cada mueble sale de una medida concreta: el hueco que querés llenar, la altura '
            'de tu silla, el largo de la pared. No hay tamaños estándar.',
            'Trabajamos con distintos tipos de madera según el uso y el presupuesto, y '
            'también restauramos muebles de hierro o madera que ya tenés.',
        ],
        incluye=['Mesas de comedor y ratonas', 'Escritorios y mesas de trabajo',
                 'Bibliotecas y estanterías', 'Racks y muebles de apoyo',
                 'Botelleros y mobiliario decorativo', 'Restauración de muebles existentes'],
    ),
    dict(
        slug='cerramientos-y-aberturas',
        nombre='Cerramientos y aberturas',
        corto='Cerramientos',
        carpetas=['cerramientos'],
        resumen='Puertas, ventanas, mamparas y frentes de asador para cerrar galerías y quinchos.',
        titulo='Cerramientos y Aberturas a Medida | Herrería en Córdoba',
        meta='Cerramientos de galería y quincho, puertas corredizas y tipo granero, ventanas, '
             'mamparas de baño y frentes de asador a medida en Córdoba.',
        h1='Cerramientos y aberturas',
        bajada='Cerrar la galería, el quincho o el asador y ganar un ambiente nuevo '
               'sin obra húmeda.',
        texto=[
            'Fabricamos puertas corredizas, puertas tipo granero, ventanas, mamparas para '
            'baño, frentes de asador y cerramientos completos de galería. Resolvemos el '
            'cerramiento con la abertura que mejor funcione para el uso que le vas a dar.',
            'Es de los trabajos que más cambian una casa: un quincho abierto que se usa tres '
            'meses al año pasa a usarse todo el año.',
        ],
        incluye=['Cerramientos de galería y quincho', 'Puertas corredizas y tipo granero',
                 'Ventanas y puertas de hierro', 'Mamparas para baño',
                 'Frentes de asador y puertas guillotina',
                 'Puertas con material desplegado (rejilla) para ventilación'],
    ),
    dict(
        slug='techos-y-galerias',
        nombre='Techos y galerías',
        corto='Techos y galerías',
        carpetas=['techos', 'techosycerramientos'],
        resumen='Estructuras para cochera, galería y patio, con cenefa y chapa pintada.',
        titulo='Techos y Galerías Metálicas | Herrería en Córdoba',
        meta='Techos metálicos para cochera, galería y patio en Córdoba. Estructura de hierro, '
             'cenefa y chapa pintada. Presupuesto sin cargo.',
        h1='Techos y galerías',
        bajada='Para el auto, para el patio o para sumarle sombra a la casa. '
               'Estructura de hierro y chapa, calculada para durar.',
        texto=[
            'Hacemos techos de cochera, galerías, aleros y estructuras para patio. La '
            'estructura se calcula según la luz que tenga que cubrir y la terminación se '
            'define con vos: cenefa gruesa o liviana, chapa pintada del color que elijas.',
            'Va desde el techo simple para cubrir un auto hasta la galería completa con '
            'columnas, que es donde después entra el asador o el deck.',
            'Si te preocupa por dónde escurre la lluvia, podemos sumar zinguería y '
            'canaletas de chapa hechas a medida del techo. Es un adicional sobre el '
            'techo base, no algo que venga incluido siempre.',
        ],
        incluye=['Techos de cochera', 'Galerías y aleros', 'Estructuras para patio',
                 'Cenefas y terminaciones', 'Chapa pintada a elección',
                 'Zinguería y canaletas a medida (opcional)'],
    ),
    dict(
        slug='espejos',
        nombre='Espejos',
        corto='Espejos',
        carpetas=['espejos'],
        resumen='Espejos con marco de hierro, en cualquier medida, con opción retroiluminada.',
        titulo='Espejos con Marco de Hierro a Medida | Córdoba',
        meta='Espejos a medida con marco de hierro en Córdoba: de pie, de baño, arcos y '
             'espejos retroiluminados. Cualquier medida y terminación.',
        h1='Espejos con marco de hierro',
        bajada='En la medida que necesites, con el marco que quieras. Es la pieza '
               'más simple de encargar y la que más cambia un ambiente.',
        texto=[
            'Fabricamos espejos de cuerpo entero, de baño, de arco y con formas especiales, '
            'siempre con marco de hierro hecho a medida. También hacemos espejos '
            'retroiluminados con luz LED, que quedan muy bien en baños y entradas.',
            'Trabajamos con un vidriero de primera calidad, que además de las formas '
            'clásicas hace diseños especiales: espejos tipo ameba o repartidos en piezas '
            'más chicas. También se puede pedir el vidrio con alguna característica '
            'particular, como espejado o ahumado; consultanos según lo que busques.',
            'Al ser fabricación propia, la medida la ponés vos: no dependés de lo que haya '
            'en stock.',
        ],
        incluye=['Espejos de cuerpo entero', 'Espejos de baño y tocador',
                 'Marcos tipo arco y formas especiales', 'Espejos retroiluminados con LED',
                 'Diseños especiales: forma ameba, en piezas repartidas',
                 'Cualquier medida a pedido'],
    ),
    dict(
        slug='decks',
        nombre='Decks',
        corto='Decks',
        carpetas=['decks'],
        resumen='Decks de madera para pileta, patio y galería, con estructura tratada.',
        titulo='Decks de Madera para Pileta y Patio | Córdoba',
        meta='Decks de madera a medida en Córdoba para pileta, patio y galería. '
             'Estructura tratada y terminación a elección.',
        h1='Decks de madera',
        bajada='Alrededor de la pileta, en el patio o en la galería. La madera cambia '
               'por completo cómo se usa un espacio exterior.',
        texto=[
            'Hacemos decks para pileta, patio y galería, con estructura tratada para '
            'intemperie y la terminación que elijas. Resolvemos también los desniveles, '
            'los escalones y los bordes de pileta.',
            'Es un trabajo con mucha demanda en temporada, y no manejamos una '
            'anticipación fija: cuanto antes nos consultes, mejor margen tenemos para '
            'coordinar la fecha.',
            'La madera necesita mantenimiento: un hidrolaqueado (o similar) una vez '
            'por año la mantiene protegida y con buen color. No es algo que se ponga y '
            'se olvide.',
        ],
        incluye=['Decks perimetrales de pileta', 'Decks de patio y galería',
                 'Escalones y desniveles', 'Estructura tratada para intemperie',
                 'Terminación y color a elección'],
    ),
    dict(
        slug='elementos-de-cocina',
        nombre='Elementos de cocina',
        corto='Elem. de cocina',
        carpetas=['elemCocina'],
        resumen='Parrillas, accesorios de asador y piezas de hierro para la cocina.',
        titulo='Parrillas y Elementos de Cocina en Hierro | Córdoba',
        meta='Parrillas, accesorios de asador y elementos de cocina en hierro, hechos a '
             'medida en Córdoba.',
        h1='Elementos de cocina',
        bajada='Parrillas, accesorios de asador y piezas de hierro para la cocina, '
               'hechas en la medida de tu asador.',
        texto=[
            'Fabricamos parrillas a medida, accesorios de asador y piezas de hierro para la '
            'cocina. Si tenés el asador construido y no encontrás la parrilla del tamaño '
            'justo, la hacemos.',
            'Se combina muy bien con el frente de asador, que hacemos en el mismo trabajo.',
        ],
        incluye=['Parrillas a medida, con varillas o chapa calada', 'Accesorios de asador',
                 'Piezas de hierro para cocina', 'Complementos de frente de asador'],
    ),
]

OTROS = ['otros_trabajos']

# --------------------------------------------------------------------------
# utilidades
# --------------------------------------------------------------------------

def fotos_de(carpetas):
    """Fotos de un rubro. Las que llevan el anio en el nombre son las ultimas
    incorporadas y van primero: es el trabajo mas reciente del taller."""
    nuevas, viejas = [], []
    for c in carpetas:
        d = f'img/trabajos/{c}'
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.lower().endswith('.webp'):
                continue
            (nuevas if '-2026-' in f else viejas).append(f'{d}/{f}')
    return nuevas + viejas


def url(base, ruta):
    return base + ruta.replace(' ', '%20')


def alt_de(ruta, rubro):
    return f'Trabajo de {rubro.lower()} realizado por Herrería WS Murua en Córdoba'


ICONO_WA = ('<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><path d="M16 3C8.8 3 3 8.8 3 '
            '16c0 2.3.6 4.5 1.7 6.4L3 29l6.8-1.8c1.9 1 4 1.6 6.2 1.6 7.2 0 13-5.8 13-13S23.2 3 16 3zm0 '
            '23.6c-2 0-3.9-.5-5.5-1.5l-.4-.2-4 1.1 1.1-3.9-.3-.4c-1.1-1.7-1.6-3.6-1.6-5.6C5.3 10.1 10.1 '
            '5.3 16 5.3S26.7 10.1 26.7 16 21.9 26.6 16 26.6zm5.9-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2c-.2.'
            '3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.3-.2-.3 0-.5.1-.7l.5-.6c'
            '.2-.2.2-.3.3-.5.1-.2 0-.4 0-.6s-.7-1.7-1-2.3c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 '
            '1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.9 5.2.8.4 1.5.6 2 .7.8.3 1.6.2 2.2.1.7-.1 2-.8 '
            '2.3-1.6.3-.8.3-1.5.2-1.6-.1-.2-.3-.3-.6-.4z"/></svg>')

ICONO_IG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.3 '
            '2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c0 1.2-.2 '
            '1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c'
            '-1.2 0-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 '
            '15.2 2.2 12s0-3.6.1-4.9c0-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 '
            '2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 2c-3.1 0-3.5 0-4.7.1-1.1 0-1.7.2-2.1.3-.5.2-.9.4-1.2.8-.4'
            '.3-.6.7-.8 1.2-.1.4-.3 1-.3 2.1-.1 1.2-.1 1.6-.1 4.7s0 3.5.1 4.7c0 1.1.2 1.7.3 2.1.2.5.4.9'
            '.8 1.2.3.4.7.6 1.2.8.4.1 1 .3 2.1.3 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1.1 0 1.7-.2 2.1-.3.5-.2'
            '.9-.4 1.2-.8.4-.3.6-.7.8-1.2.1-.4.3-1 .3-2.1.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c0-1.1-.2-1.7-.3'
            '-2.1-.2-.5-.4-.9-.8-1.2-.3-.4-.7-.6-1.2-.8-.4-.1-1-.3-2.1-.3-1.2-.1-1.6-.1-4.7-.1zm0 3.4a5.'
            '4 5.4 0 1 1 0 10.8 5.4 5.4 0 0 1 0-10.8zm0 8.9a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zm6.9-9.1a'
            '1.3 1.3 0 1 1-2.5 0 1.3 1.3 0 0 1 2.5 0z"/></svg>')

ICONO_FB = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2'
            '.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2'
            '.4v7A10 10 0 0 0 22 12z"/></svg>')


def cabeza(base, titulo, meta, ruta, og_img, extra=''):
    return f'''<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{meta}">
<meta name="author" content="Leonardo Murua">
<link rel="canonical" href="{SITIO}{ruta}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#15171A">
<meta name="geo.region" content="AR-X">
<meta name="geo.placename" content="Córdoba">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="Herrería WS Murua">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{meta}">
<meta property="og:url" content="{SITIO}{ruta}">
<meta property="og:image" content="{SITIO}{og_img.replace(' ', '%20')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{meta}">
<meta name="twitter:image" content="{SITIO}{og_img.replace(' ', '%20')}">
<link rel="icon" type="image/webp" href="{url(base, 'img/icon/logo.webp')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Karla:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{url(base, 'css/site.css')}">
{extra}</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
'''


def cabecera(base, actual):
    items = [('index.html', 'Inicio', 'inicio')]
    items += [(f'pages/{r["slug"]}.html', r['corto'], r['slug']) for r in RUBROS[:4]]
    items += [('pages/trabajos.html', 'Trabajos', 'trabajos'),
              ('pages/taller.html', 'El taller', 'taller'),
              ('pages/contacto.html', 'Contacto', 'contacto')]
    links = []
    for ruta, texto, clave in items:
        cur = ' aria-current="page"' if clave == actual else ''
        links.append(f'<a href="{url(base, ruta)}"{cur}>{texto}</a>')
    nav = '\n        '.join(links)
    return f'''<header class="cabecera">
  <div class="wrap cabecera__fila">
    <a class="marca" href="{url(base, 'index.html')}">
      <img src="{url(base, 'img/icon/logo.webp')}" alt="" width="38" height="38">
      <span>Herrería WS Murua<small>Herrería y carpintería · Córdoba</small></span>
    </a>
    <button class="hamburguesa" type="button" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v2H3V6zm0 5h18v2H3v-2zm0 5h18v2H3v-2z"/></svg>
    </button>
    <nav class="nav" id="menu" aria-label="Principal">
        {nav}
    </nav>
    <a class="btn btn--principal" href="{WA_GENERAL}" target="_blank" rel="noopener">{ICONO_WA} Presupuesto</a>
  </div>
</header>
'''


def pie(base):
    r_links = '\n        '.join(
        f'<li><a href="{url(base, "pages/" + r["slug"] + ".html")}">{r["nombre"]}</a></li>'
        for r in RUBROS)
    return f'''<footer class="pie">
  <div class="wrap pie__grid">
    <div>
      <h2>Rubros</h2>
      <ul>
        {r_links}
      </ul>
    </div>
    <div>
      <h2>El negocio</h2>
      <ul>
        <li><a href="{url(base, 'pages/taller.html')}">El taller</a></li>
        <li><a href="{url(base, 'pages/trabajos.html')}">Trabajos realizados</a></li>
        <li><a href="{url(base, 'pages/contacto.html')}">Contacto</a></li>
      </ul>
    </div>
    <div>
      <h2>Escribinos</h2>
      <ul>
        <li><a href="{WA_GENERAL}" target="_blank" rel="noopener">WhatsApp {TEL_TXT}</a></li>
        <li><a href="{GOOGLE_RESENAS}" target="_blank" rel="noopener">{DIRECCION}</a></li>
        <li>Presupuesto sin cargo</li>
      </ul>
      <div class="pie__social">
        <a href="https://www.instagram.com/herreria_wsmurua/" target="_blank" rel="noopener" aria-label="Instagram">{ICONO_IG}</a>
        <a href="https://www.facebook.com/HerreriaMuruaHM" target="_blank" rel="noopener" aria-label="Facebook">{ICONO_FB}</a>
        <a href="{WA_GENERAL}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICONO_WA}</a>
      </div>
    </div>
  </div>
  <div class="wrap pie__legal">
    © 2026 Herrería WS Murua. Desarrollado por
    <a href="https://murua.com.ar" target="_blank" rel="author noopener">Leonardo Murua</a>
    (<a href="mailto:leonardo@murua.com.ar">leonardo@murua.com.ar</a>).
  </div>
</footer>
'''


def cierre(base, script_extra=''):
    return f'''<a class="wa-flotante" href="{WA_GENERAL}" target="_blank" rel="noopener" aria-label="Escribirnos por WhatsApp">
  {ICONO_WA}<span class="wa-flotante__texto">WhatsApp</span>
</a>
<script>
document.documentElement.classList.add('js');
(function () {{
  var b = document.querySelector('.hamburguesa'), n = document.getElementById('menu');
  if (b && n) {{
    var chico = matchMedia('(max-width: 950px)');
    var cerrar = function () {{ if (chico.matches) {{ n.hidden = true; b.setAttribute('aria-expanded', 'false'); }} }};
    cerrar(); chico.addEventListener('change', cerrar);
    b.addEventListener('click', function () {{
      var abierto = !n.hidden;
      n.hidden = abierto;
      b.setAttribute('aria-expanded', String(!abierto));
    }});
  }}
  var obj = document.querySelectorAll('.revelar');
  if (!obj.length) return;
  if (!('IntersectionObserver' in window)) {{
    obj.forEach(function (e) {{ e.classList.add('visible'); }}); return;
  }}
  var io = new IntersectionObserver(function (es) {{
    es.forEach(function (e) {{
      if (e.isIntersecting) {{ e.target.classList.add('visible'); io.unobserve(e.target); }}
    }});
  }}, {{ rootMargin: '0px 0px -8%' }});
  obj.forEach(function (e) {{ io.observe(e); }});
}})();
</script>
{script_extra}</body>
</html>
'''


def galeria(base, fotos, rubro_nombre, desde=0):
    out = []
    for i, f in enumerate(fotos):
        carga = 'eager' if (i + desde) < 3 else 'lazy'
        prio = ' fetchpriority="high"' if (i + desde) == 0 else ''
        out.append(
            f'    <img src="{url(base, f)}" alt="{alt_de(f, rubro_nombre)}" '
            f'width="1200" height="1200" loading="{carga}" decoding="async"{prio}>')
    return '\n'.join(out)


SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "name": "Herrería WS Murua",
  "alternateName": "Herrería y Muebles Murua",
  "description": "Herrería y carpintería a medida en Córdoba: rejas, portones, cerramientos, techos, decks, espejos y muebles en hierro y madera.",
  "url": "%(s)s/",
  "logo": "%(s)s/img/icon/logo.webp",
  "image": "%(s)s/img/trabajos/fotos_index/reja_index.webp",
  "telephone": "+%(t)s",
  "priceRange": "$$",
  "address": { "@type": "PostalAddress", "streetAddress": "%(calle)s", "postalCode": "%(cp)s", "addressLocality": "Córdoba", "addressRegion": "Córdoba", "addressCountry": "AR" },
  "geo": { "@type": "GeoCoordinates", "latitude": -31.4356545, "longitude": -64.2456634 },
  "areaServed": { "@type": "City", "name": "Córdoba" },
  "sameAs": ["https://www.instagram.com/herreria_wsmurua/", "https://www.facebook.com/HerreriaMuruaHM"],
  "hasOfferCatalog": {
    "@type": "OfferCatalog", "name": "Servicios",
    "itemListElement": [%(items)s]
  }
}
</script>
''' % dict(s=SITIO, t=WA_NUM, calle=CALLE, cp=CP, items=', '.join(
    '{"@type":"Offer","itemOffered":{"@type":"Service","name":"%s"}}' % r['nombre'] for r in RUBROS))


def tarjetas_rubro(base):
    out = []
    for r in RUBROS:
        f = fotos_de(r['carpetas'])
        portada = f[0] if f else 'img/trabajos/fotos_index/reja_index.webp'
        out.append(f'''      <a class="rubro revelar" href="{url(base, 'pages/' + r['slug'] + '.html')}">
        <img class="rubro__foto" src="{url(base, portada)}" alt="{alt_de(portada, r['nombre'])}" width="1200" height="1200" loading="lazy" decoding="async">
        <div class="rubro__cuerpo">
          <div class="rubro__t">{r['nombre']}</div>
          <p class="rubro__d">{r['resumen']}</p>
          <span class="rubro__mas">Ver trabajos &rarr;</span>
        </div>
      </a>''')
    return '\n'.join(out)


# ------------------------------------------------------------------ INICIO
def pagina_inicio():
    base = './'
    hero = 'img/trabajos/fotos_index/reja_index.webp'
    h = cabeza(base,
        'Herrería y Carpintería a Medida en Córdoba | WS Murua',
        'Herrería y carpintería a medida en Córdoba: rejas, portones, cerramientos, techos, '
        'decks, espejos y muebles en hierro y madera. Presupuesto sin cargo por WhatsApp.',
        '/', hero, extra=SCHEMA)
    h += cabecera(base, 'inicio')
    h += f'''<main id="contenido">

  <section class="hero">
    <img class="hero__foto" src="{url(base, hero)}" alt="" width="1200" height="1200" fetchpriority="high" decoding="async">
    <div class="wrap hero__contenido">
      <p class="eyebrow">Córdoba, Argentina</p>
      <h1>Hierro y madera, en la medida exacta de tu casa</h1>
      <p class="hero__bajada">Somos un taller familiar. Hacemos rejas, portones, cerramientos,
        techos, decks, espejos y muebles a medida. Cada trabajo arranca tomando las medidas
        en tu casa, no eligiendo de un catálogo.</p>
      <div class="hero__acciones">
        <a class="btn btn--sobre-foto" href="{WA_GENERAL}" target="_blank" rel="noopener">{ICONO_WA} Pedir presupuesto</a>
        <a class="btn btn--linea" href="{url(base, 'pages/trabajos.html')}">Ver trabajos</a>
      </div>
    </div>
  </section>

  <div class="tira">
    <div class="tira__item"><div class="tira__d">Presupuesto sin cargo</div><div class="tira__t">Te pasamos el precio antes de que decidas</div></div>
    <div class="tira__item"><div class="tira__d">Todo a medida</div><div class="tira__t">Fabricación propia, sin medidas estándar</div></div>
    <div class="tira__item"><div class="tira__d">Herrero Amigo</div><div class="tira__t">Distinción de ACERCO</div></div>
    <div class="tira__item"><div class="tira__d">Tres barrios privados</div><div class="tira__t">Somos su herrería de confianza</div></div>
    <div class="tira__item"><div class="tira__d">Taller familiar</div><div class="tira__t">Hablás siempre con quien hace el trabajo</div></div>
  </div>

  <section class="seccion">
    <div class="wrap">
      <p class="eyebrow">Qué hacemos</p>
      <h2 class="titulo-seccion">Siete rubros, un solo taller</h2>
      <p class="bajada">Trabajamos el hierro y la madera. Elegí el rubro y mirá lo que hicimos.</p>
      <div class="rubros">
{tarjetas_rubro(base)}
      </div>
    </div>
  </section>

  <section class="seccion" style="background: var(--surface-2);">
    <div class="wrap">
      <p class="eyebrow">Lo que dicen</p>
      <h2 class="titulo-seccion">Clientes de Córdoba</h2>
      <div class="puntaje">
        <span class="puntaje__n">{PUNTAJE}</span>
        <span class="puntaje__e" aria-hidden="true">★★★★★</span>
        <span class="puntaje__t">{CANT_RESENAS} opiniones en Google</span>
      </div>
      <div class="citas">
{CITAS}
      </div>
      <div style="margin-top:2rem">
        <a class="btn btn--linea" href="{GOOGLE_RESENAS}" target="_blank" rel="noopener">Ver todas las reseñas en Google &rarr;</a>
      </div>
    </div>
  </section>

  <section class="seccion">
    <div class="wrap">
      <div class="cta">
        <h2>Contanos qué necesitás</h2>
        <p>Mandanos una foto del lugar y las medidas aproximadas. Con eso ya te podemos orientar.</p>
        <a class="btn btn--principal" href="{WA_GENERAL}" target="_blank" rel="noopener">{ICONO_WA} Escribinos por WhatsApp</a>
      </div>
    </div>
  </section>

</main>
'''
    h += pie(base) + cierre(base)
    return 'index.html', h


# ------------------------------------------------------------------ RUBRO
def pagina_rubro(r):
    base = '../'
    fotos = fotos_de(r['carpetas'])
    hero = fotos[0] if fotos else 'img/trabajos/fotos_index/reja_index.webp'
    resto = fotos[1:] if len(fotos) > 1 else fotos
    otros = [x for x in RUBROS if x['slug'] != r['slug']][:3]
    otros_html = '\n'.join(
        f'''      <a class="rubro" href="{url(base, 'pages/' + o['slug'] + '.html')}">
        <img class="rubro__foto" src="{url(base, (fotos_de(o['carpetas']) or [hero])[0])}" alt="{alt_de('', o['nombre'])}" width="1200" height="1200" loading="lazy" decoding="async">
        <div class="rubro__cuerpo"><div class="rubro__t">{o['nombre']}</div>
        <span class="rubro__mas">Ver trabajos &rarr;</span></div>
      </a>''' for o in otros)
    incluye = '\n'.join(f'        <li>{i}</li>' for i in r['incluye'])
    parrafos = '\n'.join(f'        <p>{p}</p>' for p in r['texto'])
    wa_rubro = wa(f'Hola Herrería WS Murua, quería consultarles por {r["nombre"].lower()}.')

    h = cabeza(base, r['titulo'], r['meta'], f'/pages/{r["slug"]}.html', '/' + hero)
    h += cabecera(base, r['slug'])
    h += f'''<main id="contenido">

  <section class="hero hero--interno">
    <img class="hero__foto" src="{url(base, hero)}" alt="" width="1200" height="1200" fetchpriority="high" decoding="async">
    <div class="wrap hero__contenido">
      <p class="eyebrow">Herrería WS Murua · Córdoba</p>
      <h1>{r['h1']}</h1>
      <p class="hero__bajada">{r['bajada']}</p>
      <div class="hero__acciones">
        <a class="btn btn--sobre-foto" href="{wa_rubro}" target="_blank" rel="noopener">{ICONO_WA} Consultar por este trabajo</a>
      </div>
    </div>
  </section>

  <section class="seccion">
    <div class="wrap duo">
      <div class="prosa">
        <p class="eyebrow">Cómo trabajamos</p>
        <h2 class="titulo-seccion">{r['nombre']}</h2>
{parrafos}
      </div>
      <div>
        <p class="eyebrow">Incluye</p>
        <ul class="lista-marcas">
{incluye}
        </ul>
      </div>
    </div>
  </section>

  <section class="seccion" style="background: var(--surface-2);">
    <div class="wrap">
      <p class="eyebrow">{len(fotos)} trabajos</p>
      <h2 class="titulo-seccion">Lo que hicimos</h2>
      <div class="galeria">
{galeria(base, resto, r['nombre'], desde=1)}
      </div>
    </div>
  </section>

  <section class="seccion">
    <div class="wrap">
      <div class="cta">
        <h2>¿Te interesa algo así?</h2>
        <p>Mandanos una foto del lugar y las medidas aproximadas. Te pasamos el presupuesto sin cargo.</p>
        <a class="btn btn--principal" href="{wa_rubro}" target="_blank" rel="noopener">{ICONO_WA} Pedir presupuesto</a>
      </div>
    </div>
  </section>

  <section class="seccion">
    <div class="wrap">
      <p class="eyebrow">También hacemos</p>
      <h2 class="titulo-seccion">Otros rubros</h2>
      <div class="rubros">
{otros_html}
      </div>
    </div>
  </section>

</main>
'''
    h += pie(base) + cierre(base)
    return f'pages/{r["slug"]}.html', h


# ------------------------------------------------------------------ TRABAJOS
def pagina_trabajos():
    base = '../'
    grupos = [(r['nombre'], r['slug'], fotos_de(r['carpetas'])) for r in RUBROS]
    extra = fotos_de(OTROS)
    if extra:
        grupos.append(('Otros trabajos', None, extra))
    total = sum(len(g[2]) for g in grupos)
    hero = 'img/trabajos/muebles/' + sorted(os.listdir('img/trabajos/muebles'))[0]

    filtros = ['<a class="btn btn--linea" href="#todos" data-filtro="todos">Todos</a>']
    filtros += [f'<a class="btn btn--linea" href="#{s or "otros"}" data-filtro="{s or "otros"}">{n}</a>'
                for n, s, _ in grupos]

    bloques = []
    for n, s, fs in grupos:
        ficha = (f'<a class="btn btn--linea" href="{url(base, "pages/" + s + ".html")}">Ver el rubro &rarr;</a>'
                 if s else '')
        bloques.append(f'''  <section class="seccion" id="{s or 'otros'}">
    <div class="wrap">
      <p class="eyebrow">{len(fs)} trabajos</p>
      <h2 class="titulo-seccion">{n}</h2>
      <div style="margin-top:1.2rem">{ficha}</div>
      <div class="galeria">
{galeria(base, fs, n, desde=3)}
      </div>
    </div>
  </section>''')

    h = cabeza(base, 'Trabajos Realizados | Herrería WS Murua — Córdoba',
        f'Galería completa de {total} trabajos realizados en Córdoba: rejas, muebles a medida, '
        'cerramientos, techos, espejos, decks y elementos de cocina.',
        '/pages/trabajos.html', '/' + hero)
    h += cabecera(base, 'trabajos')
    h += f'''<main id="contenido">

  <section class="hero hero--interno">
    <img class="hero__foto" src="{url(base, hero)}" alt="" width="1200" height="1200" fetchpriority="high" decoding="async">
    <div class="wrap hero__contenido">
      <p class="eyebrow">Herrería WS Murua · Córdoba</p>
      <h1>Trabajos realizados</h1>
      <p class="hero__bajada">{total} trabajos hechos en Córdoba, ordenados por rubro.
        Todo lo que ves acá lo fabricamos nosotros.</p>
      <div class="hero__acciones" style="gap:.5rem">
        {' '.join(filtros[1:])}
      </div>
    </div>
  </section>

{chr(10).join(bloques)}

  <section class="seccion">
    <div class="wrap">
      <div class="cta">
        <h2>¿Viste algo parecido a lo que necesitás?</h2>
        <p>Mandanos la foto por WhatsApp y te decimos si se puede hacer igual y cuánto sale.</p>
        <a class="btn btn--principal" href="{WA_GENERAL}" target="_blank" rel="noopener">{ICONO_WA} Escribinos</a>
      </div>
    </div>
  </section>

</main>
'''
    h += pie(base) + cierre(base)
    return 'pages/trabajos.html', h


# ------------------------------------------------------------------ TALLER
def pagina_taller():
    base = '../'
    hero = 'img/trabajos/muebles/' + sorted(os.listdir('img/trabajos/muebles'))[3]
    muestra = (fotos_de(['rejas'])[:2] + fotos_de(['muebles'])[:2]
               + fotos_de(['techos'])[:1] + fotos_de(['espejos'])[:1])

    h = cabeza(base, 'El Taller | Herrería WS Murua — Córdoba',
        'Herrería WS Murua es un taller familiar de Córdoba. Nuestra historia, cómo trabajamos '
        'y la distinción Herrero Amigo de ACERCO.',
        '/pages/taller.html', '/' + hero)
    h += cabecera(base, 'taller')
    h += f'''<main id="contenido">

  <section class="hero hero--interno">
    <img class="hero__foto" src="{url(base, hero)}" alt="" width="1200" height="1200" fetchpriority="high" decoding="async">
    <div class="wrap hero__contenido">
      <p class="eyebrow">Quiénes somos</p>
      <h1>Karina y Walter, un taller familiar en Córdoba</h1>
      <p class="hero__bajada">Empezamos por necesidad y seguimos por gusto. Hoy hacemos
        hierro y madera a medida para casas de toda la ciudad.</p>
    </div>
  </section>

  <section class="seccion">
    <div class="wrap prosa">
      <p class="eyebrow">La historia</p>
      <h2 class="titulo-seccion">Empezó como una salida y quedó como oficio</h2>
      <p>Somos <strong>Karina y Walter Murua</strong>. Herrería WS Murua nació como
        respuesta a una crisis laboral que nos afectó directamente, y decidimos
        convertirla en una oportunidad: armar un emprendimiento familiar.</p>
      <p>La pasión por las tareas manuales y la creatividad se potenciaron con el proyecto,
        y nos permitieron aprender y crecer gracias a las exigencias y las ideas de cada
        cliente. Muchos de los trabajos que ves en la web salieron de algo que alguien nos
        pidió y no sabíamos si podíamos hacer.</p>
      <p>Somos un taller chico, y eso tiene una ventaja concreta: hablás siempre con la
        persona que va a hacer el trabajo. No hay vendedor en el medio.</p>
    </div>
  </section>

  <section class="seccion" style="background: var(--surface-2);">
    <div class="wrap duo">
      <div>
        <img src="{url(base, 'img/galardones/1.webp')}" alt="ACERCO distingue a Herrería Murua como Herrero Amigo, sobre un frente de asador fabricado por el taller" width="1200" height="1200" loading="lazy" decoding="async">
      </div>
      <div class="prosa">
        <p class="eyebrow">Reconocimiento</p>
        <h2 class="titulo-seccion">Herrero Amigo</h2>
        <p>ACERCO nos nombró colaboradores destacados con la distinción
          <strong>Herrero Amigo</strong>. Es un reconocimiento del sector, no una
          autodefinición: lo da una empresa que trabaja con herreros de toda la provincia.</p>
        <p>También somos los herreros de confianza de
          <strong>tres barrios privados de Córdoba</strong>, que es la forma más concreta
          que tenemos de decir que el trabajo se sostiene en el tiempo.</p>
        <p><a href="{GOOGLE_RESENAS}" target="_blank" rel="noopener">Mirá nuestras reseñas en Google &rarr;</a></p>
      </div>
    </div>
  </section>

  <section class="seccion">
    <div class="wrap">
      <p class="eyebrow">Lo que dicen</p>
      <h2 class="titulo-seccion">Clientes que nos recomiendan</h2>
      <p class="bajada">Reseñas publicadas por clientes en nuestra ficha de Google.</p>
      <div class="puntaje">
        <span class="puntaje__n">{PUNTAJE}</span>
        <span class="puntaje__e" aria-hidden="true">★★★★★</span>
        <span class="puntaje__t">{CANT_RESENAS} opiniones · <a href="{GOOGLE_RESENAS}" target="_blank" rel="noopener">verlas en Google</a></span>
      </div>
      <div class="citas">
{CITAS_TODAS}
      </div>
      <figure class="captura-testimonio" style="margin-top:2.5rem">
        <img src="{url(base, 'img/galardones/4.webp')}" alt="Clienta agradeciendo en Instagram el escritorio que le fabricó Herrería WS Murua" width="1200" height="1200" loading="lazy" decoding="async">
        <figcaption>Así nos lo agradeció una clienta en su Instagram.</figcaption>
      </figure>
    </div>
  </section>

  <section class="seccion" style="background: var(--surface-2);">
    <div class="wrap">
      <p class="eyebrow">Menciones</p>
      <h2 class="titulo-seccion">Nos nombraron en Instagram</h2>
      <div class="mencion revelar">
        <div class="mencion__cuerpo">
          <p class="mencion__quien">Nazarena Vélez <span class="mencion__verificada" title="Cuenta verificada" aria-label="Cuenta verificada">✓</span></p>
          <p class="mencion__texto">Nos mencionó en un video de su cuenta, y le agradecimos
            desde la nuestra. Está publicado en su perfil de Instagram.</p>
          <a class="btn btn--linea" href="{MENCION_REEL}" target="_blank" rel="noopener">
            Ver la publicación en Instagram &rarr;
          </a>
        </div>
      </div>
    </div>
  </section>

  <section class="seccion">
    <div class="wrap">
      <p class="eyebrow">Cómo trabajamos</p>
      <h2 class="titulo-seccion">De la consulta al trabajo terminado</h2>
      <div class="duo" style="margin-top:2rem">
        <ul class="lista-marcas">
          <li><strong>Nos escribís por WhatsApp</strong> con una foto del lugar y las medidas aproximadas.</li>
          <li><strong>Vamos a tomar medidas</strong> nosotros mismos, en la mayoría de los casos.</li>
          <li><strong>Te pasamos el presupuesto</strong> sin cargo y sin compromiso.</li>
        </ul>
        <ul class="lista-marcas">
          <li><strong>Fabricamos en el taller</strong>, con la medida real de tu casa.</li>
          <li><strong>Instalamos</strong> y dejamos el trabajo terminado.</li>
          <li><strong>Lo publicamos</strong> en Instagram, con tu permiso.</li>
        </ul>
      </div>
      <p class="prosa" style="margin-top:1.5rem;color:var(--ink-2)">
        Preferimos medir nosotros: hasta una cinta métrica da medidas distintas según
        quién mida, y esa diferencia después se nota en el trabajo terminado. Para cosas
        puntuales —una mesa, por ejemplo, no algo como un ropero empotrado— y si ya tenés
        las medidas seguras, o un plano de arquitecto, también trabajamos con eso.
      </p>
      <p class="prosa" style="margin-top:.8rem;color:var(--ink-2)">
        Los plazos varían mucho según el trabajo: te decimos un tiempo estimado
        cuando pasamos el presupuesto, no antes.
      </p>
    </div>
  </section>

  <section class="seccion" style="background: var(--surface-2);">
    <div class="wrap">
      <p class="eyebrow">Materiales</p>
      <h2 class="titulo-seccion">Herrería y carpintería, con las herramientas para las dos</h2>
      <p class="bajada" style="font-size:var(--step-0)">Trabajamos con todo tipo de metal y de madera,
        y adaptamos las herramientas y la terminación a lo que haga falta.</p>
      <div class="duo" style="margin-top:1.5rem">
        <ul class="lista-marcas">
          <li><strong>Caños, ángulos, chapa calada y material desplegado</strong>, según lo que pida cada pieza.</li>
          <li><strong>Pintura epoxi, al horno o antióxido</strong>, la que corresponda al uso.</li>
          <li><strong>Oxidato</strong>: una terminación de óxido controlado, sellada con barniz, para quien busca ese aspecto.</li>
        </ul>
        <ul class="lista-marcas">
          <li><strong>Todo tipo de madera</strong>, según el uso y el presupuesto.</li>
          <li><strong>Restauración</strong> de piezas de hierro o madera que ya tenés.</li>
          <li>Herramientas propias para metal y para madera: no tercerizamos ninguna de las dos partes.</li>
        </ul>
      </div>
      <div class="nota revelar">
        <p class="nota__titulo">Un tip contra la inflación</p>
        <p class="nota__texto">Si te preocupa que el precio de los materiales suba antes de
          arrancar, podés comprarlos vos o dejar una reserva en la casa de materiales apenas
          cerramos el presupuesto: eso te congela el precio hasta que empecemos el trabajo.
          No es obligatorio, es una opción. Como tenemos bastante trabajo entre manos, ya no
          nos queda lugar en el taller para guardar el material de todos los clientes al
          mismo tiempo.</p>
      </div>
    </div>
  </section>

  <section class="seccion" style="background: var(--surface-2);">
    <div class="wrap">
      <p class="eyebrow">Nuestro trabajo</p>
      <h2 class="titulo-seccion">Algunas cosas que hicimos</h2>
      <div class="galeria">
{galeria(base, muestra, 'trabajos varios', desde=3)}
      </div>
      <div style="margin-top:2rem">
        <a class="btn btn--linea" href="{url(base, 'pages/trabajos.html')}">Ver todos los trabajos &rarr;</a>
      </div>
    </div>
  </section>

  <section class="seccion">
    <div class="wrap">
      <div class="cta">
        <h2>¿Arrancamos?</h2>
        <p>Contanos qué necesitás. El presupuesto no te cuesta nada.</p>
        <a class="btn btn--principal" href="{WA_GENERAL}" target="_blank" rel="noopener">{ICONO_WA} Escribinos por WhatsApp</a>
      </div>
    </div>
  </section>

</main>
'''
    h += pie(base) + cierre(base)
    return 'pages/taller.html', h


# ------------------------------------------------------------------ CONTACTO
def pagina_contacto():
    base = '../'
    hero = 'img/trabajos/rejas/' + sorted(os.listdir('img/trabajos/rejas'))[0]
    mapa = ('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d13616.873508254981!2d-64.24566336044921'
            '!3d-31.435654499999995!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9432a37dd1b1a475'
            '%3A0x46dbd73b835083a6!2sHerrer%C3%ADa_WsMurua!5e0!3m2!1ses-419!2sar!4v1674433110032!5m2!1ses-419!2sar')
    script = '''<script>
(function () {
  var f = document.getElementById('form-contacto');
  if (!f) return;
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(f);
    var t = 'Hola Herrería WS Murua!\\n\\n' +
            'Nombre: ' + (d.get('nombre') || '').trim() + '\\n' +
            'Contacto: ' + (d.get('contacto') || '').trim() + '\\n' +
            'Trabajo: ' + (d.get('rubro') || '').trim() + '\\n\\n' +
            (d.get('mensaje') || '').trim();
    window.open('https://api.whatsapp.com/send?phone=''' + WA_NUM + '''&text=' +
                encodeURIComponent(t), '_blank', 'noopener');
  });
})();
</script>
'''
    opciones = '\n'.join(f'            <option value="{r["nombre"]}">{r["nombre"]}</option>' for r in RUBROS)

    h = cabeza(base, 'Contacto y Presupuestos | Herrería WS Murua — Córdoba',
        f'Pedí tu presupuesto sin cargo de herrería o carpintería en Córdoba. Escribinos por '
        f'WhatsApp al {TEL_TXT}.',
        '/pages/contacto.html', '/' + hero)
    h += cabecera(base, 'contacto')
    h += f'''<main id="contenido">

  <section class="hero hero--interno">
    <img class="hero__foto" src="{url(base, hero)}" alt="" width="1200" height="1200" fetchpriority="high" decoding="async">
    <div class="wrap hero__contenido">
      <p class="eyebrow">Presupuesto sin cargo</p>
      <h1>Contanos qué necesitás</h1>
      <p class="hero__bajada">Lo más rápido es WhatsApp: mandanos una foto del lugar y las
        medidas aproximadas, y con eso ya te orientamos.</p>
      <div class="hero__acciones">
        <a class="btn btn--sobre-foto" href="{WA_GENERAL}" target="_blank" rel="noopener">{ICONO_WA} WhatsApp {TEL_TXT}</a>
      </div>
    </div>
  </section>

  <section class="seccion">
    <div class="wrap duo duo--texto-primero">
      <div>
        <p class="eyebrow">Formulario</p>
        <h2 class="titulo-seccion">O escribinos desde acá</h2>
        <p class="bajada" style="font-size:var(--step-0)">Completá los datos y se abre WhatsApp
          con el mensaje ya escrito.</p>
        <form class="form" id="form-contacto">
          <label class="campo">
            <span>Nombre</span>
            <input type="text" name="nombre" required placeholder="Tu nombre">
          </label>
          <label class="campo">
            <span>Teléfono o email</span>
            <input type="text" name="contacto" required placeholder="Para poder responderte">
          </label>
          <label class="campo">
            <span>Qué necesitás</span>
            <select name="rubro" style="font:inherit;padding:.8rem .9rem;border:1px solid var(--line);border-radius:4px;background:var(--surface);color:var(--ink)">
{opciones}
              <option value="Otro trabajo">Otro trabajo</option>
            </select>
          </label>
          <label class="campo">
            <span>Contanos un poco más</span>
            <textarea name="mensaje" required placeholder="Medidas aproximadas, dónde va, para cuándo lo necesitás..."></textarea>
          </label>
          <div>
            <button class="btn btn--principal" type="submit">{ICONO_WA} Enviar por WhatsApp</button>
          </div>
          <p class="form__nota">No guardamos tus datos: el mensaje va directo a nuestro WhatsApp.</p>
        </form>
      </div>
      <div>
        <p class="eyebrow">Dónde estamos</p>
        <h2 class="titulo-seccion">{CALLE}, {CIUDAD}</h2>
        <p class="bajada" style="font-size:var(--step-0)">Trabajamos en toda la ciudad de Córdoba
          y alrededores. Vamos a tomar las medidas a tu casa, sin cargo.</p>
        <div class="puntaje">
          <span class="puntaje__n">{PUNTAJE}</span>
          <span class="puntaje__e" aria-hidden="true">★★★★★</span>
          <span class="puntaje__t">{CANT_RESENAS} opiniones · <a href="{GOOGLE_RESENAS}" target="_blank" rel="noopener">ver en Google</a></span>
        </div>
        <div style="margin-top:1.5rem;border:1px solid var(--line);border-radius:4px;overflow:hidden">
          <iframe title="Ubicación de Herrería WS Murua en Google Maps" src="{mapa}"
                  width="600" height="380" style="border:0;width:100%;display:block"
                  allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>
    </div>
  </section>

</main>
'''
    h += pie(base) + cierre(base, script)
    return 'pages/contacto.html', h


# ------------------------------------------------------------------ main
def main():
    paginas = [pagina_inicio(), pagina_trabajos(), pagina_taller(), pagina_contacto()]
    paginas += [pagina_rubro(r) for r in RUBROS]
    os.makedirs('pages', exist_ok=True)
    for ruta, contenido in paginas:
        with open(ruta, 'w', encoding='utf-8') as fh:
            fh.write(contenido)
        print(f'  escrita  {ruta:44s} {len(contenido)//1024:3d} KB')
    print(f'\ntotal: {len(paginas)} paginas')


if __name__ == '__main__':
    main()
