def main():
    x =pozitif_sayi()
    print(x)
def pozitif_sayi():
    while True:
        sayi = int(input("Pozitif bir sayı giriniz:"))
        if sayi>0:
            break
    return sayi
main()