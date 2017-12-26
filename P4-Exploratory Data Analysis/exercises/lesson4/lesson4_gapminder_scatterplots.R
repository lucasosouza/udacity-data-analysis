#clear all variables
rm(list=ls())

#load libraries
library(ggplot2)
library(dplyr)
library(tidyr)

#load data for poorest, and richest, combine. 

#load data for poorest. count the year with more occurrences
df.poorest <- read.csv("Indicator_Income share held by lowest 10%.csv", sep=";")
str(df.poorest)
summary(df.poorest)
names(df.poorest)
df.poorest %>% summarise_each(funs(n_distinct))

#based on it, the year of 2005 has been chosen for analysis
#isolate it, and remove nas.
names(df.poorest)[1] <- "Country"
df.poorest.2005 <- subset(df.poorest, !is.na(X2005), select=c(Country, X2005))

#load data for richest
df.richest <- read.csv("Indicator_Income share held by highest 10%.csv", sep=";")
summary(df.richest)
names(df.richest)[1] <- "Country"
df.richest.2005 <- subset(df.richest, !is.na(X2005), select=c(Country, X2005))

#combine both, and make inequality index
df.inequality <- merge(df.poorest.2005, df.richest.2005, by=c("Country"))
names(df.inequality)[2:3] <- c('poorest', 'richest')
df.inequality$inequality <- df.inequality$richest / df.inequality$poorest 

#gather data on population
#gather data on life expectancy, murder, suicide, and working hours per week
df.suicide <- read.csv("suicide.csv", sep=";")
df.homicide <- read.csv("homicide.csv", sep=";")
df.working_hours <- read.csv("working_hours.csv", sep=";")
df.life_expectancy <- read.csv("life_expectancy.csv", sep=";")
df.population <- read.csv("population.csv", sep=";")

#change names
names(df.suicide)[1] = "Country"
names(df.homicide)[1] = "Country"
names(df.working_hours)[1] = "Country"
names(df.life_expectancy)[1] = "Country"
names(df.population)[1] = "Country"

#merge
df.data <- merge(df.inequality, df.suicide, by=c("Country"))
names(df.data)[5] = "Suicide"
df.data <- merge(df.data, df.homicide, by=c("Country"))
names(df.data)[6] = "Homicide"
df.data <- merge(df.data, df.life_expectancy, by=c("Country"))
names(df.data)[7] = "Life_Expectancy"
df.data <- merge(df.data, df.population, by=c("Country"))
names(df.data)[8] = "Population"

df.data <- df.data[,1:8]

#working hours removed - not reliable data

#Plotter scatterplots
#Look if inequality, amongst underdeveloped countries, is able to explain 
#life expectancy at birth, murder per 100,000 and suicide per 100,000

p1 <- ggplot(data=df.data, aes(x=inequality, y=Life_Expectancy)) +
  geom_point() + geom_smooth(method="lm", se=FALSE)
p2 <- ggplot(data=df.data, aes(x=inequality, y=Homicide, colour=Country)) +
  geom_point() + geom_smooth(method="lm", se=FALSE)
p3 <- ggplot(data=df.data, aes(x=inequality, y=Suicide)) +
  geom_point() + geom_smooth(method="lm", se=FALSE)
grid.arrange(p1,p2,p3,ncol=1)

ggplot(data=df.data, aes(x=inequality, y=Homicide, colour=Country, size=Population)) +
  geom_point() + 
  scale_size_continuous(range = c(3,20))

+ geom_smooth(method="lm", se=FALSE)

with(df.data, cor.test(inequality, Homicide))
with(df.data, cor.test(inequality, Suicide))
with(df.data, cor.test(inequality, Life_Expectancy))

write.csv(df.data, "data.csv")
