import com.leapmotion.leap.*;
import java.util.ArrayList;
import ddf.minim.*;
Minim minim;//新增minim變數

// Leap Motion 控制器物件
com.leapmotion.leap.Controller leapController;

// 遊戲元素
PVector paddle;
float paddleWidth = 100;
float paddleHeight = 20;
PVector ball;
PVector ballSpeed;
PImage img;

// 磚塊
ArrayList<Brick> bricks;

// 遊戲狀態
boolean gameActive = true;
int countdown = 3;
int lastTime;
boolean countdownStarted = true;
int point = 0;

void setup() {
  size(800, 600);
  AudioPlayer player;//新增音樂變數
  minim = new Minim(this);
  player = minim.loadFile("bgmusic.mp3");
  player.play();
  
  // 初始化Leap Motion控制器
  leapController = new com.leapmotion.leap.Controller();
  
  // 初始化遊戲元素
  paddle = new PVector(width / 2 - paddleWidth / 2, height - 50);
  ball = new PVector(int(random(10, width - 10)), height / 2);
  ballSpeed = new PVector();
  
  // 初始化磚塊
  bricks = new ArrayList<Brick>();
  int rows = 5;
  int cols = 10;
  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      bricks.add(new Brick(j * 80 + 20, i * 30 + 50, 60, 20));
    }
  }
}

void draw() {
  if (point == 50) {
    gameActive = false;
  }
  background(255);
  img = loadImage("bg.jpg");
  image(img, 0, 0, 800, 600);
  if (gameActive) {
    if (countdownStarted) {
      int currentTime = millis();
      if (currentTime - lastTime >= 1000) {
        countdown--;
        lastTime = currentTime;
      }
      if (countdown > 0) {
        fill(255, 0, 0);
        textSize(64);
        textAlign(CENTER, CENTER);
        text(countdown, width / 2, height / 2);
      }
      else {
        countdownStarted = false;
        ballSpeed = new PVector(-5, 5);
      }
    }
    Frame frame = leapController.frame();
    for (Hand hand : frame.hands()) {
      // 根據手的位置更新板子的位置
      PVector handPos = leapToScreen(hand.palmPosition());
      paddle.x = handPos.x - paddleWidth / 2;
    }
    
    // 移動板子，確保不超出螢幕邊界
    paddle.x = constrain(paddle.x, 0, width - paddleWidth);
    
    // 繪製板子
    fill(int(random(255)), int(random(255)), int(random(255)));
    rect(paddle.x, paddle.y, paddleWidth, paddleHeight);
    
    // 更新球的位置
    ball.add(ballSpeed);
    
    // 如果球觸碰到螢幕邊界，改變方向
    if (ball.x < 10 || ball.x + 10 > width) {
      ballSpeed.x *= -1;
    }
    if (ball.y < 10) {
      ballSpeed.y *= -1;
    }
    // 如果球觸碰到板子，改變方向
    if (ball.x >= paddle.x && ball.x <= paddle.x + paddleWidth && ball.y + 10 == paddle.y) {
      ballSpeed.y *= -1;
    }
    
    // 檢查球是否與磚塊相撞
    for (Brick brick : bricks) {
      if (brick.visible && ball.x >= brick.x && ball.x <= brick.x + brick.width
          && ball.y >= brick.y + 5 && ball.y <= brick.y + brick.height + 10) {
        brick.visible = false;
        point += 1;
        ballSpeed.y *= -1;
        AudioPlayer player1;//新增音樂變數
        minim = new Minim(this);
        player1 = minim.loadFile("music.mp3");
        player1.play();
      }
    }
    
    // 檢查球是否超過畫面底部，結束遊戲
    if (ball.y + 10 > height) {
      gameActive = false;
    }
    
    // 繪製球
    fill(int(random(255)), int(random(255)), int(random(255)));
    ellipse(ball.x, ball.y, 20, 20);
    
    // 繪製磚塊
    for (Brick brick : bricks) {
      if (brick.visible) {
        fill(175, 80, 80);
        rect(brick.x, brick.y, brick.width, brick.height);
      }
    }
  }
  else {
    // 遊戲結束的畫面
    if (point == 50) {
      img = loadImage("win.jpg");
      image(img, 0, 0, 800, 600);
    }
    else{
      img = loadImage("lose.png");
      image(img, 0, 0, 800, 600);
      fill(0);
      textSize(32);
      textAlign(CENTER, CENTER);
      text("Game Over", width / 2, height / 2);
      fill(255, 0, 0);
      text("score : " + point, width / 2, height / 2 + 30);
    }
  }
}

// 將Leap Motion座標轉換為螢幕座標
PVector leapToScreen(Vector leapVector) {
  PVector screenPosition = new PVector();
  screenPosition.x = map(leapVector.getX(), -200, 200, 0, width);
  screenPosition.y = map(leapVector.getY(), 100, 500, height, 0);
  return screenPosition;
}

// 磚塊類別
class Brick {
  float x, y, width, height;
  boolean visible = true;
  
  Brick(float x, float y, float w, float h) {
    this.x = x;
    this.y = y;
    this.width = w;
    this.height = h;
  }
}

void startCountdown() {
  countdownStarted = true;
  lastTime = millis();
}