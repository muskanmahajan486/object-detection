//main.cpp
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
 
#include "Ball.h"
 
cv::Scalar yellowLow = cv::Scalar(25, 130, 180);
cv::Scalar yellowHigh = cv::Scalar(45, 255, 255);
cv::Scalar greenLow = cv::Scalar(46, 40, 40);
cv::Scalar greenHigh = cv::Scalar(70, 255, 255);
cv::Scalar blueLow = cv::Scalar(100, 150, 150);
cv::Scalar blueHigh = cv::Scalar(140, 255, 255);
cv::Scalar purpleLow = cv::Scalar(148, 117, 89);
cv::Scalar purpleHigh = cv::Scalar(152, 255, 255);
cv::Scalar redLow = cv::Scalar(170, 140, 160);
cv::Scalar redHigh = cv::Scalar(180, 255, 255);
 
std::vector<Ball> balls;
 
void GetBalls(cv::Mat img, cv::Scalar low, cv::Scalar high, Color color) {
   cv::Mat mask;
   cv::inRange(img, low, high, mask);
   std::vector<std::vector<cv::Point> > contours;
   cv::findContours(mask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

   for (size_t i = 0; i < contours.size(); i++)
   {
      cv::Rect boundRect = boundingRect(contours[i]);
      if (boundRect.area() > 350 && (boundRect.width < 100 || boundRect.height < 100)) {
         balls.emplace_back(color, boundRect, boundRect.x + boundRect.width / 2, boundRect.y + boundRect.height / 2);
      }
   }
}
 
void drawBalls(cv::Mat background) {
   for (size_t i = 0; i < balls.size(); i++) {
      switch (balls[i].color) {
      case RED:
         rectangle(background, balls[i].rect.tl(), balls[i].rect.br(), CV_RGB(255, 0, 0), 2);
         break;
      case BLUE:
         rectangle(background, balls[i].rect.tl(), balls[i].rect.br(), CV_RGB(0, 0, 255), 2);
         break;
      case GREEN:
         rectangle(background, balls[i].rect.tl(), balls[i].rect.br(), CV_RGB(0, 255, 0), 2);
         break;
      case YELLOW:
         rectangle(background, balls[i].rect.tl(), balls[i].rect.br(), CV_RGB(255, 255, 0), 2);
         break;
      case PURPLE:
         rectangle(background, balls[i].rect.tl(), balls[i].rect.br(), CV_RGB(128, 0, 128), 2);
         break;
      }
   }
}
 
 
int main(){
   cv::Mat target = cv::imread("bal.jpg"); //cv::IMREAD_COLOR

   cv::Mat background;
   target.copyTo(background);

   cv::cvtColor(target, target, cv::COLOR_BGR2HSV);
//  make not draw
   cv::rectangle(target, cv::Point(0, 0), cv::Point(640, 30), (0, 0, 0), cv::FILLED);

   GetBalls(target, yellowLow, yellowHigh, Color::YELLOW); //find yellow balls
   GetBalls(target, blueLow, blueHigh, Color::BLUE); //find blue balls
   GetBalls(target, redLow, redHigh, Color::RED); //find red balls
   GetBalls(target, greenLow, greenHigh, Color::GREEN); //find green balls
   GetBalls(target, purpleLow, purpleHigh, Color::PURPLE); // find purple balls
   drawBalls(background);

   cv::imshow("contours", background);
   cv::waitKey(0);
}