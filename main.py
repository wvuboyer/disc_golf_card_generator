import argparse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def create_pdf(output_filename, logo_file, cards_text):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    card_height = height / 3
    
    c.setFont("Helvetica-Bold", 36)
    
    if logo_file:
        image_path = logo_file
        image_width = 2 * inch
        image_height = 2 * inch
    
    for i, card in enumerate(cards_text):
        if i > 0 and i % 3 == 0:
            c.showPage()
            c.setFont("Helvetica-Bold", 36)
            
        card_index_on_page = i % 3
        y_position = height - (card_index_on_page + 1) * card_height

        text_y_position = y_position + card_height - (0.75 * inch)

        c.drawString(0.5 * inch, text_y_position, card['name'])
        
        c.drawRightString(width - 0.5 * inch, text_y_position, card['division'])
        
        if logo_file:
            image_x_position = (width - image_width) - 0.4 * inch
            image_y_position = y_position + (card_height - image_height) / 2 - (0.5 * inch)

            try:
                c.drawImage(image_path, image_x_position, image_y_position, width=image_width, height=image_height, mask='auto')
            except OSError:
                print("Could not open logo file.")
                exit(99)

        if card_index_on_page < 2 or (i == (len(cards_text) - 1) and card_index_on_page < 2):
            c.setDash(1, 20)
            c.setStrokeColor(colors.black)
            line_y_position = y_position
            c.line(0.25 * inch, line_y_position, width - 0.25 * inch, line_y_position)
            c.setDash()
    
    c.save()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate PDF cards with custom images and text")
    parser.add_argument(
        '--logo_file',
        type=str,
        help="Path to the logo file (e.g., logo.png)"
    )
    parser.add_argument(
        '--output_file',
        type=str,
        help="The name of the output PDF file (e.g., output.pdf)"
    )
    return parser.parse_args()


if __name__ == '__main__':
    cards_text = [
        {"name": "John Doe", "division": "MA1"},
        {"name": "Jane Doe", "division": "FA1"},
        {"name": "Johnny Doe", "division": "MPO"},
        {"name": "Jennie Doe", "division": "FPO"},
    ]
    args = parse_arguments()
    
    create_pdf(args.output_file, args.logo_file, cards_text)
