

data(diamonds)
rm(list=ls())
names(diamonds)
?diamonds
library(gridExtra)

p1 <- ggplot(data=diamonds, aes(x=price, y=x)) + geom_point()
p2 <- ggplot(data=diamonds, aes(x=price, y=y)) + geom_point()
p3 <- ggplot(data=diamonds, aes(x=price, y=z)) + geom_point()
p4 <- ggplot(data=diamonds, aes(x=price, y=carat)) + geom_point()
p5 <- ggplot(data=diamonds, aes(x=price, y=clarity)) + geom_point()
p6 <- ggplot(data=diamonds, aes(x=price, y=cut)) + geom_point()
p7 <- ggplot(data=diamonds, aes(x=price, y=color)) + geom_point()
p8 <- ggplot(data=diamonds, aes(x=price, y=depth)) + geom_point()
grid.arrange(p1,p2,p3,p4,p5,p6,p7,p8,ncol=3,nrow=3)

with(diamonds, cor.test(x=price, y=x))
with(diamonds, cor.test(x=price, y=y))
with(diamonds, cor.test(x=price, y=z))

ggplot(data = diamonds, aes(x = depth, y = price)) + 
  geom_point(alpha=1/10) + 
  scale_x_continuous(breaks=seq(min(diamonds$depth),max(diamonds$depth),2))

with(diamonds, cor.test(x=depth, y=price))

ggplot(data=subset(diamonds, price < quantile(price, 0.99) & carat < quantile(price, 0.99)), 
       aes(x=carat, y=price)) + 
  geom_point()

ggplot(data=diamonds, aes(x=price, y=carat)) + 
  geom_point()

data(diamonds)
diamonds$volume <- diamonds$x * diamonds$y * diamonds$z
ggplot(data=subset(diamonds, volume > 0 & volume < 800), aes(y=price, x=volume)) + 
  geom_point(alpha=1/10) +
  geom_smooth(method='lm')

?geom_smooth

with(subset(diamonds, volume > 0 & volume < 800), cor.test(y=price, x=volume))
count(diamonds$volume == 0)
detach("package:plyr", unload=TRUE)
library(dplyr)

diamondsByClarity <- diamonds %>%
    group_by(clarity) %>%
    summarize(mean_price = mean(price), 
              median_price= median(price),
              min_price = min(price),
              max_price = max(price),
              n=n())
?diamonds
names(diamonds)
with(diamonds, cor.test(x=price, y=clarity))



diamonds_by_clarity <- group_by(diamonds, clarity)
diamonds_mp_by_clarity <- summarise(diamonds_by_clarity, mean_price = mean(price))

diamonds_by_color <- group_by(diamonds, color)
diamonds_mp_by_color <- summarise(diamonds_by_color, mean_price = mean(price))

diamonds_by_cut <- group_by(diamonds, cut)
diamonds_mp_by_cut <- summarise(diamonds_by_cut, mean_price = mean(price))

bar1 <- ggplot(data=diamonds_mp_by_clarity, aes(x=clarity, y=mean_price)) + 
  geom_bar(stat='identity')

bar2 <- ggplot(data=diamonds_mp_by_color, aes(x=color, y=mean_price)) + 
  geom_bar(stat='identity')

bar3 <- ggplot(data=diamonds_mp_by_cut, aes(x=cut, y=mean_price)) + 
  geom_bar(stat='identity')

grid.arrange(bar1, bar2, bar3, ncol=1, nrow=3)

