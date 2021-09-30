//main.cpp
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
 

#include <opencv2/core/types.hpp>
enum Colors {BLUE, RED, GREEN, YELLOW, PURPLE, GRAY};

class Ball
{
public:
    Colors color;
    cv::Point position;
    cv::Rect rect;
 
    Ball();
    Ball(Colors color, cv::Rect rect, int x, int y){
      this->color = color;
      this->rect = rect;
      this->position = cv::Point(x, y);
    }
 
};

cv::Scalar yellowLow = cv::Scalar(25, 130, 180);
cv::Scalar yellowHigh = cv::Scalar(45, 255, 255);
cv::Scalar greenLow = cv::Scalar(46, 40, 40);
cv::Scalar greenHigh = cv::Scalar(70, 255, 255);
cv::Scalar blueLow = cv::Scalar(100, 150, 150);
cv::Scalar blueHigh = cv::Scalar(140, 255, 255);
cv::Scalar purpleLow = cv::Scalar(148, 110, 89);
cv::Scalar purpleHigh = cv::Scalar(152, 255, 255);
cv::Scalar redLow = cv::Scalar(170, 140, 160);
cv::Scalar redHigh = cv::Scalar(180, 255, 255);

cv::Scalar grayLow = cv::Scalar(0, 0, 20);
cv::Scalar grayHigh = cv::Scalar(250, 20, 200);
 
std::vector<Ball> balls;
int cnt=0;
void GetBalls(cv::Mat img, cv::Scalar low, cv::Scalar high, Colors color) {
   cv::Mat mask;
   cv::inRange(img, low, high, mask);
   std::vector<std::vector<cv::Point> > contours;
   cv::findContours(mask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

   for (size_t i = 0; i < contours.size(); i++)
   {
      cv::Rect boundRect = boundingRect(contours[i]);
      if (boundRect.area() > 350 && (boundRect.width > 100 || boundRect.height > 100)) {
         balls.emplace_back(color, boundRect, boundRect.x + boundRect.width / 2, boundRect.y + boundRect.height / 2);
         cnt ++;
      }
   }
}
 
void drawBalls(cv::Mat background) {
   // std::cout<<balls.size()<<"yyyy";
   // std::cout<<cnt;
   for (size_t i = 0; i < balls.size(); i++) {
      switch (balls[i].color) {
      case RED:
         // rectangle(background, balls[i].rect.tl(), balls[i].rect.br(), CV_RGB(255, 0, 0), 2);
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
      
      case GRAY:
         rectangle(background, balls[i].rect.tl(), balls[i].rect.br(), CV_RGB(0, 255, 0), 2);
         break;
      }
   }
}
 
 
int main(){
   cv::Mat target = cv::imread("v.png"); //cv::IMREAD_COLOR

   cv::Mat background,crop;
   target.copyTo(background);
   target.copyTo(crop);

   cv::cvtColor(target, target, cv::COLOR_BGR2HSV);
//  make not draw
   cv::rectangle(target, cv::Point(0, 0), cv::Point(640, 30), (0, 0, 0), cv::FILLED);
   // cv::imshow("target", target);

   /*
   * Get contour
   */

   // GetBalls(target, yellowLow, yellowHigh, Colors::YELLOW); //find yellow balls
   // GetBalls(target, blueLow, blueHigh, Colors::BLUE); //find blue balls
   GetBalls(target, redLow, redHigh, Colors::RED); //find red balls
   // GetBalls(target, greenLow, greenHigh, Colors::GREEN); //find green balls
   // GetBalls(target, purpleLow, purpleHigh, Colors::PURPLE); // find purple balls

   drawBalls(background);

   cv::Rect roi;
   roi.x = balls[0].rect.tl().x;
   roi.y = balls[0].rect.tl().y;
   roi.width = balls[0].rect.br().x-balls[0].rect.tl().x;
   roi.height =  balls[0].rect.br().y-balls[0].rect.tl().y;

  /*
  * Top Left
  */
   std::cout<<balls[0].rect.tl().x<<std::endl;
   std::cout<<balls[0].rect.tl().y<<std::endl;

   /*
   * buttom right
   */
   std::cout<<balls[0].rect.br().x<<std::endl;
   std::cout<<balls[0].rect.br().y<<std::endl;

   cv::Mat cropped_image = crop(roi);
   // cropped_image.copyTo(crop);
   cv::imshow("cropped_image", cropped_image);

   cv::cvtColor(cropped_image, cropped_image, cv::COLOR_BGR2HSV);
   GetBalls(cropped_image, grayLow, grayHigh, Colors::GRAY);
   drawBalls(cropped_image);

   cv::imshow("contours", background);
   cv::imshow("crop", crop);
   cv::waitKey(0);
}