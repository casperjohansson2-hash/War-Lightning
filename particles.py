from typing import Union, Sequence, Tuple
import pygame
import random

# Particle field indices (13 total)
X, Y, VX, VY, AX, AY, DX, DY, DS, R, F, A, CIDX = range(13)

class Particles(pygame.Surface):
    def __init__(
        self,  
        size: Tuple[int, int], 
        fade: Union[Tuple[float, float], float] = 0.98, 
        vel_x: Union[Tuple[float, float], float] = (-10, 10), 
        vel_y: Union[Tuple[float, float], float] = (-10, 10), 
        acc_x: Union[Tuple[float, float], float] = (0, 0), 
        acc_y: Union[Tuple[float, float], float] = (0, 0), 
        decay_x: Union[Tuple[float, float], float] = 0.95, 
        decay_y: Union[Tuple[float, float], float] = 0.95, 
        decay_size: Union[Tuple[float, float], float] = 0.96,
        radius: Union[Tuple[int, int], int] = (2, 6),
        colors: Sequence[Tuple[int, int, int]] = [(255, 50, 50), (255, 150, 50), (255, 255, 50)]
    ) -> None: 
        super().__init__(size, flags=pygame.SRCALPHA)
        self.particles = []
        self.size = size
        self.fade = fade
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.decay_x = decay_x
        self.decay_y = decay_y
        self.decay_size = decay_size
        self.radius = radius
        self.colors = colors
        
        # Pre-compute ranges for fast emission
        self._vx_is_range = isinstance(vel_x, (tuple, list, Sequence)) and len(vel_x) == 2
        self._vy_is_range = isinstance(vel_y, (tuple, list, Sequence)) and len(vel_y) == 2
        self._ax_is_range = isinstance(acc_x, (tuple, list, Sequence)) and len(acc_x) == 2
        self._ay_is_range = isinstance(acc_y, (tuple, list, Sequence)) and len(acc_y) == 2
        self._dx_is_range = isinstance(decay_x, (tuple, list, Sequence)) and len(decay_x) == 2
        self._dy_is_range = isinstance(decay_y, (tuple, list, Sequence)) and len(decay_y) == 2
        self._ds_is_range = isinstance(decay_size, (tuple, list, Sequence)) and len(decay_size) == 2
        self._r_is_range = isinstance(radius, (tuple, list, Sequence)) and len(radius) == 2
        self._f_is_range = isinstance(fade, (tuple, list, Sequence)) and len(fade) == 2
        self._num_colors = len(colors)
    
    def emit(self, x: float, y: float, count: int = 1) -> None:
        """Emit count particles at position (x, y)"""
        particles = self.particles
        append = particles.append
        uniform = random.uniform
        randint = random.randint
        
        # Cache lookups
        vx, vy = self.vel_x, self.vel_y
        ax, ay = self.acc_x, self.acc_y
        dx, dy = self.decay_x, self.decay_y
        ds, r, f = self.decay_size, self.radius, self.fade
        
        for _ in range(count):
            p = [0.0] * 13
            p[X], p[Y] = x, y
            p[VX] = uniform(*vx) if self._vx_is_range else vx
            p[VY] = uniform(*vy) if self._vy_is_range else vy
            p[AX] = uniform(*ax) if self._ax_is_range else ax
            p[AY] = uniform(*ay) if self._ay_is_range else ay
            p[DX] = uniform(*dx) if self._dx_is_range else dx
            p[DY] = uniform(*dy) if self._dy_is_range else dy
            p[DS] = uniform(*ds) if self._ds_is_range else ds
            p[R] = uniform(*r) if self._r_is_range else r
            p[F] = uniform(*f) if self._f_is_range else f
            p[A] = 255.0
            p[CIDX] = randint(0, self._num_colors - 1)
            append(p)
    
    def update(self, dt: float = 1.0) -> None:
        """Update all particles. dt scales physics (default: 1.0)"""
        alive = []
        append = alive.append
        
        for p in self.particles:
            # Update position
            p[X] += p[VX] * dt
            p[Y] += p[VY] * dt
            
            # Update velocity with acceleration and decay
            p[VX] = (p[VX] + p[AX] * dt) * p[DX]
            p[VY] = (p[VY] + p[AY] * dt) * p[DY]
            
            # Update size and alpha
            p[R] *= p[DS]
            p[A] *= p[F]
            
            # Keep if alive
            if p[R] > 1.0 and p[A] > 20.0:
                append(p)
        
        self.particles = alive
    
    def render(self, surface: pygame.Surface, offset: Tuple[int, int] = (0, 0)) -> None:
        """Render particles to surface at offset position"""
        self.fill((0, 0, 0, 0))

        draw = pygame.draw.circle
        colors = self.colors
        
        for p in self.particles:
            col = colors[int(p[CIDX])]
            alpha = int(p[A])
            
            # Handle RGBA colors
            if len(col) >= 4:
                alpha = min(alpha + col[3], 255)
                col = col[:3]
            
            alpha = max(0, min(alpha, 255))
            
            draw(
                self,
                (*col, alpha),
                (int(p[X]), int(p[Y])),
                max(1, int(p[R]))
            )
        
        surface.blit(self, offset)
    
    def clear(self) -> None:
        """Remove all particles"""
        self.particles.clear()
    
    def count(self) -> int:
        """Return number of active particles"""
        return len(self.particles)