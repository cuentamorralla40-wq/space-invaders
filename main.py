import pygame
import sys
import random

# Inicializar Pygame y el mezclador de sonido
pygame.init()
pygame.mixer.init()

# Configuración de pantalla y colores
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders - Local AI")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (220, 20, 60)
AZUL = (0, 100, 255)
GRIS = (120, 120, 120)
VIOLETA = (148, 0, 211)
CYAN = (0, 206, 209)
NARANJA = (255, 140, 0)
VERDE = (0, 200, 0)
AMARILLO = (255, 215, 0)
DORADO = (255, 215, 0)

# Reloj y FPS
RELOJ = pygame.time.Clock()
FPS = 60

# Fuentes
FUENTE = pygame.font.SysFont("Arial", 24)
FUENTE_GRANDE = pygame.font.SysFont("Arial", 48)

# Generadores de efectos de sonido sintéticos
def sonido_disparo():
    try:
        duracion = 120
        sample_rate = 22050
        num_samples = int(sample_rate * (duracion / 1000.0))
        buffer = bytearray()
        for i in range(num_samples):
            freq = 900 - (i * 4)
            valor = int(32767 * 0.4 * (((i * freq // sample_rate) % 2) * 2 - 1) * (1.0 - i/num_samples))
            buffer += valor.to_bytes(2, byteorder='little', signed=True)
        sonido = pygame.mixer.Sound(buffer=buffer)
        sonido.set_volume(0.25)
        sonido.play()
    except:
        pass

def sonido_explosion():
    try:
        duracion = 250
        sample_rate = 22050
        num_samples = int(sample_rate * (duracion / 1000.0))
        buffer = bytearray()
        for i in range(num_samples):
            valor = int(32767 * 0.3 * (random.random() - 0.5) * (1.0 - i/num_samples))
            buffer += valor.to_bytes(2, byteorder='little', signed=True)
        sonido = pygame.mixer.Sound(buffer=buffer)
        sonido.set_volume(0.35)
        sonido.play()
    except:
        pass

def sonido_gran_explosion():
    try:
        duracion = 400
        sample_rate = 22050
        num_samples = int(sample_rate * (duracion / 1000.0))
        buffer = bytearray()
        for i in range(num_samples):
            freq_baja = 80 + int(20 * random.random())
            valor = int(32767 * 0.5 * (((i * freq_baja // sample_rate) % 2) * 2 - 1) * (1.0 - i/num_samples))
            buffer += valor.to_bytes(2, byteorder='little', signed=True)
        sonido = pygame.mixer.Sound(buffer=buffer)
        sonido.set_volume(0.5)
        sonido.play()
    except:
        pass

def sonido_musica_fondo():
    try:
        duracion = 150
        sample_rate = 22050
        num_samples = int(sample_rate * (duracion / 1000.0))
        buffer = bytearray()
        for i in range(num_samples):
            freq = 110
            valor = int(32767 * 0.15 * (((i * freq // sample_rate) % 2) * 2 - 1))
            buffer += valor.to_bytes(2, byteorder='little', signed=True)
        sonido = pygame.mixer.Sound(buffer=buffer)
        sonido.set_volume(0.1)
        sonido.play()
    except:
        pass

class Jugador:
    def __init__(self):
        self.ancho = 50
        self.alto = 25
        self.x = ANCHO // 2 - self.ancho // 2
        self.y = ALTO - 60
        self.velocidad = 5  
        self.vidas = 5      
        self.puntuacion = 0
        self.escudo_activo = False
        self.tiempo_escudo = 0

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, AZUL, (self.x + 18, self.y - 8, 14, 10)) # Cañón
        pygame.draw.rect(superficie, AZUL, (self.x, self.y + 6, self.ancho, 14)) # Base
        pygame.draw.rect(superficie, AZUL, (self.x + 10, self.y, 30, 8)) # Cuerpo
        
        if self.escudo_activo:
            pygame.draw.circle(superficie, VERDE, (self.x + self.ancho // 2, self.y + self.alto // 2), 35, 2)

    def mover_izquierda(self):
        if self.x > 0:
            self.x -= self.velocidad

    def mover_derecha(self):
        if self.x < ANCHO - self.ancho:
            self.x += self.velocidad

class Disparo:
    def __init__(self, x, y, es_enemigo=False):
        self.x = x
        self.y = y
        self.ancho = 6   
        self.alto = 18  
        self.es_enemigo = es_enemigo
        self.velocidad = 4.5 if es_enemigo else 9.0

    def actualizar(self):
        if self.es_enemigo:
            self.y += self.velocidad
        else:
            self.y -= self.velocidad

    def dibujar(self, superficie):
        color = ROJO if self.es_enemigo else NEGRO
        pygame.draw.rect(superficie, color, (int(self.x), int(self.y), self.ancho, self.alto))

class Explosion:
    def __init__(self, x, y, grande=False):
        self.x = x
        self.y = y
        self.grande = grande
        self.duracion = 25  
    
    def dibujar(self, superficie):
        radio = 30 if self.grande else 20
        color = AMARILLO if self.grande else ROJO
        pygame.draw.circle(superficie, color, (int(self.x), int(self.y)), radio)
        pygame.draw.circle(superficie, BLANCO, (int(self.x), int(self.y)), radio // 2)
        self.duracion -= 1

class Enemigo:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.ancho = 40
        self.alto = 28
        self.tipo = tipo  

        if tipo == 1: self.color = VIOLETA
        elif tipo == 2: self.color = CYAN
        elif tipo == 3: self.color = NARANJA
        else: self.color = GRIS

    def dibujar(self, superficie):
        c = self.color
        x, y = self.x, self.y
        
        if self.tipo == 1:
            pygame.draw.rect(superficie, c, (x + 12, y, 16, 8))
            pygame.draw.rect(superficie, c, (x + 8, y + 8, 24, 8))
            pygame.draw.rect(superficie, BLANCO, (x + 12, y + 4, 4, 4))
            pygame.draw.rect(superficie, BLANCO, (x + 24, y + 4, 4, 4))
            pygame.draw.rect(superficie, c, (x + 4, y + 16, 32, 8))
            pygame.draw.rect(superficie, c, (x + 8, y + 24, 6, 6))
            pygame.draw.rect(superficie, c, (x + 26, y + 24, 6, 6))
        elif self.tipo == 2:
            pygame.draw.rect(superficie, c, (x + 8, y + 4, 24, 16))
            pygame.draw.rect(superficie, c, (x + 4, y + 8, 32, 8))
            pygame.draw.rect(superficie, BLANCO, (x + 10, y + 8, 4, 4))
            pygame.draw.rect(superficie, BLANCO, (x + 26, y + 8, 4, 4))
            pygame.draw.rect(superficie, c, (x, y + 16, 8, 8))
            pygame.draw.rect(superficie, c, (x + 32, y + 16, 8, 8))
            pygame.draw.rect(superficie, c, (x + 12, y + 20, 16, 6))
        elif self.tipo == 3:
            pygame.draw.rect(superficie, c, (x + 12, y, 16, 6))
            pygame.draw.rect(superficie, c, (x + 4, y + 6, 32, 12))
            pygame.draw.rect(superficie, BLANCO, (x + 10, y + 8, 4, 4))
            pygame.draw.rect(superficie, BLANCO, (x + 26, y + 8, 4, 4))
            pygame.draw.rect(superficie, c, (x + 8, y + 18, 24, 6))
            pygame.draw.rect(superficie, c, (x + 4, y + 24, 4, 4))
            pygame.draw.rect(superficie, c, (x + 12, y + 24, 4, 4))
            pygame.draw.rect(superficie, c, (x + 24, y + 24, 4, 4))
            pygame.draw.rect(superficie, c, (x + 32, y + 24, 4, 4))
        else:
            pygame.draw.rect(superficie, c, (x + 14, y + 2, 12, 6))
            pygame.draw.rect(superficie, c, (x + 4, y + 8, 32, 10))
            pygame.draw.rect(superficie, BLANCO, (x + 12, y + 10, 4, 4))
            pygame.draw.rect(superficie, BLANCO, (x + 24, y + 10, 4, 4))
            pygame.draw.rect(superficie, c, (x + 8, y + 18, 24, 4))
            pygame.draw.rect(superficie, c, (x + 2, y + 13, 4, 6))
            pygame.draw.rect(superficie, c, (x + 34, y + 13, 4, 6))

def crear_enemigos():
    lista_enemigos = []
    filas = 4       
    columnas = 7    
    espacio_x = 90
    espacio_y = 45
    inicio_x = 80
    inicio_y = 80

    for fila in range(filas):
        for col in range(columnas):
            x = inicio_x + (col * espacio_x)
            y = inicio_y + (fila * espacio_y)
            lista_enemigos.append(Enemigo(x, y, tipo=fila + 1))
            
    return lista_enemigos

def pantalla_transicion_nivel(nivel):
    esperando = True
    inicio_tiempo = pygame.time.get_ticks()
    while esperando:
        VENTANA.fill(BLANCO)
        texto_nivel = FUENTE_GRANDE.render(f"NIVEL {nivel}", True, AZUL)
        texto_aviso = FUENTE.render("¡Prepárate para la siguiente horda!", True, GRIS)
        
        VENTANA.blit(texto_nivel, (ANCHO // 2 - texto_nivel.get_width() // 2, ALTO // 3))
        VENTANA.blit(texto_aviso, (ANCHO // 2 - texto_aviso.get_width() // 2, ALTO // 2))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Pantalla visible durante 3 segundos exactos
        if pygame.time.get_ticks() - inicio_tiempo > 3000:
            esperando = False

def pantalla_transicion_nave(vidas_restantes):
    esperando = True
    inicio_tiempo = pygame.time.get_ticks()
    while esperando:
        VENTANA.fill(BLANCO)
        texto_nave = FUENTE_GRANDE.render(f"NAVE ACTUAL: {vidas_restantes}", True, AZUL)
        texto_aviso = FUENTE.render("Preparándose para continuar...", True, GRIS)
        
        VENTANA.blit(texto_nave, (ANCHO // 2 - texto_nave.get_width() // 2, ALTO // 3))
        VENTANA.blit(texto_aviso, (ANCHO // 2 - texto_aviso.get_width() // 2, ALTO // 2))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.time.get_ticks() - inicio_tiempo > 2000:
            esperando = False

def pantalla_victoria():
    inicio_tiempo = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inicio_tiempo < 5000:  # Dura 5 segundos
        VENTANA.fill(BLANCO)
        
        # Dibujar fuegos artificiales aleatorios de fondo
        for _ in range(8):
            fx = random.randint(100, ANCHO - 100)
            fy = random.randint(50, ALTO - 200)
            fcol = random.choice([ROJO, AZUL, VERDE, NARANJA, VIOLETA])
            pygame.draw.circle(VENTANA, fcol, (fx, fy), random.randint(15, 35), 2)

        # Dibujar una Copa de Oro geométrica en el centro
        cx, cy = ANCHO // 2, ALTO // 2 - 20
        pygame.draw.rect(VENTANA, DORADO, (cx - 30, cy - 40, 60, 50))  # Cuerpo copa
        pygame.draw.polygon(VENTANA, DORADO, [(cx - 30, cy - 40), (cx + 30, cy - 40), (cx, cy - 10)])
        pygame.draw.rect(VENTANA, DORADO, (cx - 8, cy + 10, 16, 30))   # Base soporte
        pygame.draw.rect(VENTANA, DORADO, (cx - 25, cy + 40, 50, 10))   # Base inferior
        # Asas de la copa
        pygame.draw.arc(VENTANA, DORADO, pygame.Rect(cx - 50, cy - 35, 25, 30), 0, 3.14, 3)
        pygame.draw.arc(VENTANA, DORADO, pygame.Rect(cx + 25, cy - 35, 25, 30), 0, 3.14, 3)

        # Texto de Campeón
        texto_campeon = FUENTE_GRANDE.render("¡CAMPEÓN!", True, NEGRO)
        texto_sub = FUENTE.render("¡Has superado los 5 niveles con éxito!", True, GRIS)
        
        VENTANA.blit(texto_campeon, (ANCHO // 2 - texto_campeon.get_width() // 2, ALTO // 4 - 30))
        VENTANA.blit(texto_sub, (ANCHO // 2 - texto_sub.get_width() // 2, ALTO // 4 + 30))

        pygame.display.flip()
        RELOJ.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def menu_principal():
    en_menu = True
    while en_menu:
        VENTANA.fill(BLANCO)
        titulo = FUENTE_GRANDE.render("SPACE INVADERS", True, NEGRO)
        instrucciones = FUENTE.render("Pulsa ENTER para comenzar el juego", True, GRIS)
        controles_txt1 = FUENTE.render("Controles: [Z] Izq | [X] Der | [M] Disp | [N] Escudo", True, NEGRO)
        
        VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 3))
        VENTANA.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, ALTO // 2))
        VENTANA.blit(controles_txt1, (ANCHO // 2 - controles_txt1.get_width() // 2, ALTO // 2 + 60))
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    en_menu = False

def juego_principal():
    jugador = Jugador()
    balas = []
    explosiones = []
    enemigos = crear_enemigos()
    
    nivel_actual = 1
    
    tiempo_ultimo_movimiento = pygame.time.get_ticks()
    
    fase_movimiento = 0  
    pasos_realizados = 0
    PASOS_POR_FASE = 4   

    ultimo_disparo = 0
    CADENCIA_DISPARO = 250 

    tiempo_ultima_musica = pygame.time.get_ticks()
    INTERVALO_MUSICA = 800

    tiempo_ultimo_disparo_enemigo = pygame.time.get_ticks()
    INTERVALO_DISPARO_ENEMIGO = 1000

    ejecutando = True
    while ejecutando:
        tiempo_actual = pygame.time.get_ticks()
        RELOJ.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_n:
                    jugador.escudo_activo = True
                    jugador.tiempo_escudo = tiempo_actual + 3000  

        if jugador.escudo_activo and tiempo_actual > jugador.tiempo_escudo:
            jugador.escudo_activo = False

        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_z]:
            jugador.mover_izquierda()
        if teclas[pygame.K_x]:
            jugador.mover_derecha()

        if teclas[pygame.K_m]:
            if tiempo_actual - ultimo_disparo > CADENCIA_DISPARO:
                balas.append(Disparo(jugador.x + jugador.ancho // 2 - 3, jugador.y, es_enemigo=False))
                sonido_disparo()
                ultimo_disparo = tiempo_actual

        if tiempo_actual - tiempo_ultima_musica > INTERVALO_MUSICA:
            sonido_musica_fondo()
            tiempo_ultima_musica = tiempo_actual

        # Velocidad de los enemigos aumenta un 0.1 por cada nivel (intervalo de movimiento disminuye)
        intervalo_movimiento = max(200, int(1000 - (nivel_actual - 1) * 150))

        if tiempo_actual - tiempo_ultimo_movimiento > intervalo_movimiento:
            tiempo_ultimo_movimiento = tiempo_actual
            
            dir_x = -1 if fase_movimiento == 0 else 1
            for enemigo in enemigos:
                enemigo.x += 18 * dir_x

            pasos_realizados += 1
            if pasos_realizados >= PASOS_POR_FASE:
                pasos_realizados = 0
                fase_movimiento += 1
                if fase_movimiento > 1:
                    for enemigo in enemigos:
                        enemigo.y += 20
                    fase_movimiento = 0

        if tiempo_actual - tiempo_ultimo_disparo_enemigo > INTERVALO_DISPARO_ENEMIGO:
            tiempo_ultimo_disparo_enemigo = tiempo_actual
            if enemigos:
                enemigo_tirador = random.choice(enemigos)
                balas.append(Disparo(enemigo_tirador.x + enemigo_tirador.ancho // 2, enemigo_tirador.y + enemigo_tirador.alto, es_enemigo=True))

        # Actualizar balas
        for bala in balas[:]:
            bala.actualizar()
            if bala.y < 0 or bala.y > ALTO:
                balas.remove(bala)
                continue

            bala_rect = pygame.Rect(bala.x, bala.y, bala.ancho, bala.alto)

            if bala.es_enemigo:
                jugador_rect = pygame.Rect(jugador.x, jugador.y, jugador.ancho, jugador.alto)
                if bala_rect.colliderect(jugador_rect):
                    balas.remove(bala)
                    if jugador.escudo_activo:
                        sonido_explosion()
                        explosiones.append(Explosion(jugador.x + jugador.ancho // 2, jugador.y + jugador.alto // 2, grande=False))
                    else:
                        sonido_gran_explosion()
                        explosiones.append(Explosion(jugador.x + jugador.ancho // 2, jugador.y + jugador.alto // 2, grande=True))
                        jugador.vidas -= 1
                        if jugador.vidas <= 0:
                            ejecutando = False
                        else:
                            pantalla_transicion_nave(jugador.vidas)
            else:
                for enemigo in enemigos[:]:
                    enemigo_rect = pygame.Rect(enemigo.x, enemigo.y, enemigo.ancho, enemigo.alto)
                    if bala_rect.colliderect(enemigo_rect):
                        explosiones.append(Explosion(enemigo.x + enemigo.ancho // 2, enemigo.y + enemigo.alto // 2, grande=False))
                        enemigos.remove(enemigo)
                        balas.remove(bala)
                        sonido_explosion()
                        jugador.puntuacion += 100
                        break

        for enemigo in enemigos:
            if enemigo.y >= jugador.y - 15:
                sonido_gran_explosion()
                jugador.vidas -= 1
                if jugador.vidas <= 0:
                    ejecutando = False
                else:
                    pantalla_transicion_nave(jugador.vidas)
                enemigos = crear_enemigos()

        # Si se eliminan todos los enemigos, se avanza de nivel o se gana la partida
        if len(enemigos) == 0:
            nivel_actual += 1
            if nivel_actual > 5:
                pantalla_victoria()
                ejecutando = False
            else:
                pantalla_transicion_nivel(nivel_actual)
                enemigos = crear_enemigos()

        # Dibujar elementos
        VENTANA.fill(BLANCO)

        jugador.dibujar(VENTANA)
        for bala in balas:
            bala.dibujar(VENTANA)
        for enemigo in enemigos:
            enemigo.dibujar(VENTANA)

        for exp in explosiones[:]:
            exp.dibujar(VENTANA)
            if exp.duracion <= 0:
                explosiones.remove(exp)

        texto_score = FUENTE.render(f"Puntuación: {jugador.puntuacion}", True, NEGRO)
        texto_vidas = FUENTE.render(f"Naves Extra (Vidas): {jugador.vidas}", True, NEGRO)
        texto_nivel = FUENTE.render(f"Nivel: {nivel_actual}/5", True, NEGRO)
        estado_escudo = FUENTE.render(f"Escudo [N]: {'ACTIVO' if jugador.escudo_activo else 'LISTO'}", True, VERDE if jugador.escudo_activo else GRIS)
        
        VENTANA.blit(texto_score, (20, 20))
        VENTANA.blit(texto_vidas, (20, 50))
        VENTANA.blit(texto_nivel, (20, 80))
        VENTANA.blit(estado_escudo, (20, 110))

        pygame.display.flip()

    # Pantalla Game Over
    if jugador.vidas <= 0:
        while True:
            VENTANA.fill(BLANCO)
            texto_gameover = FUENTE_GRANDE.render("FIN DEL JUEGO", True, ROJO)
            texto_puntos = FUENTE.render(f"Puntuación final: {jugador.puntuacion}", True, NEGRO)
            VENTANA.blit(texto_gameover, (ANCHO // 2 - texto_gameover.get_width() // 2, ALTO // 3))
            VENTANA.blit(texto_puntos, (ANCHO // 2 - texto_puntos.get_width() // 2, ALTO // 2))
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    while True:
        menu_principal()
        juego_principal()
