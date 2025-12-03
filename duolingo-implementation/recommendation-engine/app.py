from neo4j import GraphDatabase
import pandas as pd
import sys

# Configuración
URI = "bolt://neo4j:7687"
AUTH = ("neo4j", "password")

class MotorRecomendaciones:
    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def cerrar(self):
        self.driver.close()

    def recomendar_ejercicios(self, user_id):
        """
        Implementa el algoritmo de Filtrado Colaborativo definido en el obligatorio.
        Lógica:
        1. Identificar debilidades del usuario actual.
        2. Buscar usuarios similares ('vecinos').
        3. Ver qué ejercicios exitosos hicieron esos vecinos para esa debilidad.
        4. Filtrar ejercicios que el usuario actual ya haya hecho.
        """
        print(f"Analizando perfil de '{user_id}' en tiempo real...")
        
        query = """
        MATCH (usuario:Usuario {user_id: $uid})
        
        // Paso 1: ¿Qué le cuesta a este usuario?
        MATCH (usuario)-[:TIENE_DIFICULTAD_CON]->(habilidad:Habilidad)
        
        // Paso 2: ¿Quién más es como él?
        MATCH (vecino:Usuario)-[s:SIMILAR_A]-(usuario)
        WHERE (vecino)-[:TIENE_DIFICULTAD_CON]->(habilidad)
        
        // Paso 3: ¿Qué hizo el vecino que funcionó?
        MATCH (ejercicio:Ejercicio)-[:PRUEBA]->(habilidad)
        WHERE EXISTS {
            MATCH (vecino)-[:INTENTO {resultado: 'exito'}]->(ejercicio)
        }
        
        // Paso 4: Asegurar que NO sea algo que el usuario ya hizo
        AND NOT EXISTS {
            MATCH (usuario)-[:INTENTO]->(ejercicio)
        }
        
        RETURN DISTINCT
            habilidad.descripcion AS Habilidad_A_Reforzar,
            ejercicio.ejercicio_id AS Ejercicio_Recomendado,
            ejercicio.tipo AS Tipo,
            vecino.nombre AS Basado_En_Usuario,
            s.score AS Score_Similitud
        ORDER BY s.score DESC
        """
        
        with self.driver.session() as session:
            result = session.run(query, uid=user_id)
            data = [record.data() for record in result]
            return data

# --- Interfaz de Línea de Comandos ---
if __name__ == "__main__":
    motor = MotorRecomendaciones()
    
    # Usuario por defecto para la demo
    target_user = "ana_01" 
    
    if len(sys.argv) > 1:
        target_user = sys.argv[1]

    try:
        recomendaciones = motor.recomendar_ejercicios(target_user)
        
        print("\n" + "="*50)
        print(f"REPORTE DE RECOMENDACIONES: {target_user.upper()}")
        print("="*50)
        
        if recomendaciones:
            df = pd.DataFrame(recomendaciones)
            # Formato bonito para consola
            print(df.to_string(index=False, justify='left'))
            print("\nRecomendación generada exitosamente.")
        else:
            print("No hay recomendaciones disponibles para este usuario.")
            print("(Puede que no tenga dificultades registradas o no tenga vecinos similares).")
            
    except Exception as e:
        print(f"Error de conexión: {e}")
        print("Asegúrate de haber ejecutado 'docker-compose up' y 'python loader.py' primero.")
    finally:
        motor.cerrar()