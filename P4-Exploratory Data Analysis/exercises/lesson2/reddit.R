reddit <- read.csv('reddit.csv')
str(reddit)
library(ggplot2)
levels(reddit$age.range)
qplot(data = reddit, x=age.range)

all <- levels(reddit$age.range)
diff <- c('Under 18')
c(diff, all[-7])
all-diff
levels(reddit$military.service)
levels(reddit$children)
levels(reddit$cheese)

levels(reddit$income.range)
qplot(data=reddit, x=income.range)

#using factor
reddit$age.range <- factor(reddit$age.range, levels=c('Under 18', levels(reddit$age.range)[-7]))
str(reddit) # can pass optional argument ordered = T, same as using ordered
levels(reddit$age.range)
is.factor(reddit$age.range)
qplot(data = reddit, x=age.range)
reddit$age.range

#using order
reddit$age.range <- ordered(reddit$age.range, levels=c(levels(reddit$age.range)))
is.factor(reddit$age.range)
levels(reddit$age.range)


