import Image, ImageFont, ImageDraw, ImageChops

def generate_image(text, font_file, size, colour, image_destination):
    """
    Text transform based on:
    http://nedbatchelder.com/blog/200801/truly_transparent_text_with_pil.html
    http://phark.typepad.com/phark/2003/08/accessible_imag.html
    """
    pos = (0,0)
    image = Image.new("RGB", (1, 1), (0,0,0))
    font = ImageFont.truetype(font_file, size)
    image = image.resize(font.getsize(text))
    alpha = Image.new("L", image.size, "black")
    # Make a grayscale image of the font, white on black.
    imtext = Image.new("L", image.size, 0)
    drtext = ImageDraw.Draw(imtext)
    drtext.text(pos, text, font=font, fill="white")
    # Add the white text to our collected alpha channel. Gray pixels around
    # the edge of the text will eventually become partially transparent
    # pixels in the alpha channel.
    alpha = ImageChops.lighter(alpha, imtext)
    # Make a solid colour, and add it to the colour layer on every pixel
    # that has even a little bit of alpha showing.
    solidcolour = Image.new("RGBA", image.size, colour)
    immask = Image.eval(imtext, lambda p: 255 * (int(p != 0)))
    image = Image.composite(solidcolour, image, immask)
    # These two save()s are just to get demo images of the process.
    #image.save("transcolour.png", "PNG")
    #alpha.save("transalpha.png", "PNG")
    # Add the alpha channel to the image, and save it out.
    image.putalpha(alpha)
    image.save(image_destination, 'PNG')
    return image
