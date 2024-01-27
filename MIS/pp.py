import pygame
import sys
import random
from faker import Faker
from datetime import datetime, timedelta
 
# Inicijalizacija Pygame-a
pygame.init()
 
# Postavke prozora
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulacija čekanja pacijenata")
 
# Boje
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
emergency_red = (255, 50, 50)
 
# Fontovi
font_table_header = pygame.font.Font(None, 18)
font_table_data = pygame.font.Font(None, 18)
 
# Inicijalizacija reda
red_pacijenata = []
red_pacijenata_hitni = []
 
# Brojači pregledanih pacijenata
pregledani_obicni = 0
pregledani_hitni = 0
 
# Generiranje imena pacijenata pomoću faker
faker = Faker()
 
# Brojač rednog broja pacijenata
brojac_rednog_broja = 1
brojac_rednog_broja_hitni = 1
 
# Funkcija za generiranje random datuma rođenja
def random_datum_rodjenja():
    return faker.date_of_birth()
 
# Funkcija za izvršavanje pregleda pacijenta
def izvrsi_pregled(pacijent, trajanje):
    pacijent["gotov"] = True
    pacijent["vrijeme_zavrsetka"] = datetime.now() + timedelta(seconds=trajanje)
    if pacijent["hitno"]:
        # Povećaj brojač pregledanih hitnih pacijenata
        global pregledani_hitni
        pregledani_hitni += 1
    else:
        # Povećaj brojač pregledanih običnih pacijenata
        global pregledani_obicni
        pregledani_obicni += 1
# Glavna petlja igre
clock = pygame.time.Clock()
 
# Vremenski okviri za obične pacijente i hitne slučajeve
vrijeme_pojave_obicnih = 0
vrijeme_pregleda_obicnih = 0
vrijeme_pojave_hitnih = 0
vrijeme_pregleda_hitnih = 0
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    # Dodaj novog pacijenta u red svakih nekoliko sekundi
    vrijeme_pojave_obicnih += 1
    vrijeme_pojave_hitnih += 1
 
    if vrijeme_pojave_obicnih >=  random.randint(100, 500):
        vrijeme_pojave_obicnih = 0
        ime = faker.first_name()
        prezime = faker.last_name()
        datum_rodjenja = random_datum_rodjenja()
        pacijent = {
            "redni_broj": brojac_rednog_broja,
            "ime": ime,
            "prezime": prezime,
            "datum_rodjenja": datum_rodjenja,
            "vrijeme_dolaska": datetime.now(),
            "gotov": False,
            "hitno": False,
        }
        red_pacijenata.append(pacijent)
        brojac_rednog_broja += 1
 
    if vrijeme_pojave_hitnih >= 600:
        vrijeme_pojave_hitnih = 0
        ime = faker.first_name()
        prezime = faker.last_name()
        datum_rodjenja = random_datum_rodjenja()
        pacijent = {
            "redni_broj": brojac_rednog_broja_hitni,
            "ime": ime,
            "prezime": prezime,
            "datum_rodjenja": datum_rodjenja,
            "vrijeme_dolaska": datetime.now(),
            "gotov": False,
            "hitno": True,
        }
        red_pacijenata_hitni.append(pacijent)
        brojac_rednog_broja_hitni += 1
 
    # Provjerava i označava gotove pacijente (obični pacijenti)
    if red_pacijenata:
        pacijent = red_pacijenata[0]
        if not pacijent["gotov"] and vrijeme_pregleda_obicnih >= 100:  
            izvrsi_pregled(pacijent, 3)
            vrijeme_pregleda_obicnih = 0
        elif not pacijent["gotov"]:
            vrijeme_pregleda_obicnih += 1
 
    # Provjerava i označava gotove pacijente (hitni slučajevi)
    if red_pacijenata_hitni:
        pacijent_hitni = red_pacijenata_hitni[0]  # Uzmi prvog hitnog pacijenta u redu
        if not pacijent_hitni["gotov"] and vrijeme_pregleda_hitnih >=300:
            izvrsi_pregled(pacijent_hitni, 5)
            vrijeme_pregleda_hitnih = 0
        elif not pacijent_hitni["gotov"]:
            vrijeme_pregleda_hitnih += 1
 
    # Ukloni gotove pacijente nakon određenog vremena
    red_pacijenata = [p for p in red_pacijenata if not p["gotov"] or (p["gotov"] and (datetime.now() - p["vrijeme_zavrsetka"]).total_seconds() < 1)]
    red_pacijenata_hitni = [p for p in red_pacijenata_hitni if not p["gotov"] or (p["gotov"] and (datetime.now() - p["vrijeme_zavrsetka"]).total_seconds() < 1)]
 
    # Crta pozadinu
    screen.fill(white)
 
    # Font za naslove tablica s povećanim fontom
    font_table_header_obicni = pygame.font.Font(None, 28)
    font_table_header_hitni = pygame.font.Font(None, 28)
 
    # Crta naziv tablice (Manje bolesti pacijenti) s povećanim fontom
    header_text_obicni = font_table_header_obicni.render("Manje bolesti pacijenti", True, black)
    screen.blit(header_text_obicni, (50, 30))
 
    # Crta naziv tablice (HITNI SLUČAJ) s povećanim fontom
    header_text_hitni = font_table_header_hitni.render("HITNI SLUČAJ", True, red)
    screen.blit(header_text_hitni, (600, 30))
 
    # Crta zaglavlje tabele (obični pacijenti)
    header_text = font_table_header.render(
        "RB     | Ime i prezime                        | Datum rođenja      | Dolazak          | Završetak", True, black
    )
    screen.blit(header_text, (50, 73))
 
    # Crta zaglavlje tabele (hitni slučajevi)
    header_text_emergency = font_table_header.render(
        "RB     | Ime i prezime                        | Datum rođenja      | Dolazak          | Završetak", True, red
    )
    screen.blit(header_text_emergency, (600, 73))
 
   # Prikaz broja pregledanih pacijenata
    font_brojac = pygame.font.Font(None, 24)
 
    # Tekst za "Pregledano->"
    screen.blit(font_brojac.render("Pregledano->", True, red), (50, height - 30))
 
    # Tekst za preostali dio
    screen.blit(font_brojac.render(f"Manje bolesni pacijenti: {pregledani_obicni}  |  Hitni slučajevi: {pregledani_hitni}", True, black), (180, height - 30))
 
 
    # Crta redove pacijenata u tablici (obični pacijenti)
    for i, pacijent in enumerate(red_pacijenata):
        boja = green if pacijent["gotov"] and not pacijent["hitno"] else black
 
        rb_rect = pygame.Rect(50, 90 + i * 30, 30, 30)
        ime_rect = pygame.Rect(85, 90 + i * 30, 150, 30)
        datum_rect = pygame.Rect(240, 90 + i * 30, 90, 30)
        dolazak_rect = pygame.Rect(335, 90 + i * 30, 90, 30)
        zavrsetak_rect = pygame.Rect(430, 90 + i * 30, 90, 30)
 
        pygame.draw.rect(screen, boja, rb_rect)
        pygame.draw.rect(screen, boja, ime_rect)
        pygame.draw.rect(screen, boja, datum_rect)
        pygame.draw.rect(screen, boja, dolazak_rect)
        pygame.draw.rect(screen, boja, zavrsetak_rect)
 
        rb_text = font_table_data.render(f"{pacijent['redni_broj']}", True, white)
        ime_text = font_table_data.render(f"{pacijent['ime']} {pacijent['prezime']}", True, white)
        datum_text = font_table_data.render(f"{pacijent['datum_rodjenja'].strftime('%d.%m.%Y')}", True, white)
        dolazak_text = font_table_data.render(f"{pacijent['vrijeme_dolaska'].strftime('%H:%M:%S')}", True, white)
        zavrsetak_text = font_table_data.render(
            f"{pacijent['vrijeme_zavrsetka'].strftime('%H:%M:%S')}" if pacijent["gotov"] else "-", True, white
        )
 
        screen.blit(rb_text, rb_rect.move(5, 5))
        screen.blit(ime_text, ime_rect.move(5, 5))
        screen.blit(datum_text, datum_rect.move(5, 5))
        screen.blit(dolazak_text, dolazak_rect.move(5, 5))
        screen.blit(zavrsetak_text, zavrsetak_rect.move(5, 5))
 
    # Crta redove pacijenata u tablici (hitni slučajevi)
    for i, pacijent in enumerate(red_pacijenata_hitni):
        boja = emergency_red if not pacijent["gotov"] else green
 
        rb_rect = pygame.Rect(600, 90 + i * 30, 30, 30)
        ime_rect = pygame.Rect(635, 90 + i * 30, 150, 30)
        datum_rect = pygame.Rect(790, 90 + i * 30, 90, 30)
        dolazak_rect = pygame.Rect(885, 90 + i * 30, 90, 30)
        zavrsetak_rect = pygame.Rect(980, 90 + i * 30, 90, 30)
 
        pygame.draw.rect(screen, boja, rb_rect)
        pygame.draw.rect(screen, boja, ime_rect)
        pygame.draw.rect(screen, boja, datum_rect)
        pygame.draw.rect(screen, boja, dolazak_rect)
        pygame.draw.rect(screen, boja, zavrsetak_rect)
 
        rb_text = font_table_data.render(f"{pacijent['redni_broj']}", True, white)
        ime_text = font_table_data.render(f"{pacijent['ime']} {pacijent['prezime']}", True, white)
        datum_text = font_table_data.render(f"{pacijent['datum_rodjenja'].strftime('%d.%m.%Y')}", True, white)
        dolazak_text = font_table_data.render(f"{pacijent['vrijeme_dolaska'].strftime('%H:%M:%S')}", True, white)
        zavrsetak_text = font_table_data.render(
            f"{pacijent['vrijeme_zavrsetka'].strftime('%H:%M:%S')}" if pacijent["gotov"] else "-", True, white
        )
 
        screen.blit(rb_text, rb_rect.move(5, 5))
        screen.blit(ime_text, ime_rect.move(5, 5))
        screen.blit(datum_text, datum_rect.move(5, 5))
        screen.blit(dolazak_text, dolazak_rect.move(5, 5))
        screen.blit(zavrsetak_text, zavrsetak_rect.move(5, 5))
 
    # Prikazuje promjene na ekranu
    pygame.display.flip()
 
    # Postavlja broj sličica u sekundi (FPS)
    clock.tick(30)