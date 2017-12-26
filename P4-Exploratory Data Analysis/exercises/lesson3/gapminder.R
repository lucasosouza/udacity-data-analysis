data(diamonds) 
library(ggplot2)

#get overall structure of the data
summary(diamonds)
head(diamonds)
str(diamonds)
dim(diamonds)
levels(diamonds$cut)
levels(diamonds$color)
levels(diamonds$clarity)
?diamonds

#create histogram of the price of all diamonds
qplot(data=diamonds, x=price, geom='histogram',
      color=I('black'), fill=I('blue'))
geom_histogram(data=diamonds, x=price)
summary(diamonds$price)

#Strangely, it seems there is a negative correlation between good values
#of cut, color, and clarity, and the price. Logic says it is supposed to be
#the exact opposite - a better value at one of these characteristics would 
#imply a boxplot positioned higher up in the y axis, with higher median, Q1
#and Q2 values. But surpisingly the data shows that having a better color, 
#cut or clarity will actually make the diamond cheaper

ss <- subset(diamonds, cut == 'Fair')
qplot(data=ss, geom='boxplot', y=price, x='a') + 
  coord_cartesian(ylim=c(0,8000))

#cut: quality of the cut (Fair, Good, Very Good, Premium, Ideal)
qplot(data=diamonds, geom='boxplot', y=price, x=cut, binsize=10) + 
  coord_cartesian(ylim=c(0,6000))

by(diamonds$price, diamonds$cut, min)


#color: diamond colour, from J (worst) to D (best)
qplot(data=diamonds, geom='boxplot', y=price, x=color) + 
  coord_cartesian(ylim=c(0,8000))

#clarity: I1 (worst), SI1, SI2, VS1, VS2, VVS1, VVS2, IF (best))
qplot(data=diamonds, geom='boxplot', y=price, x=clarity) + 
  coord_cartesian(ylim=c(0,8000))

IQR(diamonds$price)

#The distribution is left-skewed, with a long tail. 
#The IQR is 4374.25, but the overall difference between maximum
#and minimum is 18,494, about 4.5x the IQR. The difference between
#the median and the mean also shows the data is long tailed: 
#the median is 2,401, while the mean is 3,933.

length(subset(diamonds, diamonds$price < 500))
dim(subset(diamonds, diamonds$price >= 15000))

ggsave()

##########

qplot(data=diamonds, x=price) +
  facet_wrap(~cut, scales="free_y", ncol=1) +
  scale_x_continuous(breaks=seq(0,20000,1000))


qplot(data=diamonds, x=price/carat, binwidth=0.02) + 
  facet_wrap(~cut, scales='free_y', ncol=1) +
  scale_x_log10()

qplot(data=diamonds, geom='boxplot', y=price, x=color) + 
  coord_cartesian(ylim=c(0,8000)) +
  scale_y_continuous(breaks=seq(0,8000,200))

qplot(data=diamonds, geom='boxplot', y=price, x=color)
qplot(data=diamonds, geom='boxplot', y=price, x=clarity)

by(diamonds$price, diamonds$color, IQR)

ggsave('diamonds_cost_a_thousand_dollars.png')


###############

qplot(data=diamonds, x=carat, geom="freqpoly", binwidth=0.01) + 
  scale_x_continuous(breaks=seq(0,6,0.1))

table(diamonds$carat)


##################3

install.packages('tidyr')
install.packages('dplyr')
install.packages('devtools')
library(tidyr)
library(dplyr)
library(EDAWR)

#################

###importing and analyzing data structure
gini <- read.csv('gapminderData.csv', sep=';')
str(gini)
summary(gini)

###create an average gini and plot it as a trend

# removing na values
gini2 <- na.omit(gini)

#summarizing and reshaping, using tidyr and dplyr
giniSummary <-summarize_each(gini2, funs(mean))
giniFinal <- gather(giniSummary, 'year', 'coef', 2:50)
giniFinal <- giniFinal[,2:3]
giniFinal <- mutate(giniFinal, year = substr(year, 2, 5))
giniFinal <- mutate(giniFinal, year = as.numeric(year))

#plot
qplot(data=giniFinal, x=year, y=coef) + 
  geom_point() + 
  geom_smooth()

###check differences between countries
#fix headers
gini2 <- setNames(gini2, c('country', substr(names(gini2[2:50]), 2, 5)))

#transform
dim(gini2)
gini2  <- gather(gini2, 'year', 'coef', 2:50)
gini2 <- mutate(gini2, year = as.numeric(year))

#plot
#str(gini2)
#names(gini2)

ggplot(data=gini2, aes(x=year, y=coef)) + 
  geom_boxplot() + 
  coord_cartesian(ylim=c(0,1.5))

#####plot by country 
#first, boxplot by country

ggplot(data=gini2, aes(x=country, y=coef)) + 
  geom_boxplot() + 
  coord_cartesian(ylim=c(0,1.5))

# a curve of evolution
# that means x is still year, y is still coef, but I will use something as color to represent the country

austriaData <- subset(gini2, country=='Austria')

#sweet... by country!!
ggplot(data=gini2, aes(year,coef)) + 
  geom_smooth(aes(group=country, color=country), fill=NA)

by(gini2$coef, gini2$country, summary)
str(gini2)

#shit... I'm analysing aid given, as a % of gross national income (not gini...)

##ok, almost there
#all I need now is aid a curve for each aid given
#how the hell would I do that??

#now gather all of them and publish a nice notebook



