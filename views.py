import os
import uuid
import textwrap
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont, ImageOps

def generate_and_send_poster(request):
    if request.method == "POST":
        # DEBUG: Check what button was clicked
        print(f"POST Data Received: {request.POST.keys()}")

        # --- STEP 2: EMAIL SENDING LOGIC ---
        # This MUST match the 'name' attribute of the button in your HTML
        if 'confirm_send' in request.POST:
            print("Confirm Send Button Clicked!")
            filename = request.POST.get('filename')
            email_to = request.POST.get('email')
            title = request.POST.get('title')
            
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            print(f"Attempting to send {filename} to {email_to}")

            try:
                email = EmailMessage(
                    subject=f"Event Poster: {title}",
                    body="Attached is your generated poster.",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email_to],
                )
                
                if os.path.exists(file_path):
                    email.attach_file(file_path)
                    email.send()
                    print("Email Sent Successfully!")
                    # THIS IS THE SUCCESS REDIRECT
                    return render(request, 'success.html', {'email': email_to})
                else:
                    print(f"Error: File not found at {file_path}")
                    return render(request, 'poster_form.html', {'error': "Image file was lost. Please regenerate."})
            
            except Exception as e:
                print(f"SMTP Error: {e}")
                return render(request, 'poster_form.html', {'error': f"Mail Error: {str(e)}"})

        # --- STEP 1: POSTER GENERATION LOGIC ---
        print("Generating Poster Preview...")
        title = request.POST.get('title', 'EVENT TITLE').upper()
        speaker = request.POST.get('speaker', '').upper()
        date_str = request.POST.get('date', '').upper()
        coord = request.POST.get('coordinator', '').upper()
        description = request.POST.get('description', '')
        email_to = request.POST.get('email')

        # [Keep all your PIL Drawing code here exactly as it was]
        # ... (Canvas, Fonts, draw_centered, etc.) ...
        width, height = 1080, 1500
        bg_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'template.png')
        poster = Image.open(bg_path).convert("RGB").resize((width, height)) if os.path.exists(bg_path) else Image.new('RGB', (width, height), color=(12, 12, 28))
        draw = ImageDraw.Draw(poster)
        win_fonts = "C:/Windows/Fonts/"

        def draw_centered(y, text, font, color):
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            draw.text(((width - w) / 2, y), text, fill=color, font=font)

        title_size = 150
        f_main = ImageFont.truetype(os.path.join(win_fonts, "ariblk.ttf"), title_size)
        while draw.textbbox((0, 0), title, font=f_main)[2] > 900 and title_size > 50:
            title_size -= 10
            f_main = ImageFont.truetype(os.path.join(win_fonts, "ariblk.ttf"), title_size)

        f_script = ImageFont.truetype(os.path.join(win_fonts, "ITCEDSCR.TTF"), 180)
        f_desc = ImageFont.truetype(os.path.join(win_fonts, "arial.ttf"), 38)
        f_detail = ImageFont.truetype(os.path.join(win_fonts, "arialbd.ttf"), 50)
        f_header = ImageFont.truetype(os.path.join(win_fonts, "arialbd.ttf"), 22)

        draw_centered(100, "STUDENT COUNCIL & TECH CLUB PRESENTS", f_header, (200, 200, 200))
        draw_centered(280, title, f_main, "white")
        lines = textwrap.wrap(description, width=55)
        curr_y = 480
        for line in lines:
            draw_centered(curr_y, line, f_desc, (180, 180, 180))
            curr_y += 50
        draw_centered(850, "details", f_script, (0, 255, 255)) 
        draw.line([(240, 1030), (830, 1030)], fill="white", width=6)
        draw_centered(1100, f"DATE: {date_str}", f_detail, "white")
        speaker_text = f"RESOURCE PERSON: {speaker}"
        f_spk = f_detail
        if len(speaker_text) > 30:
            f_spk = ImageFont.truetype(os.path.join(win_fonts, "arialbd.ttf"), 38)
        draw_centered(1200, speaker_text, f_spk, (0, 255, 255))
        draw_centered(1290, f"HOSTED BY: {coord}", f_detail, "white")
        draw_centered(1420, "WWW.STUDCOUNCIL.EDU.IN", f_header, (150, 150, 150))

        if not os.path.exists(settings.MEDIA_ROOT): os.makedirs(settings.MEDIA_ROOT)
        filename = f"prev_{uuid.uuid4().hex[:6]}.png"
        output_path = os.path.join(settings.MEDIA_ROOT, filename)
        poster.save(output_path)

        # Rendering Preview
        return render(request, 'poster_preview.html', {
            'image_url': f"{settings.MEDIA_URL}{filename}",
            'filename': filename, 
            'email': email_to, 
            'title': title
        })

    return render(request, 'poster_form.html')