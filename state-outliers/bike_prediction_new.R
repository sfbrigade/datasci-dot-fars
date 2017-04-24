#Author: Kevin Vo
#This R script implements an interrupted time series
#approach to determine if there is a significant change
#in the number of bike deaths per capita in the year
#2015.

rm(list = ls())

Preprocess <- function(){
	setwd("/Users/kevinavo/Documents/datasci-dot-fars-master")
	library(plm)
	library(data.table)
	library(DataCombine)
	library(plyr)
	library(stargazer)
}

MakeData <- function(){
	#Read in and clean the data
	df = read.csv('new_data.csv')
	names(df) = tolower(names(df))
	df = rename(df, c("vmt..b." = 'vmt_b', 'total.deaths' = 'total_deaths', 
					  'deaths.per.bvmt' = 'deaths_bvmt', 'deaths.involving.drivers.under.16' = 'deaths_16', 
					  'deaths.involving.drivers.under.16.per.bvmt' = 'deaths_16_bvmt', 
					  'deaths.involving.drivers.between.25...44' = 'deaths_25_44', 
					  'deaths.involving.drivers.between.25...44.per.bvmt' = 'deaths_25_44_bvmt', 
					  'multi.vehicle.deaths'= 'mult_vehicle_deaths', 
					  'multi.vehicle.deaths.per.bvmt' = 'multi_vehicle_deaths_per_bvmt', 
					  'bicyclist.deaths' = 'bike_deaths', 'bicyclist.deaths.per.bvmt' = 'bike_deaths_bvmt'))
	
	# #Generate an indicator variable for pre and post year 2015
	df['post'] = as.numeric((df['year'] == 2015))
	df['year'] = df['year'] - 2009	
	return (df)
}

##########Main Scripting##########
Preprocess()
df = MakeData()
listOfFits = list()
depVars = c('deaths_bvmt', 'deaths_16_bvmt', 'deaths_25_44_bvmt', 'multi_vehicle_deaths_per_bvmt', 'bike_deaths_bvmt')
for (depVar in depVars){
	regModel = paste(depVar, '~', 'year + post + state', sep = '')
	print (regModel)
	regModel = as.formula(regModel)
	lm_fit = lm(regModel, data = df)
	summary(lm_fit)
	listOfFits[[depVar]] = lm_fit
	# postCoef = test_fit$coefficients['post']
	# pval = summary(test_fit)$coefficients['post', 'Pr(>|t|)']
}
# summary(test_fit)

#total deaths per mile
#