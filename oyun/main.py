import random
import tkinter as tk
import tkinter.messagebox as messagebox
import string
# Kelime ve ipucu listesi
kelimeler = {
    "avakado": ("meyve", "Ülkemizin belirli bölgelerde de yetişen tropikal bir meyve"),
    "emily in paris": ("dizi", "Başrolde renkli kıyafetleriyle dikkat çeken bir genç kadın bir dizi serisi"),
    "aşk-ı memnu": ("roman", "Dizisiyle de meşhur bir Türk yazar tarafından yazılmış bir roman"),
    "yapay zeka mühendisliği": ("meslek", "Kodlama yapan bir meslek türü"),
    "bitlis'te beş minare": ("şarkı", "İçinde bir ilimizin isminin geçtiği bir şarkı"),
    "isviçre": ("ülke", "Dağlarıyla meşhur bir ülke"),
    "ters yüz": ("animasyon", "Ana teması duygulardan oluşan bir animasyon"),
    "antilop": ("hayvan", "Türlerinin çoğunun Afrika'da yaşadığı bir hayvan"),
    "aydın": ("şehir", "Bir yaz meyvesiyle meşhur bir ilimiz"),
    "semicenk": ("müzisyen", "Son zamanların en popüler müzisyenlerinden biri"),
    "badminton": ("spor", "Raket ve top ile oynanan bir tür spor")
}

# Kelime seçiminde tek kelimeli veya iki kelimeli kelimeleri ayıralım
kelime_secilen = []

# Rastgele kelime seçimi
def kelime_seç():
    global kelime_secilen

    if len(kelime_secilen) == len(kelimeler):
        # Tüm kelimeler seçildiğinde listeyi sıfırla
        kelime_secilen = []

    kelime = random.choice(list(kelimeler.keys()))

    # Seçilen kelime daha önce seçilmediyse ekle
    while kelime in kelime_secilen:
        kelime = random.choice(list(kelimeler.keys()))

    kelime_secilen.append(kelime)
    return kelime, kelimeler[kelime]

rastgele_kelime, (kelime_turu, ipucu) = kelime_seç()
tahmin_hakki = 5
ipucu_hakkı = 1
harf_hakkı = 2
gosterilen_harfler = set()

# Oyun penceresi
pencere = tk.Tk()
pencere.title("Kelime Tahmin Oyunu")
pencere.attributes('-fullscreen', True)
pencere.configure(bg="pink")

# Ortalamak için boş bir çerçeve
frame = tk.Frame(pencere, bg="pink")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Kelime türleri Label
kelime_turleri_label = tk.Label(frame, text=f"Bu kelime bir: {kelime_turu}", bg="pink", font=("Times New Roman", 27))
kelime_turleri_label.grid(row=0, column=0, columnspan=4, pady=10)

# Kelimenin harf sayısı
kelime_harf_sayisi_label = tk.Label(frame, text=f"Kelimenin harf sayısı: {len(rastgele_kelime.replace(' ', '').translate(str.maketrans('', '', string.punctuation)))}", bg="pink", font=("Times New Roman", 27))
kelime_harf_sayisi_label.grid(row=1, column=0, columnspan=4, pady=10)

# İpucu Label
ipucu_label = tk.Label(frame, text="Bu kelime ile ilgili bir şey tahmin ediniz.", bg="pink", font=("Times New Roman", 27))
ipucu_label.grid(row=2, column=0, columnspan=4, pady=10)

# Tahmin girişi
tahmin_entry = tk.Entry(frame, font=("Times New Roman", 18))
tahmin_entry.grid(row=3, column=0, columnspan=4, pady=10)

# Sonuç Label
sonuc_label = tk.Label(frame, text=f"{tahmin_hakki} tahmin hakkınız var. İpucu alma hakkınız: {ipucu_hakkı}, Harf alma hakkınız: {harf_hakkı}",
                       bg="pink", font=("Times New Roman", 27))
sonuc_label.grid(row=4, column=0, columnspan=4, pady=10)

def ozellestirilmis_bildirim(title, message, durum):
    bildirim_penceresi = tk.Toplevel()
    bildirim_penceresi.title(title)
    bildirim_penceresi.geometry("450x150")

    # Duruma göre arka plan rengi ayarlanıyor
    if durum == "dogru":
        bildirim_penceresi.configure(bg="lightgreen")
    elif durum == "yanlis":
        bildirim_penceresi.configure(bg="lightcoral")
    else:
        bildirim_penceresi.configure(bg="pink")  # Diğer durumlar için standart renk

    # Ekranın ortasına yerleştir
    x = (pencere.winfo_width() // 2) - (450 // 2)
    y = (pencere.winfo_height() // 2) - (150 // 2)
    bildirim_penceresi.geometry(f"450x150+{x}+{y}")

    # Mesaj Label
    mesaj_label = tk.Label(bildirim_penceresi, text=message, bg=bildirim_penceresi['bg'], font=("Times New Roman", 16))
    mesaj_label.pack(pady=20)

    # Tamam Butonu
    tamam_butonu = tk.Button(bildirim_penceresi, text="Tamam", command=lambda: [bildirim_penceresi.destroy(), yeniden_baslat() if durum == "dogru" else None], bg="lightblue", font=("Times New Roman", 12))
    tamam_butonu.pack(pady=10)

    bildirim_penceresi.transient(pencere)  # Ana pencere üzerine yerleştir
    bildirim_penceresi.grab_set()  # Kullanıcının bu pencere dışında bir şey yapmasını engelle

def yuvarlak_buton(master, text, command):
    # Canvas oluştur
    canvas = tk.Canvas(master, width=150, height=50, bg="pink", highlightthickness=0)
    canvas.create_oval(5, 5, 145, 45, fill="lightblue", outline="")

    # Buton oluştur
    button = tk.Button(canvas, text=text, command=command, bg="lightblue", font=("Times New Roman", 18), relief=tk.FLAT)
    button.place(x=0, y=0, relwidth=1, relheight=1)

    # Butona fare ile üzerine gelme ve çıkma efektleri
    def on_enter(e):
        button['bg'] = 'lightpink'

    def on_leave(e):
        button['bg'] = 'lightblue'

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return canvas

def tahmin_et():
    global tahmin_hakki
    tahmin = tahmin_entry.get().lower().strip()
    temizle_giris()

    if tahmin == "":
        messagebox.showwarning("Uyarı", "Lütfen bir tahmin girin.")
        return

    if tahmin == rastgele_kelime:
        ozellestirilmis_bildirim("Sonuç", "Doğru tahmin! Oyunu kazandınız.", "dogru")
    else:
        tahmin_hakki -= 1
        if tahmin_hakki > 0:
            ozellestirilmis_bildirim("Yanlış Tahmin", f"Yanlış tahmin. Kalan tahmin hakkı: {tahmin_hakki}.", "yanlis")
            sonuc_label.config(text=f"{tahmin_hakki} tahmin hakkınız var. İpucu alma hakkınız: {ipucu_hakkı}, Harf alma hakkınız: {harf_hakkı}")
        else:
            ozellestirilmis_bildirim("Sonuç", f"Tahmin hakkınız kalmadı! Doğru kelime: {rastgele_kelime}", "yanlis")
            oyun_bitis()

def ipucu_al():
    global ipucu_hakkı
    if ipucu_hakkı > 0:
        ozellestirilmis_bildirim("İpucu", ipucu, "bilgi")
        ipucu_hakkı -= 1
        sonuc_label.config(text=f"{tahmin_hakki} tahmin hakkınız var. İpucu alma hakkınız: {ipucu_hakkı}, Harf alma hakkınız: {harf_hakkı}")
    else:
        ozellestirilmis_bildirim("İpucu", "İpucu alma hakkınız kalmadı!", "yanlis")

def harf_al():
    global harf_hakkı
    if harf_hakkı > 0:
        harf_index = random.randint(0, len(rastgele_kelime) - 1)
        harf = rastgele_kelime[harf_index]
        if harf not in gosterilen_harfler:
            gosterilen_harfler.add(harf)
            ozellestirilmis_bildirim("Harf", f"Kelimenin içinde geçen bir harf: '{harf}' (Harf sırası: {harf_index + 1})", "bilgi")
            harf_hakkı -= 1
            sonuc_label.config(text=f"{tahmin_hakki} tahmin hakkınız var. İpucu alma hakkınız: {ipucu_hakkı}, Harf alma hakkınız: {harf_hakkı}")
        else:
            ozellestirilmis_bildirim("Harf", "Bu harfi zaten gösterdiniz!", "bilgi")
    else:
        ozellestirilmis_bildirim("Harf", "Harf alma hakkınız kalmadı!", "yanlis")

def temizle_giris():
    tahmin_entry.delete(0, tk.END)

def oyun_bitis():
    if messagebox.askyesno("Oyun Bitti", "Oyunu yeniden başlatmak ister misiniz?"):
        yeniden_baslat()
    else:
        pencere.quit()

def yeniden_baslat():
    global tahmin_hakki, ipucu_hakkı, harf_hakkı, rastgele_kelime, kelime_turu, ipucu, gosterilen_harfler
    tahmin_hakki = 5
    ipucu_hakkı = 1
    harf_hakkı = 2
    gosterilen_harfler.clear()
    rastgele_kelime, (kelime_turu, ipucu) = kelime_seç()
    kelime_turleri_label.config(text=f"Bu kelime bir: {kelime_turu}")
    kelime_harf_sayisi_label.config(text=f"Kelimenin harf sayısı: {len(rastgele_kelime)}")
    sonuc_label.config(text=f"{tahmin_hakki} tahmin hakkınız var. İpucu alma hakkınız: {ipucu_hakkı}, Harf alma hakkınız: {harf_hakkı}")
    temizle_giris()

def kapat():
    pencere.quit()

# Butonları oluştur
tahmin_butonu = yuvarlak_buton(frame, "Tahmin Et", tahmin_et)
ipucu_butonu = yuvarlak_buton(frame, "İpucu Al", ipucu_al)
harf_butonu = yuvarlak_buton(frame, "Harf Al", harf_al)
kapatma_butonu = yuvarlak_buton(frame, "Kapat", kapat)

# Butonları yan yana yerleştir
tahmin_butonu.grid(row=5, column=0, padx=10, pady=10)
ipucu_butonu.grid(row=5, column=1, padx=10, pady=10)
harf_butonu.grid(row=5, column=2, padx=10, pady=10)
kapatma_butonu.grid(row=5, column=3, padx=10, pady=10)

# Pencereyi başlat
pencere.mainloop()
