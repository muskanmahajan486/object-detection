//Ball.h
#pragma once
 
#include "Color.h"
#include <opencv2/core/types.hpp>
 
class Ball
{
public:
    Color color;
    cv::Point position;
    cv::Rect rect;
 
    Ball();
    Ball(Color color, cv::Rect rect, int x, int y);
 
};
 
//Ball.cpp
#include "Ball.h"
 
Ball::Ball(){
}
 
Ball::Ball(Color color, cv::Rect rect, int x, int y){
    this->color = color;
    this->rect = rect;
    this->position = cv::Point(x, y);
}