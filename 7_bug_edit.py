## 7. 공이 무기를 연속으로 맞으면 공이 안사라지는 버그발생
## for문 안에 for가 있기 때문에 발생
import pygame
import os
pygame.init() # 기본 초기화
clock = pygame.time.Clock() # FPS 설정
screen_width = 640 #화면 크기
screen_height = 480 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Nado Pang") 

# 1. 사용자 게임 초기화 (배경, 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)    # 현재 파일의 위치를 반환
image_path = os.path.join(current_path, "images")   # 현재 파일위치에서 images 폴더 경로 추가

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size  # size를 튜플형식으로 저장
stage_height = stage_size[1]    # 스테이지 높이 위에 캐릭터

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
charactor_size = character.get_rect().size
character_wight = charactor_size[0]
character_height = charactor_size[1]
character_x_pos = (screen_width/2) - (character_wight/2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 방향 및 속도
character_to_x = 0
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 연사 가능 -> list 활용
weapons = []
weapon_speed = 10

# 공 만들기(4개의 유형)
ball_images = [
    pygame.image.load(os.path.join(image_path, "ballon1.png")),
    pygame.image.load(os.path.join(image_path, "ballon2.png")),
    pygame.image.load(os.path.join(image_path, "ballon3.png")),
    pygame.image.load(os.path.join(image_path, "ballon4.png"))]

# 작아지면 낮게 뛰어 오름
ball_speed_y = [-18, -15, -12, -9]  # list index 0 1 2 3 에 해당

# 공 정보가 많으므로 dic활용
balls = []

balls.append({
    "pos_x" : 50,   # 공의 좌표
    "pos_y" : 50,
    "img_idx" : 0,   # 공 이미지의 index
    "to_x" : 3,     # 공의 x축 이동
    "to_y" : -6,    # 공의 y축 이동
    "init_spd_y" : ball_speed_y[0]})  # y최초속도 정의

# 사라질 무기, 공 정보 저장
weapon_to_remove = -1
ball_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100 # 시간
start_ticks = pygame.time.get_ticks()

# 게임 종료 메시지 / Time Out, Mission complete, Game Over
game_result = "Game over" # 이건 기본값, 후에 timeout 시 새로 대입해주면 됨


running = True 
while running: 
    dt = clock.tick(30) 

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:   
            running = False       

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                # 무기 발사, 캐릭터 머리에서 발사되며 누를 때 마다 위치를 weapons에 추가
                weapon_x_pos = character_x_pos + character_wight/2 - weapon_width/2 
                weapon_y_pos = character_y_pos
                weapons.append([character_x_pos, character_y_pos])

        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0 :
        character_x_pos =0
    elif character_x_pos > screen_width - character_wight:
        character_x_pos = screen_width - character_wight

    # 무기의 움직임. weapons list를 w[0], w[1]로 가져오고, y가 이동하도록 새롭게 정의
    weapons = [ [w[0] , w[1] - weapon_speed] for w in weapons]

    # 천장에 닿은 무기 없애기, y가 0보다 클때만 존재.
    weapons = [ [w[0],w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    # enumerate : ball dic에 있는 것들을 하나씩 가지고 와서 순서와 벨류 출력.
    for ball_idx, ball_val in enumerate(balls):    
        ball_pos_x = ball_val['pos_x']  # pos_x index의 value를 가지고 옴. 60줄.
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']
            # ball_images list에 index를 넣어 사이즈 가지고 옴.48줄 1~3번 공은 나중에
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_widht = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿았을 때 반사
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_widht:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 스테이지에 튕귐
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]

        # 올라갈 수록 감속
        else:
            ball_val["to_y"] += 0.5     #y의 이동속도는 계속 0.5씩 증가
        ball_val["pos_x"] += ball_val["to_x"]   # x의 이동속도 만큼 위치 변경
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 충돌 처리 
        # 캐릭터 크기 정의
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

        # 공 크기 정의
    for ball_idx, ball_val in enumerate(balls):    
        ball_pos_x = ball_val['pos_x']  
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 캐릭터와 곂치면 종료 
        if character_rect.colliderect(ball_rect):
            print("충돌하였습니다.")
            running = False
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):    
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]
            
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y
            
            # 충돌 처리, 공도 사라지고 무기도 사라짐
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx   
                
                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 넘어감
                if ball_img_idx < 3: 
                    # 현재 공 크기 정보 가지고오기
                    ball_wight = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보. 현재 공 보다 idx + 1인 공 사진 정보 가지고옴.
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    #왼쪽으로 튀는 공
                    balls.append({
                        "pos_x" : ball_pos_x + ball_widht/2 - small_ball_width/2,   # 이전 공 위치 기준
                        "pos_y" : ball_pos_y + ball_height/2 - small_ball_height/2,
                        "img_idx" : ball_img_idx + 1,   
                        "to_x" : -3,     
                        "to_y" : -6,   
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]}) 
                    
                    #오른쪽으로 튀는 공
                    balls.append({
                        "pos_x" : ball_pos_x + ball_widht/2 + small_ball_width/2,
                        "pos_y" : ball_pos_y + ball_height/2 - small_ball_height/2,
                        "img_idx" : ball_img_idx + 1,    
                        "to_x" : 3,     
                        "to_y" : -6,   
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]})  
                break
        else :
            continue    
        break       #버그 수정.
    
    # 충돌된 공 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공 없애면 게임 종료
    # balls 의 길이가 0이면
    if len(balls) == 0: 
        game_result = "Mission Complete"
        running = False

    # 5. 화면에 그리기. 덮어쓰기 순서 이므로 중요
    screen.blit(background, (0,0))

    # list 에 있는 모든 weapon 에게 적용, 무기가 캐릭터와 스테이지 밑에 있어야함.
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0,screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간 초과시
    if total_time - elapsed_time <= 0 :
        game_result = "Time Over"
        running = False

    # 6. 반드시 필요
    pygame.display.update()

# 게임 오버 메세지
msg = game_font.render(game_result, True, (255,255,0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg,msg_rect)
pygame.display.update()

pygame.time.delay(2000) # 2초 대기후 종료

pygame.quit()
