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
}

MakeData <- function(){
	#Read in and clean the data
	df = read.csv('bike.csv')
	df['X'] = NULL
	names(df) = tolower(names(df))
	df = df[df$state_abbv != "DC",]
	df = rename(df, c("bicycle.commuters" = 'bicycle_commuters'))

	#Generate the lead variable for bike deaths
	df = slide(df, Var = "bike_deaths", GroupVar = "state", slideBy = 1)
	
	#Let's make the per capita variables
	qVars = c('bike_deaths', 'vmt','commuters', 'bicycle_commuters')
	newVars = paste(qVars, "pc", sep = "_")
	df['pc_driving'] = df['vmt']/df['population']
	df[newVars] = df[qVars]/df[, 'pc_driving']

	#Generate an indicator variable for pre and post year 2015
	df['post'] = as.numeric((df['year'] == 2015))
	df['year'] = df['year'] - 2010
	
	return (df)
}

##########Main Scripting##########
Preprocess()
df = MakeData()
test_fit = lm(bike_deaths_pc ~ year + post + state, data = df)
summary(test_fit)