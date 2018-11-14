﻿# UFJF - Ischemic PreCondition
 
 Python routines developed in order to process research data series producing reports and graphs.
 
 Effect of Ischemic Preconditioning on Local Oxigenation of Lower Limbs
 Ribeiro, G.G.S., Bresser, M., Deotti, A., Marocolo, M.
 Physiology and Human Performance Research Group - UFJF

Data series are comma separated text files. 
Each line should contain a time record with participants analyzed variable values separated by commas. 

For example, a record with 8 participants looks like:
12.55, 12.38, 12.41, 11.82, 12.08, 12.86, 11.48, 12.4

It is possible to configure:
Filename:       name of the file to be processed.
Sampling rate:  # of records per minute.
Initial time:   The of obtained data before the first intervention in minutes
Occlusion time: Intervention time in minutes.
Reperfusion time: Time between interventions in minutes.
Number of occlusions: integer (i.e. 4)


 @author: Antonio Iyda Paganelli antonioiyda@gmail.com
