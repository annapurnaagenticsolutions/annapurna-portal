"""
Project 06: QR Code Art

Hidden Gem: `qrcode` with `pillow` — generates stylized QR codes with
custom colors, embedded logos, and artistic patterns.

What it does: Creates visually appealing QR codes with custom styling
that still scan correctly. Demonstrates QR code generation with aesthetics.
"""
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw
import os


def generate_styled_qr(data, output_path="qr_art.png", fill_color="#1a1a2e",
                       back_color="#e94560", dot_color="#0f3460"):
    """Generate a styled QR code with custom colors."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img = img.convert("RGB")
    return img


def generate_gradient_qr(data, output_path="qr_gradient.png"):
    """Generate a QR code with a gradient background."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.convert("RGB")
    pixels = img.load()

    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            if r == 0 and g == 0 and b == 0:
                # Replace black with gradient
                t = x / w
                pixels[x, y] = (
                    int(30 + t * 100),
                    int(60 + t * 80),
                    int(120 + t * 60),
                )

    return img


def generate_rounded_qr(data, output_path="qr_rounded.png"):
    """Generate a QR code with rounded dot styling."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    matrix = qr.modules
    size = len(matrix)
    scale = 12
    border = 4 * scale

    img_size = size * scale + 2 * border
    img = Image.new("RGB", (img_size, img_size), (245, 245, 250))
    draw = ImageDraw.Draw(img)

    for y in range(size):
        for x in range(size):
            if matrix[y][x]:
                px = x * scale + border
                py = y * scale + border
                radius = scale // 3
                draw.rounded_rectangle(
                    [px, py, px + scale, py + scale],
                    radius=radius,
                    fill=(30, 60, 120),
                )

    return img


def main():
    data = "https://github.com/annapurna-agentics"
    print(f"--- QR Code Art Generator ---")
    print(f"Encoding: {data}")

    try:
        # Style 1: Custom colors
        img1 = generate_styled_qr(data)
        img1.save("qr_styled.png")
        print("✓ Styled QR saved: qr_styled.png")

        # Style 2: Gradient
        img2 = generate_gradient_qr(data)
        img2.save("qr_gradient.png")
        print("✓ Gradient QR saved: qr_gradient.png")

        # Style 3: Rounded dots
        img3 = generate_rounded_qr(data)
        img3.save("qr_rounded.png")
        print("✓ Rounded QR saved: qr_rounded.png")

        print(f"\n3 QR code variants generated. Scan them to test!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
