from neo4j import GraphDatabase
import time

# Configuración
URI = "bolt://neo4j:7687"
AUTH = ("neo4j", "password")

def cargar_datos_prueba():
    print("1. Iniciando proceso de carga de datos...")
    driver = GraphDatabase.driver(URI, auth=AUTH)
    
    with driver.session() as session:
        # 1. Limpieza (Para asegurar que no duplicamos en pruebas repetidas)
        print("2. Limpiando base de datos anterior...")
        session.run("MATCH (n) DETACH DELETE n")
        
        # 2. Definición del Escenario (Copiado de tu informe)
        print("3. Creando Nodos (Usuarios, Habilidades, Ejercicios)...")
        query_nodos = """
        // Usuarios
        MERGE (u1:Usuario {user_id: 'ana_01', nombre: 'Ana', nivel: 'Intermedio'})
        MERGE (u2:Usuario {user_id: 'luis_02', nombre: 'Luis', nivel: 'Intermedio'})
        
        // Habilidades
        MERGE (h1:Habilidad {habilidad_id: 'sub_01', descripcion: 'Subjuntivo'})
        MERGE (h2:Habilidad {habilidad_id: 'pas_02', descripcion: 'Pasado Simple'})
        
        // Ejercicios
        MERGE (e1:Ejercicio {ejercicio_id: 'ej_101', tipo: 'completar_frase', dificultad: 3})
        MERGE (e2:Ejercicio {ejercicio_id: 'ej_102', tipo: 'traduccion', dificultad: 4})
        MERGE (e3:Ejercicio {ejercicio_id: 'ej_201', tipo: 'listening', dificultad: 2})
        """
        session.run(query_nodos)
        
        # 3. Creación de Relaciones (Historia)
        print("4. Conectando Relaciones y simulando historial...")
        query_relaciones = """
        MATCH (u1:Usuario {user_id: 'ana_01'})
        MATCH (u2:Usuario {user_id: 'luis_02'})
        MATCH (h1:Habilidad {habilidad_id: 'sub_01'})
        MATCH (h2:Habilidad {habilidad_id: 'pas_02'})
        MATCH (e1:Ejercicio {ejercicio_id: 'ej_101'})
        MATCH (e2:Ejercicio {ejercicio_id: 'ej_102'})
        MATCH (e3:Ejercicio {ejercicio_id: 'ej_201'})
        
        // Estructura Pedagógica (Estática)
        MERGE (e1)-[:PRUEBA]->(h1)
        MERGE (e2)-[:PRUEBA]->(h1)
        MERGE (e3)-[:PRUEBA]->(h2)
        
        // Historial de Usuario (Dinámico)
        // Ana tiene problemas con el Subjuntivo
        MERGE (u1)-[:TIENE_DIFICULTAD_CON {tasa_error: 0.75, detectado_en: datetime()}]->(h1)
        
        // Luis también tiene problemas con el Subjuntivo
        MERGE (u2)-[:TIENE_DIFICULTAD_CON {tasa_error: 0.80, detectado_en: datetime()}]->(h1)
        
        // Luis intentó el Ejercicio 101 y primero falló, luego tuvo éxito
        MERGE (u2)-[:INTENTO {resultado: 'fallo', timestamp: datetime('2025-11-01T10:00:00')}]->(e1)
        MERGE (u2)-[:INTENTO {resultado: 'exito', timestamp: datetime('2025-11-01T10:05:00')}]->(e1)
        
        // Luis intentó el Ejercicio 102 y falló
        MERGE (u2)-[:INTENTO {resultado: 'fallo', timestamp: datetime('2025-11-02T11:00:00')}]->(e2)
        
        // Similitud (Calculada por ML Batch Job)
        MERGE (u1)-[:SIMILAR_A {score: 0.88, algoritmo: 'cosine_similarity'}]->(u2)
        MERGE (u2)-[:SIMILAR_A {score: 0.88, algoritmo: 'cosine_similarity'}]->(u1)
        """
        session.run(query_relaciones)
        
    driver.close()
    print("5. ¡Base de datos precargada exitosamente!")
    print("6. Datos listos: Ana, Luis, Habilidades y sus historiales.")

if __name__ == "__main__":
    cargar_datos_prueba()