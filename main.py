import pyautogui
import cv2
import numpy as np
import easyocr
import re
import time

tp_max = 100
rp_max = 5

tp_x1 = 478
tp_y1 = 31
tp_x2 = 553
tp_y2 = 47
tp_largura = tp_x2 - tp_x1
tp_altura = tp_y2 - tp_y1
regiao_tp = (tp_x1, tp_y1, tp_largura, tp_altura)

rp_x1 = 694
rp_y1 = 31
rp_x2 = 724
rp_y2 = 47
rp_largura = rp_x2 - rp_x1
rp_altura = rp_y2 - rp_y1
regiao_rp = (rp_x1, rp_y1, rp_largura, rp_altura)


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
    if len(numbers) >= 1:
        return int(numbers[0])
    return None


def main():
    pyautogui.PAUSE = 0.5

    print("Comecando sleep 1 segundos")
    time.sleep(1)
    print("Executando")

    location = None
    try:
        if pyautogui.locateOnScreen("screenshots/menu/buttons/insideHome_button.png", confidence=0.8):
            location = "home"
    except Exception:
        print("Nao esta em home")

    if location is None:
        try:
            home_location = pyautogui.locateOnScreen("screenshots/menu/buttons/home_button.png", confidence=0.8)
            if home_location:
                pyautogui.click(home_location)
        except Exception:
            print("Algum erro ocorreu ao tentar identificar o botao home, menu atual desconhecido.")
            home_location = None

    img_tp = pyautogui.screenshot(region=regiao_tp)
    img_tp.save('screenshots/temp/tp.png')
    img_tp = np.array(img_tp)

    img_rp = pyautogui.screenshot(region=regiao_rp)
    img_rp.save('screenshots/temp/rp.png')
    img_rp = np.array(img_rp)

    img_rp_mask = filtro_azul(img_rp)
    cv2.imwrite('screenshots/temp/rp_mask.png', img_rp_mask)

    text_tp = easyocr_text(img_tp)
    print("Texto detectado:", text_tp)

    text_rp = easyocr_text(img_rp_mask)
    print("Texto detectado:", text_rp)

    tp_atual = extrair_tprp(text_tp)
    if tp_atual is not None:
        print(f"TP atual: {tp_atual} de {tp_max}")
    else:
        print("Nao foi possivel detectar o TP atual.")

    rp_atual = extrair_tprp(text_rp)
    if rp_atual is not None:
        print(f"RP atual: {rp_atual} de {rp_max}")
    else:
        print("Nao foi possivel detectar o RP atual.")


if __name__ == "__main__":
    main()
