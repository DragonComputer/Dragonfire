#include "/usr/include/opencv2/opencv.hpp"
#include "/usr/include/opencv2/highgui/highgui_c.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <math.h>
#include <float.h>
#include <limits.h>
#include <time.h>
#include <ctype.h>


int flag = 0;
int f = 0;
int played = 0;
static CvMemStorage* storage = 0;
static CvHaarClassifierCascade* cascade = 0;

int detect_and_draw( IplImage* image )
{

	int scale = 1;	
	CvPoint pt1, pt2;

	int i;
	
	cvClearMemStorage( storage );

	if( cascade ){
		CvSeq* faces = cvHaarDetectObjects( img, cascade, storage,
		                                     1.1, 2, CV_HAAR_DO_CANNY_PRUNING,
		                                     cvSize(40, 40) );
		       
		if(!faces || faces->total == 0){
			return 0;
		}	
		
		for( i = 0; i < (faces ? faces->total : 0); i++ ){
			CvRect* r = (CvRect*)cvGetSeqElem( faces, i );
			
			pt1.x = (r->x) * scale;
			pt2.x = (r->x+r->width) * scale;
			pt1.y = (r->y) * scale;
			pt2.y = (r->y+r->height) * scale;
			
			cvRectangle( img, pt1, pt2, CV_RGB(255,0,0), 3, 8, 0 );
		}

	}
	
	return 1;
}



int main( int argc, char** argv )
{

	CvCapture* capture = 0;
	IplImage *frame, *frame_copy = 0;
	cascade = (CvHaarClassifierCascade*) cvLoad( "yolo.xml", 0, 0, 0 );
  
	if( !cascade ){
		printf("ERROR: Could not load classifier cascade\n");
		return -1;
	}
    
	storage = cvCreateMemStorage(0);
    
	capture = cvCaptureFromCAM(0);

	if( capture ){
		int j = 0;

		for(;;){

			FILE *fin;
			int i = 0;
			flag = 0,f = 0;
    
			if( !cvGrabFrame( capture )){
				break;
			}
			
			frame = cvRetrieveFrame( capture );
			
			if( !frame ){
				break;
			}
			        
			if( !frame_copy ){
				frame_copy = cvCreateImage( cvSize(frame->width,frame->height),
								IPL_DEPTH_8U, frame->nChannels );
			}

			system("ps -e | grep totem > sample.txt");

			fin = fopen("sample.txt","r");

			fflush(fin);

			while(!feof(fin)){
				char a[40];
				fscanf(fin,"%s\n",a);

				if(a[i]=='t'&&a[i+1]=='o'&&a[i+2]=='t'&&a[i+3]=='e'&&a[i+4]=='m'){
					f=1;
					break;
				}
				else{
					 f=0;
				}
    			}	
    	  
			fclose(fin);

			if( frame->origin == IPL_ORIGIN_TL ){
				cvCopy( frame, frame_copy, 0 );
			}
			else{
				cvFlip( frame, frame_copy, 0 );
			}
            
			flag = detect_and_draw( frame_copy );

	   		if(f==0){
				printf("no totem playing\n
					please switch off the application from the command centre\n
					or open a video file\n");
				sleep(5);
			}
			else if (flag == 0 && f == 1 && played == 1){
				system("totem --pause");
 				played=0;
    			}
			else if (flag == 1 && f == 1 && played == 0){
				system("totem --play");
				played=1;
    			}
	    

    			if( cvWaitKey( 10 ) >= 0 ){
				break;
			}
    
		}

		//cvReleaseImage( &frame_copy );
        	cvReleaseCapture( &capture );
	}

	else{
		printf("some error in capturing from cam");
	}

	return 0;
}

