import pygame
import random

class Jump_game:
    def __init__(self):
        # 表示モジュールの初期化
        pygame.init()

        # ゲーム画面の幅と高さの設定
        screen_width = 800
        screen_height = 400

        # 画面の作成
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        # ウィンドウタイトル
        title = "Jumping Club"
        pygame.display.set_caption(title)

        # キャラクターの表示画像、位置設定
        self.player_image = pygame.image.load("image/player.png")
        self.X = 100 - self.player_image.get_width() / 2
        self.Y = 300 - self.player_image.get_height() / 2
        self.player_X = self.X
        self.player_Y = self.Y

        # 障害物用変数
        self.obj_image = pygame.image.load("image/object_1.png")
        self.obj_X = 800
        self.obj_Y = 270 - self.obj_image.get_height() / 2

        # 背景用変数
        self.sun_image = pygame.image.load("image/sun.png")
        self.sun_X = 700
        self.sun_Y = 0

        # キャラクター移動用変数
        self.speed = 0
        self.accelalate = 0
        self.obj_speed = -13

        # スコア
        self.score = 0

        # 当たり判定
        self.player_collision_X = self.player_X + self.player_image.get_width() / 2
        self.player_collision_Y = self.player_Y + self.player_image.get_height() / 2
        self.obj_collision_X = self.obj_X - self.obj_image.get_width() / 2
        self.obj_collision_Y = self.obj_Y + self.obj_image.get_height() / 2

        # テキストのフォント設定
        self.font_size = 30
        self.font_file = None
        self.antialias = True

    def main(self):
        # フレームレート設定用変数
        F_rate = 60
        clock = pygame.time.Clock()
        # ゲームループ
        running = True
        while running:
            clock.tick(F_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.keydown()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.keydown()
                    if event.key == pygame.K_F5:
                        # リスタート処理
                        self.player_Y = self.Y
                        self.obj_X = 800
                        self.obj_speed =  -10
                        self.sun_X = 750
                        self.score = 0

            if self.collision():
                self.gameover()
                
            else:
                self.update()
                self.draw()

            # 画面の更新
            pygame.display.flip()

        # ゲームの終了
        pygame.quit()

    def draw(self):
        # テキストのフォント設定
        font = pygame.font.Font(self.font_file, self.font_size)

        # スコア等の表示に使うテキストとプレイヤーを表示するためのimageを作成
        text_image = font.render("SCORE : " + str(self.score), self.antialias, (255, 150, 10))
        text_X = 790 - text_image.get_width()
        text_Y = 10

        # 画面の色の設定
        self.screen.fill((100, 150, 250))
        self.screen.fill((250, 230, 150), rect=(0, 170, 800, 300))

        # imageを画面に表示
        self.screen.blit(self.sun_image, (self.sun_X, self.sun_Y))
        self.screen.blit(self.player_image, (self.player_X, self.player_Y))
        self.screen.blit(text_image, (text_X, text_Y))
        self.screen.blit(self.obj_image, (self.obj_X, self.obj_Y))
        
        pygame.display.update()

    def keydown(self):
        # 連続してジャンプができないように条件指定
        if self.player_Y == self.Y:

            # ジャンプ用変数
            self.speed = -25
            self.accelalate = 1.5

    def update(self):
        # ジャンプ動作
        self.speed += self.accelalate
        self.player_Y += self.speed

        # もとの高さでジャンプ停止
        if self.player_Y >= self.Y:
            self.player_Y = self.Y
            self.speed = 0
            self.accelalate = 0

        # 障害物の移動処理
        self.obj_X += self.obj_speed
        if self.obj_X <= -self.obj_image.get_width():
            self.obj_X = 800
            # 次に出てくる障害物の速度をランダムで決める
            self.obj_speed = random.randint(-20, -8)
        
        # 背景の移動
        self.sun_X -= 0.1
        if self.sun_X <= -200:
            self.sun_X = 800

        # 1F毎にスコアを+1
        self.score += 1

    def collision(self):
        # 衝突判定
        collision_det = False

        # 自キャラと障害物の衝突範囲の変数
        player_collision_X_r = self.player_X + self.player_image.get_width()
        player_collision_X_l = self.player_X
        player_collision_Y = self.player_Y + self.player_image.get_height()

        obj_collision_X_r = self.obj_X + self.obj_image.get_width()
        obj_collision_X_l = self.obj_X
        obj_collision_Y = self.obj_Y

        # 衝突したかどうか
        if player_collision_X_r >= obj_collision_X_l and player_collision_Y >= obj_collision_Y and\
            player_collision_X_l <= obj_collision_X_r:
            collision_det = True

        return collision_det
    
    def gameover(self):
        # 衝突したらゲームオーバーなのでキャラと障害物の動きを停止
        self.speed = 0
        self.obj_speed = 0
        # ゲームオーバー用テキストの設定と表示
        self.font_size = 100
        font = pygame.font.Font(self.font_file, self.font_size)
        game_over = font.render("GAME OVER", self.antialias, pygame.Color("black"))
        game_over_X = self.screen.get_width() / 2 - game_over.get_width() / 2
        game_over_Y = self.screen.get_height() / 2 - game_over.get_height() / 2

        self.font_size = 50
        font = pygame.font.Font(self.font_file, self.font_size)
        restart_text = font.render("Restart : F5", self.antialias, pygame.Color("red"))
        restart_X = self.screen.get_width() / 2 - restart_text.get_width()
        restart_Y = self.screen.get_height() / 2 + game_over.get_height()
        
        self.screen.blit(game_over, (game_over_X, game_over_Y))
        self.screen.blit(restart_text, (restart_X, restart_Y))
        
        pygame.display.update()

if __name__ == "__main__":
    app = Jump_game()
    app.main()