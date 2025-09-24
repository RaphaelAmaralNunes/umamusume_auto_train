import pyautogui
import cv2
import numpy as np
import easyocr
import re
import time

rp_x1 = 694
rp_y1 = 31

rp_x2 = 724
rp_y2 = 47

rp_largura = rp_x2 - rp_x1
rp_altura = rp_y2 - rp_y1

print("Comecando sleep 1 segundos")
time.sleep(1)
print("Executando")


def capturar_regiao(r):
    screenshot = pyautogui.screenshot(region=r)
    return np.array(screenshot)


def filtro_azul(img_np):
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(img_np, img_np, mask=mask)
    return result


def easyocr_text(img_np):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(img_np)
    text = ' '.join(res[1] for res in results)
    return text


def extrair_tprp(text):
    numbers = re.findall(r'\d+', text)
    if len(numbers) >= 2:
        return int(numbers[0]), int(numbers[1])
    return None, None


def main():
    regiao_rp = (rp_x1, rp_y1, rp_largura, rp_altura)

    img = pyautogui.screenshot(region=regiao_rp)
    img.save('screenshots/menu/rp.png')
    img_np = np.array(img)
    rp_mask = filtro_azul(img_np)
    cv2.imwrite('screenshots/menu/rp_mask.png', rp_mask)

    text = easyocr_text(rp_mask)
    print("Texto detectado:", text)

    rp_atual, rp_max = extrair_tprp(text)
    if rp_atual is not None:
        print(f"RP atual: {rp_atual} de {rp_max}")
    else:
        print("Nao foi possivel detectar o RP atual.")


if __name__ == "__main__":
    main()
