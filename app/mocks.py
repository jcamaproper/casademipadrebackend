# Description: Este archivo contiene los datos de prueba para el proyecto
def respuestas_mocks(page =1, per_page=10):
    respuestas = []
    for i in range(1, 52):
        respuesta = {
            "Descripcion Audio": "Escucha la lectura del capítulo y el devocional correspondiente.",
            "Descripcion Video": "Mira nuestro video de Lee la Biblia sobre el libro de 2 Corintios, que desglosa el diseño literario del libro y su línea de pensamiento. En 2 Corintios, Pablo soluciona su conflicto con los corintios mostrándoles como el escándalo de la crucifixión pone al revés nuestros sistemas de valores.",
            "Devocional": "Dios ama al dador alegre\nEl asunto de las ofrendas en algunas iglesias es motivo de vergüenza para el evangelio...",
            # Nota: Aquí puedes variar el contenido del devocional para cada respuesta
            "Instrucciones": "Lee el capítulo del día y llena los cuadros correspondientes. Después lee la lectura devocional como un complemento para reflexionar en el mensaje que Dios tiene para ti. Si es posible, usa la versión Nueva Biblia de las Américas.",
            "Reflexion": "Reflexión\n¿Estás listo para recoger la cosecha abundante en tu vida?\n(1) Lc. 6:38 (2) Pr. 3:9-10 (3) Jn. 3:16",
            "Semana": f"Semana {i}",
            "SoundCloud Link": f"https://soundcloud.com/user-452278035/356-capitulos-mas-importantes-de-la-biblia-2-corintios-{i}?si=47d816d51e9648d59e90d50e5f792990&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing",
            "Titulo": f"Los 365 capítulos más importantes de la Biblia - 29 de octubre de 2023 – 2 Corintios {i}",
            "Titulo Audio": f"Los 365 capítulos más importantes de la Biblia – 2 Corintios {i}",
            "Titulo Video": "Proyecto Biblia: 2 Corintios",
            "Video Link": "https://www.youtube.com/watch?v=jV7dTkYFym4"
        }
        respuestas.append(respuesta)

    start = (page - 1) * per_page
    end = start + per_page
    
    return respuestas[start:end]