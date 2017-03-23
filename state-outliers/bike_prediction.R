#Author: Kevin Vo
#This R script implements an interrupted time series
#approach to determine if there is a significant change
#in the number of bike deaths per capita in the year
#2015.

rm(list = ls())

Preprocess <- function(){
	
	library(plm)
	library(data.table)
	library(DataCombine)
	library(plyr)
}

MakeData <- function(){
	#Read in and clean the data
	df = read.csv('data.csv')
	names(df) = tolower(names(df))
	df = rename(df, c("bicycle.commuters" = 'bicycle_commuters', 'no..deaths' = 'bike_deaths', 'deaths.per.b.miles' = 'bike_deaths_pc'))
	
	# #Generate an indicator variable for pre and post year 2015
	df['post'] = as.numeric((df['year'] == 2015))
	df['year'] = df['year'] - 2010
	
	return (df)
}

##########Main Scripting##########
Preprocess()
df = MakeData()
test_fit = lm(bike_deaths_pc ~ year + post + state, data = df)
summary(test_fit)

#total deaths per mile
#