# SEO Control — Guía de diseño

Herramienta interna de Paraty Tech para el control SEO de las webs de hoteles. Este documento describe la identidad visual y los patrones de interfaz para que cualquiera pueda replicar el mismo aspecto corporativo.

Nota importante: usamos la identidad oficial vigente de Paraty Tech (guía de mayo de 2026), no los tokens antiguos que arrastra la app "Hotel SEO Studio". El azul de marca es #0088CC y la tipografía es Roboto.

## Stack de interfaz

- Next.js 16 (App Router) con TypeScript.
- Tailwind CSS v4 (los tokens se definen con @theme en el CSS global, no con tailwind.config.js).
- shadcn/ui como librería de componentes (Button, Card, Input, Label, Select, Textarea, Badge, AlertDialog, Tabs, etc.).
- Lucide React para iconografía.
- next-themes para el modo claro/oscuro (estrategia por clase).

## Colores

Paleta primaria de marca:

- Azul Paraty #0088CC. Color primario: botones principales, acentos, pestañas activas, badge de fase "Migración".
- Gris Paraty #A7A7A8. Texto secundario, separadores, badge de fase "Mantenimiento".
- Oscuro corporativo #202B37. Texto principal en modo claro y superficies oscuras. Se usa en lugar del negro puro.
- Texto tenue #57595A. Descripciones, labels, textos de ayuda.

Superficies en modo claro:

- Fondo general #F5F7FA.
- Cards en blanco #FFFFFF, con borde fino gris claro y sombra sutil.

Modo oscuro:

- Fondo gris muy oscuro casi negro (aprox #0F1216).
- Cards apenas más claras (aprox #171B21).
- Se mantiene el azul de marca #0088CC como primario.
- Texto tenue en gris #A7A7A8.

Accesibilidad (contraste AA):

- El azul de marca #0088CC cumple de sobra para botones e iconos, pero se queda corto para texto de enlace pequeño sobre fondo blanco.
- Solución: el texto de los enlaces en modo claro usa un azul un punto más oscuro, #0072AB (cumple AA). El resto del azul de marca se queda en #0088CC. En modo oscuro los enlaces pueden seguir en #0088CC, que ahí ya contrasta bien.

## Tipografía

- Roboto, cargada con next/font/google.
- Solo tres pesos: Thin 100, Regular 400, Medium 500. Prohibido Bold y Black.
- Cuerpo en 400. Títulos en 100 o 400. Subtítulos, etiquetas y botones en 500.
- Fallback: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif.

## Logotipo

- Se usan los logos oficiales de Paraty Tech (adjuntos aparte).
- Sobre fondo claro: versión de color.
- Sobre fondo oscuro: versión blanca.
- No deformar, recolorear ni rotar el logo.

## Cabecera

- Fija en la parte superior, presente en todas las páginas.
- A la izquierda, el logo de Paraty (cambia a la versión blanca en modo oscuro).
- Junto al logo, el título de la app en Roboto peso 500 (no bold) y, debajo, un subtítulo pequeño en gris.
- A la derecha, la navegación principal y el toggle de modo claro/oscuro (icono sol/luna de Lucide).

## Layout y contenedores

- Contenido centrado, con ancho máximo cómodo (unos 1000px para vistas generales, unos 640-800px para formularios y fichas).
- Padding generoso y mucho espacio en blanco.
- Cards con radios suaves (8-12px), borde fino gris claro y sombra sutil. Nada de sombras exageradas ni gradientes.

## Componentes y patrones

- Badges de estado por color: "Migración" en azul de marca, "Mantenimiento" en gris. Mismo criterio para otros estados (verde éxito, ámbar aviso).
- Formularios: labels encima del campo, textos de ayuda pequeños debajo, inputs de altura cómoda y radio suave. Campos condicionales que aparecen u ocultan según la selección (por ejemplo, un campo de detalle que solo se muestra al elegir "Sí").
- Selects de tres estados para preguntas de sí/no opcionales: "Sin responder", "Sí", "No".
- Pestañas (Tabs de shadcn) para organizar secciones dentro de una misma vista, por ejemplo la ficha de un hotel.
- Confirmaciones con AlertDialog de shadcn (nunca el confirm nativo del navegador).
- Botón primario: fondo azul de marca, texto blanco. Botón secundario: fondo transparente, borde gris. Iconos a la izquierda del texto cuando aporta.

## Tono e idioma

- Toda la interfaz en español.
- Textos claros y directos, sin tecnicismos innecesarios.
- Tono partner de Paraty: cercano pero profesional, frases cortas, sin buzzwords vacíos.

## Estilo general

Limpio, ordenado, mucho aire. Sensación de herramienta interna profesional, no de producto de consumo.
