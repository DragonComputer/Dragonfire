#include </usr/include/opencv2/opencv.hpp>
#include </usr/include/opencv2/highgui/highgui_c.h>
#include <stdio.h>
    
int main()
{ 


	CvCapture *capture;
	IplImage *frame;
	IplImage *frame1 = cvCreateImage(cvSize(640,480),IPL_DEPTH_8U,1);

	capture = cvCaptureFromCAM(0) ; 


	while(1){

		int histogram[256];
		      
		for(int i = 0; i < 256; i++){
		      	histogram[i] = 0;
		}
		
		frame = cvQueryFrame(capture);
		cvCvtColor(frame,frame1,CV_BGR2GRAY); 
		      
		for(int i = 0; i < frame1->height; i++) {
			for(int j = 0; j < frame1->width; j++){

				histogram[(int)frame1->imageData[j]]++;
			}
		}
       
		int max = histogram[0];
		int j = 0;
	
		for(int i = 0; i < 256; i++){

			if(histogram[i] > max){
				max = histogram[i];
				j = i;
			}
		}
		
		if(j <= 15){
			system("xbacklight -set 20");
		}
		else if(j <= 40){
			 system("xbacklight -set 50");
		}
		else if(j <= 75){
			 system("xbacklight -set 80");
		}
 
	}

	cvReleaseCapture(&capture);
}



