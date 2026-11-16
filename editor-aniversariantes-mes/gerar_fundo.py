"""Gera fundo-modelo.jpg a partir da arte original:
- apaga o subtítulo "aniversariantes de ...", a lista de datas/nomes e a logo antiga;
- troca o azul escuro da arte pelo azul da NTW (#09509E).
Requer: pip install pillow numpy opencv-python-headless
"""
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np, cv2

AQUI = Path(__file__).parent
im = Image.open(AQUI / "modelo-original.webp").convert("RGB")
a = np.array(im).astype(float)
H, W = a.shape[:2]
yy, xx = np.mgrid[0:H, 0:W]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
tinta = (r < 120) & (b - r > 40)

# 1) subtítulo em arco (círculo de centro (520,1316) e raio ~1078 na linha de base)
dist = np.hypot(xx - 520, yy - 1316.5)
arco = (dist > 1062) & (dist < 1131) & (xx > 128) & (xx < 900) & (yy < 330)
m_arco = (tinta & arco).astype(np.uint8) * 255
m_arco = cv2.dilate(m_arco, np.ones((7, 7), np.uint8))

# 2) logo antiga no rodapé
caixa = (xx > 278) & (xx < 778) & (yy > 1338) & (yy < 1482)
claro = (r > 200) & (g > 225)
m_logo = cv2.dilate(((caixa & ~claro).astype(np.uint8) * 255), np.ones((7, 7), np.uint8))

bgr = cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2BGR)
bgr = cv2.inpaint(bgr, np.maximum(m_arco, m_logo), 9, cv2.INPAINT_TELEA)
a = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(float)

# 3) área da lista: interpola o fundo entre as laterais (x=195 e x=845), linha a linha
x0, x1, y0, y1 = 195, 845, 348, 1010
def suaviza(col):  # mediana móvel vertical para ignorar riscos/enfeites nas laterais
    return np.array([np.median(col[max(0, i - 30):i + 31], axis=0) for i in range(len(col))])
esq = suaviza(np.median(a[y0:y1, x0 - 6:x0], axis=1))
dir_ = suaviza(np.median(a[y0:y1, x1:x1 + 6], axis=1))
t = np.linspace(0, 1, x1 - x0)[None, :, None]
a[y0:y1, x0:x1] = esq[:, None, :] * (1 - t) + dir_[:, None, :] * t
reg = Image.fromarray(a[y0 - 4:y1 + 4, x0 - 4:x1 + 4].astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
a[y0:y1, x0:x1] = np.array(reg).astype(float)[4:-4, 4:-4]

# 4) azul escuro da arte -> azul NTW
TINTA, NTW = np.array([4, 49, 131.]), np.array([9, 80, 158.])
peso = np.clip((255 - a[..., 0]) / 251, 0, 1) ** 1.5
peso[(a[..., 2] - a[..., 0]) < 30] = 0
a = a + peso[..., None] * (NTW - TINTA)

Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(AQUI / "fundo-modelo.jpg", quality=93)
print("OK", W, H)

# 5) camadas para trocar cores no editor: R = balões, G = caixa de presente, B = textos/enfeites
orig = np.array(im).astype(float)
ro = orig[..., 0]
def preenche(m):
    """fecha e preenche buracos (brilhos dos balões)"""
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    inv = (m == 0).astype(np.uint8)
    cnt = inv.copy(); h, w = m.shape
    mask_ff = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(cnt, mask_ff, (0, 0), 2)
    return np.where(cnt == 1, 255, m).astype(np.uint8)

objeto = (ro < 175).astype(np.uint8) * 255
def regiao(x0, y0, x1, y1):
    r_ = np.zeros((H, W), np.uint8); r_[y0:y1, x0:x1] = 255; return r_
def sem_pequenos(m, minimo=400):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    out = np.zeros_like(m)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= minimo: out[lab == i] = 255
    return out
escuro = (ro < 45) & ((orig[..., 2] - ro) > 60)   # tinta: textos, riscos, corações
# riscos decorativos (pequenos traços escuros nas laterais) não fazem parte dos balões
esc8 = ((ro < 60) & ((orig[..., 2] - ro) > 60)).astype(np.uint8)
n_, lab_, st_, _ = cv2.connectedComponentsWithStats(esc8)
riscos = np.zeros((H, W), np.uint8)
for i in range(1, n_):
    x, y, w, h, area = st_[i]
    if 80 < area < 1200 and w < 100 and h < 100 and x > 0 and y < 1000 and (x < 200 or x + w > 830):
        riscos[lab_ == i] = 255
perto_riscos = cv2.dilate(riscos, np.ones((9, 9), np.uint8))
obj_sem_riscos = objeto & ~perto_riscos
bal_esq = preenche(sem_pequenos(obj_sem_riscos & regiao(0, 0, 165, 645)))
bal_dir = preenche(sem_pequenos(obj_sem_riscos & regiao(884, 275, W, 805)))
bal_cor = sem_pequenos(cv2.morphologyEx(((ro < 160).astype(np.uint8) * 255) & regiao(848, 1035, 1015, 1490), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)), 1500)
baloes = np.maximum.reduce([bal_esq, bal_dir, bal_cor])
baloes[perto_riscos > 0] = 0
reg_pres = np.maximum(regiao(0, 1190, 292, H), regiao(0, 1150, 232, H))
presente = preenche(sem_pequenos(objeto & reg_pres))
# tinta fora dos objetos (o arco, a lista e a logo apagados não contam)
tinta_m = (escuro.astype(np.uint8) * 255)
tinta_m[(baloes > 0) | (presente > 0)] = 0
tinta_m[348:1010, 195:845] = 0; tinta_m[1338:1482, 278:778] = 0; tinta_m[(m_arco > 0)] = 0
tinta_m = cv2.dilate(tinta_m, np.ones((5, 5), np.uint8))
suave = lambda m: cv2.GaussianBlur(m, (0, 0), 1.5)
camadas = np.dstack([suave(baloes), suave(presente), suave(tinta_m)])
Image.fromarray(camadas).save(AQUI / "camadas.png", optimize=True)
print("camadas OK")
