# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import random

ICONS = [
    'icon-wallet', 'icon-calendar', 'icon-bar-chart', 'icon-equalizer', 'icon-grid', 'icon-list',
    'icon-rocket', 'icon-shuffle', 'icon-support', 'icon-tag', 'icon-cloud-upload', 'icon-link',
    'icon-camera', 'icon-music-tone-alt', 'icon-globe', 'icon-directions', 'icon-cup', 'icon-basket',
    'icon-badge', 'icon-disc', 'icon-fire', 'icon-graduation', 'icon-ghost', 'icon-magic-wand',
    'icon-plane', 'icon-social-dropbox', 'icon-social-dribbble', 'icon-shield', 'icon-screen-desktop',
    'icon-social-twitter', 'icon-trophy', 'icon-speedometer', 'icon-social-youtube', ' icon-user',
    'icon-user-follow',
]


def get_random_icon():
    return ICONS[random.randrange(0, len(ICONS))]
