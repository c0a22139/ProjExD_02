import random
import sys
import pygame as pg

WIDTH, HEIGHT = 1600, 900

delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

def check_bound(obj_rct: pg.Rect):
    """
    引数:こうかとんRectか、ばくだんRect
    戻り値:横方向・縦方向の真理値タプル（True:画面内/False:画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    go = False
    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img_r = pg.transform.flip(kk_img, True, False) #反転こうかとん
    kk_img_go = pg.image.load("ex02/fig/8.png")
    kk_img_go = pg.transform.rotozoom(kk_img_go, 0, 2.5)
    tmr_go = 0
    """こうかとん・各方向"""
    kk_delta = {
        pg.transform.rotozoom(kk_img_r, 60, 2.0): [0, -5],
        pg.transform.rotozoom(kk_img_r, 30, 2.0): [5, -5],
        pg.transform.rotozoom(kk_img_r, 0, 2.0): [5, 0],
        pg.transform.rotozoom(kk_img_r, 330, 2.0): [5, 5],
        pg.transform.rotozoom(kk_img_r, 300, 2.0): [0, 5],
        pg.transform.rotozoom(kk_img, 30, 2.0): [-5, 5],
        pg.transform.rotozoom(kk_img, 0, 2.0): [-5, 0],
        pg.transform.rotozoom(kk_img, 330, 2.0): [-5, -5]
    }
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_t = kk_img #初期こうかとん、直前の入力に対応したこうかとんの保持
    
    kk_rct = kk_img.get_rect()
    kk_rct.center = [900, 400]
    """爆弾"""
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))#1:黒い余白を透明にする
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect() #1:SurfaceからRectを抽出
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y)
    vx, vy = +5, +5
    accs = [a for a in range(1, 11)] #加速
    avx, avy = vx, vy #加速初期値

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct): #5:こうかとんと爆弾がぶつかったらreturn、colliderect()はぶつかったらTrue
            #print("GameOver")
            go = True

        screen.blit(bg_img,[0,0])

        """こうかとん"""
        if not go:
            key_lst = pg.key.get_pressed()
            sum_mv = [0, 0]
            for key, mv in delta.items():
                if key_lst[key]:
                    sum_mv[0] += mv[0]
                    sum_mv[1] += mv[1] 
            kk_rct.move_ip(sum_mv[0], sum_mv[1])
            if check_bound(kk_rct) != (True, True): #4:こうかとんが壁にぶつかったときの処理
                kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
            for kk in kk_delta.items(): #各こうかとんのsum_mvと比較
                if sum_mv == kk[1]:
                    screen.blit(kk[0], kk_rct)
                    kk_t = kk[0]
            if sum_mv == [0, 0]:
                screen.blit(kk_t, kk_rct) #入力されていない時

        """爆弾"""
        bd_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bd_rct)
        if not yoko: #4:横方向にはみ出た場合（False）
            vx *= -1
        if not tate: #4:縦方向にはみ出た場合（False）
            vy *= -1
        screen.blit(bd_img, bd_rct)

        """その他"""
        pg.display.update()
        tmr += 1
        avx, avy = vx*accs[min(tmr//500,9)], vy*accs[min(tmr//500,9)] #加速
        
        clock.tick(50)
        if go:
            kk_t = kk_img_go
            screen.blit(kk_img_go, kk_rct)
            #kk_t = kk_img_go
            tmr_go += 1
            vx, vy = 0, 0
        if tmr_go >= 250:
            print("GameOver")
            return




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()