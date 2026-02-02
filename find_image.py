import cv2
import numpy as np
import pygame

def surface_to_cv(surface):
    return pygame.surfarray.array3d(surface).swapaxes(0, 1)

def find_image(template, source, threshold=0.95):
    tpl = surface_to_cv(template)
    src = surface_to_cv(source)

    result = cv2.matchTemplate(src, tpl, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    rects = []
    w, h = template.get_size()

    for pt in zip(*locations[::-1]):
        rects.append(pygame.Rect(pt[0], pt[1], w, h))

    return rects