scores = []
for i in range(3):
    scores.append(int(input("Bir not giriniz:")))

ortalama = str(sum(scores) / len(scores))
print(f"Ortalama {ortalama}")