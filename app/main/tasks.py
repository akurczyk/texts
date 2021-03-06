import colorsys
import random

import imgkit
from celery import shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from .models import Text


@shared_task
def process_text(text_id):
    text = Text.objects.get(pk=text_id)

    patterns = [
        'axiom-pattern',
        'asfalt-dark',
        'batthern',
        'blu-stripes',
        'brushed-alum-dark',
        'checkered-pattern',
        'crissxcross',
        'diagonal-striped-brick',
        'grid-me',
        'lined-paper',
        'low-contrast-linen',
        'purty-wood',
        'random-grey-variations',
        'simple-dashed',
        'skulls',
        'subtle-zebra-3d',
        'textured-stripes',
        'tileable-wood',
        'vichy',
        'wavecut',
        'white-paperboard',
        'white-tiles',
        'zig-zag',
    ]

    template = '''
    <!DOCYPE html5>
    <html>
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css?family=Roboto+Slab:400&amp;subset=latin-ext" rel="stylesheet">
        <style>
            html {{
                margin: 0;
                padding: 0;
                width: 688px;
                background-color: {color};
                background-image: url("https://www.transparenttextures.com/patterns/{pattern}.png");
                zoom: {scale};
            }}
            p {{
                margin: 10px;
                padding: 0;
                font-family: 'Roboto Slab', serif;
                font-size: 18px;
                text-align: justify;
            }}
        </style>
    </head>
    <body>
        <p>{text}</p>
    </body>
    </html>
    '''

    color_values = colorsys.hsv_to_rgb(random.randint(0, 360) / 360.0, 0.2, 1.0)
    color_html = '#%02x%02x%02x' % (
        int(color_values[0] * 255),
        int(color_values[1] * 255),
        int(color_values[2] * 255),
    )

    pattern = random.choice(patterns)

    content = ''
    for line in text.content.split('\n'):
        content += '<p>{line}</p>'.format(line=line.strip())

    options = {
        'format': 'png',
        'encoding': 'UTF-8',
        'width': '1',
        'quiet': '',
    }

    html = template.format(color=color_html, pattern=pattern, scale=2, text=content)
    image = imgkit.from_string(html, False, options=options)
    file_name = FileSystemStorage().save(f'{text_id}.png', ContentFile(image))

    html_mini = template.format(color=color_html, pattern=pattern, scale=0.9, text=content)
    image_mini = imgkit.from_string(html_mini, False, options=options)
    file_name_mini = FileSystemStorage().save(f'{text_id}_mini.png', ContentFile(image_mini))

    text.add_processed_image(file_name, file_name_mini)
