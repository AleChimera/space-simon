#!/usr/bin/python3
'''
Space Simon, programmed by Alejandro Chimera, winter 2024 (southern hemisphere).

A version of the classic memory game. Being more focused on the game's logic
than anything else, the aesthetics and (minimal) theme stem more from reusing
preexisting classes than deliberate design.

The functions to generate tones were provided by ChatGPT and worked after
some adjustments.

The code contains redundancies, particularly in color declarations.

Play using the arrow keys. Press Enter to start a new game.
Close with Ctrl+F4 or the window's "X" button.

Hope you enjoy it!


Space Simon, programado por Alejandro Chimera, invierno de 2024 (hemisferio sur).

Versión del clásico juego de memorización. Estando más concentrado en la lógica
del juego que en otra cosa, la estética y la (ínfima) temática responden más a
la reutilización de clases ya escritas que a otra cosa.

Las funciones para producir tonos fueron provistas por chatGPT, las cuales
funcionaron luego de algunos retoques.

Hay redundancias en el código, en particular con las declaraciones de colores.

Se juega con las flechas del cursor. Enter para iniciar un nuevo juego.
Se cierra con Ctrl+F4, o con la "X" de la ventana.

¡Espero lo disfruten!
'''

import pygame, sys, random
import numpy as np

class BGAnimation:
    '''Se declara antes del bucle principal. El constructor recibe como
    parámetro la ventana del juego. Luego en el bucle principal se pegan
    los métodos actualizar (game_logic) y dibujar (update_screen).'''
    NEGRO   = (  0,   0,   0)
    BLANCO  = (255, 255, 255)
    AZUL    = (  0,   0, 255)
    VERDE   = (  0, 255,   0)
    ROJO    = (255,   0,   0)
    VIOLETA = (255,   0, 255)

    colores = [AZUL, VERDE, ROJO, VIOLETA, BLANCO]

    def __init__(self, contenedor:pygame.Surface) -> None:
        self.contenedor = contenedor
        self.luces_grupo_1 = []
        self.luces_grupo_2 = []
        self.colores_grupo_1 = []
        self.colores_grupo_2 = []
        self.crear_grupo_de_luces(self.luces_grupo_1, self.colores_grupo_1)
        self.crear_grupo_de_luces(self.luces_grupo_2, self.colores_grupo_2)
        
    def crear_grupo_de_luces(self, grupo_luces:list, grupo_colores:list):
        for i in range(100):
            horizontal = random.randint(0, 800)
            vertical = random.randint(0, 600)
            punto = [horizontal, vertical]
            grupo_luces.append(punto)
        
        for i in range(100):
            grupo_colores.append(BGAnimation.colores[random.randint(0, 4)])

    def actualizar_animation_1(self):
        for i in range(100):
            self.luces_grupo_1[i][1] += 0.5
            if self.luces_grupo_1[i][1] > 550:
                self.luces_grupo_1[i][1] = -1
        for i in range(100):
            self.luces_grupo_2[i][1] += 0.75
            if self.luces_grupo_2[i][1] > 550:
                self.luces_grupo_2[i][1] = -1

    def dibujar_animation(self):
        for i in range(100):
            pygame.draw.rect(self.contenedor, self.colores_grupo_1[i], (self.luces_grupo_1[i][0], self.luces_grupo_1[i][1], 1, 1))
        for i in range(100):
            pygame.draw.rect(self.contenedor, self.colores_grupo_2[i], (self.luces_grupo_2[i][0], self.luces_grupo_2[i][1], 2, 2))

def generate_tone(frequency, duration, waveform='sine'):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    time = np.linspace(0, duration, num_samples, False)
    
    if waveform == 'sine':
        wave = np.sin(2 * np.pi * frequency * time)
    elif waveform == 'triangle':
        wave = 2 * np.abs(2 * (time * frequency - np.floor(time * frequency + 0.5))) - 1
    elif waveform == 'sawtooth':
        wave = 2 * (time * frequency - np.floor(time * frequency + 0.5))
    elif waveform == 'square':
        wave = np.sign(np.sin(2 * np.pi * frequency * time))
    elif waveform == 'noise':
        wave = np.random.uniform(-1, 1, num_samples)
    else:
        wave = np.sin(2 * np.pi * frequency * time)
    audio_data = np.array([wave, wave]).T  # Hacer que sea bidimensional
    audio_data *= 32767  # Escalar a valores de 16 bits
    audio_data = audio_data.astype(np.int16)  # Convertir a tipo de datos int16
    audio_data = np.ascontiguousarray(audio_data)  # Asegurar que el array sea contiguo
    
    return pygame.sndarray.make_sound(audio_data)

class Personaje(pygame.sprite.Sprite):
    
    BLACK   = (  0,   0,   0)
    WHITE   = (255, 255, 255)
    ROJO    = (255,   0,   0)
    VIOLETA = (255,   0, 255)
    VERDE   = (  0, 255,   0)
    AZUL    = (  0,   0, 255)
    COLOR_FONDO = BLACK

    invader_1A = [
        [2, 0, 1, 1], [8, 0, 1, 1],
        [3, 1, 1, 1], [7, 1, 1, 1],
        [2, 2, 7, 1],
        [1, 3, 2, 1], [4, 3, 3, 1], [8, 3, 2, 1],
        [0, 4, 11, 1],
        [0, 5, 1, 1], [2, 5, 7, 1], [10, 5, 1, 1],
        [0, 6, 1, 1], [2, 6, 1, 1], [8, 6, 1, 1], [10, 6, 1, 1],
        [3, 7, 2, 1], [6, 7, 2, 1]
    ]
    invader_1B = [
        [2, 0, 1, 1], [8, 0, 1, 1],
        [0, 1, 1, 1], [3, 1, 1, 1], [7, 1, 1, 1], [10, 1, 1, 1],
        [0, 2, 1, 1], [2, 2, 7, 1], [10, 2, 1, 1], 
        [0, 3, 3, 1], [4, 3, 3, 1], [8, 3, 3, 1],
        [0, 4, 11, 1],
        [1, 5, 9, 1],
        [2, 6, 1, 1], [8, 6, 1, 1],
        [1, 7, 1, 1], [9, 7, 1, 1]
    ]
    invader_1_dimensiones = (11, 8)

    def __init__(self, personaje:str, u:int, color=(255, 255, 255)):
        super().__init__()

        self.u = u
        if personaje == "invader_1":
            self.ancho = Personaje.invader_1_dimensiones[0] * self.u
            self.alto  = Personaje.invader_1_dimensiones[1] * self.u
        self.image_1 = pygame.Surface([self.ancho, self.alto])
        self.image_1.fill(Personaje.COLOR_FONDO)
        self.image_1.set_colorkey(Personaje.COLOR_FONDO)
        
        self.image_2_iluminado = pygame.Surface([self.ancho, self.alto])
        self.image_2_iluminado.fill(Personaje.COLOR_FONDO)
        self.image_2_iluminado.set_colorkey(Personaje.COLOR_FONDO)        
        
        self.rect = self.image_1.get_rect()
        
        self.color = color
        self.color_iluminado = self._definir_color_iluminado()
        
        if personaje == "invader_1":
            self._crear_dibujo(self.image_1, Personaje.invader_1A, self.color)
            self._crear_dibujo(self.image_2_iluminado, Personaje.invader_1B, self.color_iluminado)
        
        self.active = False     #Indica si el botón está pulsado o no. Es usado por dibujar().
        self.sonando = False

    def establecer_sonido(self, frecuenica, onda):
        self.sonido = generate_tone(frecuenica, 1, onda)

    def actualizar(self, pantalla_contenedora:pygame.Surface, duracion_sonido=-1):
        if not self.active:
            pantalla_contenedora.blit(self.image_1, [self.rect.x, self.rect.y])
            if self.sonando:
                self.sonido.stop()
                self.sonando = False
        else:
            pantalla_contenedora.blit(self.image_2_iluminado, [self.rect.x, self.rect.y])
            if not self.sonando:
                self.sonido.play(duracion_sonido)
                self.sonando = True
    
    def _crear_dibujo(self, superficie:pygame.Surface, matrizDibujo, color):
        for i in range (len(matrizDibujo)):
            pygame.draw.rect(superficie,
                             color,
                             ((self.rect.x + matrizDibujo[i][0]*self.u),
                              (self.rect.y + matrizDibujo[i][1]*self.u),
                              (matrizDibujo[i][2]*self.u),
                              (matrizDibujo[i][3]*self.u))
                              )
            
    def _definir_color_iluminado(self):
        intensidad = 167
        color_iluminado = []
        for i in range(3):
            if self.color[i] == 0:
                color_iluminado.append(intensidad)
            else:
                color_iluminado.append(self.color[i])
        return color_iluminado

class Botonera:
    def __init__(self, contenedor):
        self.container = contenedor
        self.teclas_pulsadas = 0
        self.dato_capturado = False
        #self.dato_ingresado    Declarada en leer_teclado()

        self.padding = 75
        #Los cuatro "botones" (Invaders para esta versión)
        self.abajo = Personaje("invader_1", 15, Personaje.ROJO)
        self.abajo.rect.x = self.container.get_width() / 2 - self.abajo.ancho / 2
        self.abajo.rect.y = self.container.get_height() /2 + self.padding
        self.abajo.establecer_sonido(196, 'sine')

        self.izquierda = Personaje("invader_1", 15, Personaje.AZUL)
        self.izquierda.rect.x = self.container.get_width() / 2 - self.izquierda.ancho - self.padding
        self.izquierda.rect.y = self.container.get_height() /2 - self.izquierda.alto / 2
        self.izquierda.establecer_sonido(262, 'sine')

        self.derecha = Personaje("invader_1", 15, Personaje.VIOLETA)
        self.derecha.rect.x = self.container.get_width() / 2 + self.padding
        self.derecha.rect.y = self.container.get_height() /2 - self.derecha.alto / 2
        self.derecha.establecer_sonido(330, 'sine')

        self.arriba = Personaje("invader_1", 15, Personaje.VERDE)
        self.arriba.rect.x = self.container.get_width() / 2 - self.arriba.ancho / 2
        self.arriba.rect.y = self.container.get_height() /2 - self.arriba.alto - self.padding
        self.arriba.establecer_sonido(392, 'sine')

        self.botones = [self.abajo, self.izquierda, self.derecha, self.arriba]
        self.teclas = [False, False, False, False]

    def leer_teclado(self):
        if self.teclas_pulsadas:
            for i in range(len(self.teclas)):
                if self.teclas[i]:
                    self.dato_ingresado = i
                    self.dato_capturado = True
                    break

    def actualizar(self):
        for i in range(len(self.botones)):
            self.botones[i].actualizar(self.container)

class Principal:
    WINDOW_ANCHO = 700
    WINDOW_ALTO  = 550
    FPS = 50
    #FUENTE_RETRO = '/usr/local/share/fonts/computo-monospace-font/ComputoMonospace-p73xO.ttf'
    FUENTE_RETRO = './computo-monospace-font/ComputoMonospace-p73xO.ttf'
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Space Simon")
        self.container = pygame.display.set_mode((Principal.WINDOW_ANCHO, Principal.WINDOW_ALTO))
        self.clock = pygame.time.Clock()
        self.done = False

        #Botonera
        self.botonera = Botonera(self.container)

        #Animación de fondo
        self.animation = BGAnimation(self.container)
        
        #Temporizador - Variables
        self.frames = 0
        self.frames_pausa = 0

        #Secuencia        
        self.index_nota = 0
        self.secuencia = []
        self.duracion_nota = 30     

        #Banderas
        self.actualizar_secuenica = True
        self.ejecutando_secuencia = True
        self.escuchando_jugador = True
        self.otro_juego = False
        self.pausa = False

        #Fuentes
        self.fuente_1 = pygame.font.Font(Principal.FUENTE_RETRO, 20)

    #Funciones Generales---
    def get_signals(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #QUIT = 256
                self.done = True

            if event.type == pygame.KEYDOWN:
                if not self.escuchando_jugador and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                    self.otro_juego = True
                if event.key == pygame.K_DOWN:
                    if self.botonera.teclas_pulsadas == 0:
                        self.botonera.teclas[0] = True
                    self.botonera.teclas_pulsadas += 1
                if event.key == pygame.K_LEFT:
                    if self.botonera.teclas_pulsadas == 0:
                        self.botonera.teclas[1] = True
                    self.botonera.teclas_pulsadas += 1
                if event.key == pygame.K_RIGHT:
                    if self.botonera.teclas_pulsadas == 0:
                        self.botonera.teclas[2] = True
                    self.botonera.teclas_pulsadas += 1
                if event.key == pygame.K_UP:
                    if self.botonera.teclas_pulsadas == 0:
                        self.botonera.teclas[3] = True
                    self.botonera.teclas_pulsadas += 1                
            
            if event.type == pygame.KEYUP:                
                if event.key == pygame.K_DOWN:
                    self.botonera.teclas[0] = False
                    self.botonera.teclas_pulsadas -= 1                
                if event.key == pygame.K_LEFT:
                    self.botonera.teclas[1] = False
                    self.botonera.teclas_pulsadas -= 1
                if event.key == pygame.K_RIGHT:
                    self.botonera.teclas[2] = False
                    self.botonera.teclas_pulsadas -= 1
                if event.key == pygame.K_UP:
                    self.botonera.teclas[3] = False
                    self.botonera.teclas_pulsadas -= 1

    def game_logic(self):
        #Animación
        self.animation.actualizar_animation_1()
        #Juego 
        if self.actualizar_secuenica:
            self.generar_secuencia()
        elif self.ejecutando_secuencia:   
            self.ejecutar_secuencia()            
        elif self.escuchando_jugador:
            if self.botonera.dato_capturado:
                if self.hay_error():
                    self.error()
                else:
                    self.ejecutar_ingresos_usuario()
            else:
                self.botonera.leer_teclado()
        elif self.otro_juego:
            self.reinicializaciones()
            
    def update_screen(self):
        self.container.fill(Principal.BLACK)
        #Animación
        self.animation.dibujar_animation()        
        self.botonera.actualizar()
        if not self.escuchando_jugador:
            self.container.blit(self.mensaje_aciertos, (450, 485))
        pygame.display.update()
        self.clock.tick(Principal.FPS)

    def main_loop(self):
        while not self.done:
            self.get_signals()
            self.game_logic()
            self.update_screen()
        
    def cerrar(self):
        pygame.quit()
        sys.exit(0)

    def run(self):
        self.main_loop()
        self.cerrar()

    #Funciones Particulares---
    def generar_secuencia(self):
        if self.pausa:
            self.frames_pausa += 1
            if self.frames_pausa > 15:     #15 frames de pausa
                self.frames_pausa = 0
                self.pausa = False
                self.actualizar_secuenica = False
        else:
            self.secuencia.append(random.randint(0, 3))
            self.pausa = True

    def ejecutar_secuencia(self):
        if self.index_nota < len(self.secuencia):
            self._ejecutar_nota(self.secuencia[self.index_nota], self.duracion_nota)
        else:
            self.ejecutando_secuencia = False
            self.index_nota = 0
            self.escuchando_jugador = True

    def _ejecutar_nota(self, nota, duracion):
        '''La ejecución de la nota consiste en una pausa de 5 frames, y luego la nota.'''
        if self.frames_pausa < 5:
            self.frames_pausa += 1
        else:
            self.frames += 1
            if self.frames < duracion:
                self.botonera.botones[nota].active = True
            else:
                self.botonera.botones[nota].active = False
                self.frames = 0
                self.frames_pausa = 0
                self.index_nota += 1

    def hay_error(self):
    #Error se refiere al error del jugador al pulsar una tecla que no coincide
    #con aquella correspondiente a la secuencia propuesta por el juego.
        error = False
        if self.botonera.dato_ingresado != self.secuencia[self.index_nota]:
            error = True
        return error

    def ejecutar_ingresos_usuario(self):
        if self.botonera.teclas[self.botonera.dato_ingresado]:
            self.botonera.botones[self.botonera.dato_ingresado].active = True
        else:
            self.botonera.botones[self.botonera.dato_ingresado].active = False
            self.botonera.dato_capturado = False
            self.index_nota += 1
            if self.index_nota >= len(self.secuencia):
                self.index_nota = 0
                self.actualizar_secuenica = True
                self.ejecutando_secuencia = True
                self.reducir_duracion_nota(1)
    
    def reducir_duracion_nota(self, variacion_duracion:int):
        self.duracion_nota -= variacion_duracion
        if self.duracion_nota < 4:
            self.duracion_nota = 4

    def error(self):
        self.frames_pausa += 1
        if self.frames_pausa > 25:
            self.botonera.botones[self.botonera.dato_ingresado].active = False
            self.botonera.botones[self.secuencia[self.index_nota]].active = False
            self.escuchando_jugador = False
            self.frames_pausa = 0
            self.index_nota = 0
            self.mensaje_aciertos = self.fuente_1.render(f"Aciertos: {len(self.secuencia) - 1}", True, Principal.WHITE)
        else:
            self.botonera.botones[self.botonera.dato_ingresado].active = True
            self.botonera.botones[self.secuencia[self.index_nota]].active = True

    def reinicializaciones(self):
        self.secuencia = []
        self.duracion_nota = 30
        self.actualizar_secuenica = True
        self.ejecutando_secuencia = True
        self.escuchando_jugador = True
        self.otro_juego = False
        self.botonera.dato_capturado = False

Principal().run()
