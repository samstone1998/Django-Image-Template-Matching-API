from email import utils
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

import cv2
import numpy
import re
import logging

db_logger = logging.getLogger('db')

db_logger.info('info message')
db_logger.warning('warning message')

class template_check(APIView):
    def post(self, request):
        """ Takes a base image and a template image and tests if the template image can
            be found inside the base image.

        Returns:
            Json response with a bool value depending if the template was matched or not
        """
        # Used just for logging any strange or unexpected errors.
        # All errors like not providing correct post data or threshold values should already be handled.
        try:
            base_image_data = request.FILES.get('base', False)
            template_image_data = request.FILES.get('template', False)
            threshold = request.data.get('threshold', False)
            
            if not base_image_data:
                return Response({'error': 'A base image must be provided'})
            elif not template_image_data:
                return Response({'error': 'A template image must be provided'})
            
            
            base_image = cv2.imdecode(numpy.fromstring(base_image_data.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
            template_image = cv2.imdecode(numpy.fromstring(template_image_data.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
                
            # Sets default threshold to 0.8 in case one was not set
            if not threshold:
                threshold = 0.8
                
            # Regex to check if threshold is a number or decimal
            elif not re.search('^[+-]?((\\d+(\\.\\d*)?)|(\\.\\d+))$', threshold):
                return Response({'error':'threshold must be a number'})
            else:
                threshold = float(threshold)
                                
            base_gray = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(base_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            loc = numpy.where( res >= threshold)
            matched = [i for i in zip(*loc[::-1]) if i != None]
                    
            return Response({'found': True if matched else False,})
        
        # Prefer not to use 'exception' as its very generic but
        # for this is a backup in case something unpredicted fails.
        except Exception as e:
            db_logger.exception(e)
            return Response({'error': 'An error has occured. If this continues please contact support'})
        
        
