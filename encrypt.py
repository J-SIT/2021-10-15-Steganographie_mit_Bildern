from PIL import Image
import bitarray


def file_to_bitarray(path):
    result = bitarray.bitarray()
    with open(path, 'rb') as file:
        result.fromfile(file)
    return result


def bitarray_to_file(path, bits):
    with open(path, 'wb') as file:
        bits.tofile(file)


def set_last_bit(value, integer):
    bits = '{0:b}'.format(integer)
    return int(bits[0:len(bits) - 1] + str(value), 2)


def get_last_bit(integer):
    bits = '{0:b}'.format(integer)
    return int(bits[len(bits) - 1])


def hide(pfad, nachricht, ausgabe):
    im = Image.open(pfad)
    pic = im.load()
    width, height = im.size
    to_hide = file_to_bitarray(nachricht)
    k = 0
    l = len(to_hide)
    for y in range(height):
        for x in range(width):
            pixel = pic[x, y]
            r = set_last_bit(to_hide[k % l], pixel[0])
            k += 1
            g = set_last_bit(to_hide[k % l], pixel[1])
            k += 1
            b = set_last_bit(to_hide[k % l], pixel[2])
            k += 1
            pic[x, y] = (r, g, b)

    im.save(ausgabe)
    status = True
    return status


def seek(pfad, nachricht):
    im = Image.open(pfad)
    pic = im.load()
    width, height = im.size
    bits = ''
    for y in range(height):
        for x in range(width):
            pixel = pic[x, y]
            bits += str(get_last_bit(pixel[0]))
            bits += str(get_last_bit(pixel[1]))
            bits += str(get_last_bit(pixel[2]))
    bitarray_to_file(nachricht, bitarray.bitarray(bits))
    status = True
    return status


# hide()

# seek(out_file = 'extract.txt')


print(" Nachrichten-Kaskaden-System 1.0 [SIT]")
print()
print("Wählen Sie: [1] um eine Nachricht zu erstellen.")
print("Wählen Sie: [2] um eine Nachricht zu entschlüsseln.")
print()
modus = int(input("Wählen Sie: "))

if modus == 1:
    print(" -- Nachricht in Bild hinterlegen -- [SIT] -- ")
    print()
    pfad = input(" Gib den Bild-Dateinamen ein. | Bsp. [C:\\bild.png] : ")
    print(" -- 1 / 3 --")
    nachricht = input(" Gib den Nachrichten-Dateinamen ein. | Bsp. [C:\\nachricht.txt] : ")
    print(" -- 2 / 3 --")
    ausgabe = input("Gib den Bild-Datei-Ausgabenamen ein. | Bsp. [C:\\ausgabe.png] : ")
    print(" -- 3 / 3 --")
    status = hide(pfad, nachricht, ausgabe)
    if status:
        print(" Vorgang erfolgreich abgeschlossen. ")
    else:
        print(" ...ein Fehler ist aufgetreten...")


elif modus == 2:
    print(" -- Nachricht aus Bild extrahieren -- [SIT] -- ")
    print()
    pfad = input(" Gib den Bild-Dateinamen ein. | Bsp. [C:\\bild.png] : ")
    print(" -- 1 / 2 --")
    nachricht = input(" Gib den Nachrichten-Dateinamen für die extrahierte Nachricht an. | Bsp. [C:\\nachricht.txt] : ")
    print(" -- 2 / 2 --")
    status = seek(pfad, nachricht)
    if status:
        print(" Vorgang erfolgreich abgeschlossen. ")
    else:
        print(" ...ein Fehler ist aufgetreten...")

else:
    print(" Falsche eingabe! ")
