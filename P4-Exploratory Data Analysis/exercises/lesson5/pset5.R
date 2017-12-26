# Create a histogram of diamond prices.
# Facet the histogram by diamond color
# and use cut to color the histogram bars.

# The plot should look something like this.
# http://i.imgur.com/b5xyrOu.jpg

# Note: In the link, a color palette of type
# 'qual' was used to color the histogram using
# scale_fill_brewer(type = 'qual')

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ===========================================

??diamonds
library(ggplot2)
rm(list=ls())
df <- diamonds #diamonds is part of ggplot2 package
names(df)
ggplot(df, aes(x=price)) + 
  geom_histogram(aes(color=cut)) +
  scale_fill_brewer(type='qual') +
  facet_wrap(~color)

# Create a scatterplot of diamond price vs.
# table and color the points by the cut of
# the diamond.

# The plot should look something like this.
# http://i.imgur.com/rQF9jQr.jpg

# Note: In the link, a color palette of type
# 'qual' was used to color the scatterplot using
# scale_color_brewer(type = 'qual')

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ===========================================

?diamonds
ggplot(subset(df, df$cut=='Premium'), aes(x=table, y=price)) +
  geom_point(aes(color=cut), alpha=.3) + 
  scale_fill_brewer(type='qual') +
  scale_x_continuous(breaks=seq(50,80,1)) + 
  coord_cartesian(xlim=c(50,80))


# Create a scatterplot of diamond price vs.
# volume (x * y * z) and color the points by
# the clarity of diamonds. Use scale on the y-axis
# to take the log10 of price. You should also
# omit the top 1% of diamond volumes from the plot.

# Note: Volume is a very rough approximation of
# a diamond's actual volume.

# The plot should look something like this.
# http://i.imgur.com/excUpea.jpg

# Note: In the link, a color palette of type
# 'div' was used to color the scatterplot using
# scale_color_brewer(type = 'div')

# This assignment is not graded and
# will be marked as correct when you submit.

# ===========================================

df <- transform(df, volume = x*y*z)
ggplot(subset(df, volume<), aes(y=price, x=volume)) + 
  geom_points(aes(color=clarity)) + 
  scale_y_log10()

# Create a scatterplot of diamond price vs.
# volume (x * y * z) and color the points by
# the clarity of diamonds. Use scale on the y-axis
# to take the log10 of price. You should also
# omit the top 1% of diamond volumes from the plot.

# Note: Volume is a very rough approximation of
# a diamond's actual volume.

# The plot should look something like this.
# http://i.imgur.com/excUpea.jpg

# Note: In the link, a color palette of type
# 'div' was used to color the scatterplot using
# scale_color_brewer(type = 'div')

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ===========================================
?diamonds
df <- diamonds
df <- transform(df, volume=x*y*z)
ggplot(data=df, aes(y=price, x=volume)) +
  geom_point(aes(color=clarity)) + 
  scale_y_log10() + 
  coord_cartesian(xlim=c(min(df$volume), quantile(df$volume,.99))) +
  scale_color_brewer(type='div')

# Many interesting variables are derived from two or more others.
# For example, we might wonder how much of a person's network on
# a service like Facebook the user actively initiated. Two users
# with the same degree (or number of friends) might be very
# different if one initiated most of those connections on the
# service, while the other initiated very few. So it could be
# useful to consider this proportion of existing friendships that
# the user initiated. This might be a good predictor of how active
# a user is compared with their peers, or other traits, such as
# personality (i.e., is this person an extrovert?).

# Your task is to create a new variable called 'prop_initiated'
# in the Pseudo-Facebook data set. The variable should contain
# the proportion of friendships that the user initiated.

# This programming assignment WILL BE automatically graded.

# DO NOT DELETE THIS NEXT LINE OF CODE
# ========================================================================
pf <- read.delim('pseudo_facebook.tsv')
pf <- transform(pf, prop_initiated=friendships_initiated/friend_count)
# ENTER YOUR CODE BELOW THIS LINE
# ========================================================================


# Create a line graph of the median proportion of
# friendships initiated ('prop_initiated') vs.
# tenure and color the line segment by
# year_joined.bucket.

# Recall, we created year_joined.bucket in Lesson 5
# by first creating year_joined from the variable tenure.
# Then, we used the cut function on year_joined to create
# four bins or cohorts of users.

# (2004, 2009]
# (2009, 2011]
# (2011, 2012]
# (2012, 2014]

# The plot should look something like this.
# http://i.imgur.com/vNjPtDh.jpg
# OR this
# http://i.imgur.com/IBN1ufQ.jpg

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ===========================================================
names(pf)
library(ggplot2)
#create year joined bucket
pf$year_joined <- floor(2014 - (pf$tenure/365))
pf$year_joined.bucket<- cut(pf$year_joined, breaks=c(2004, 2009, 2011, 2012, 2014))
#plot the graph
ggplot(pf, aes(x=tenure, y=prop_initiated)) + 
  geom_line(aes(color=year_joined.bucket), stat="summary", fun.y="median")
  
# i want the median of proportion of friendships initated
# how to get the median? got apply some function to the y function
# but how? I really forgot how to do it


# Smooth the last plot you created of
# of prop_initiated vs tenure colored by
# year_joined.bucket. You can bin together ranges
# of tenure or add a smoother to the plot.

# There won't be a solution image for this exercise.
# You will answer some questions about your plot in
# the next two exercises.

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ====================================================
ggplot(pf, aes(x=tenure, y=prop_initiated)) + 
  geom_line(aes(color=year_joined.bucket), stat="summary", fun.y="median") +
  geom_smooth()

table(pf$year_joined.bucket)
#sounds good enough

library(tidyr)
library(dplyr)

custom.summary <- pf %>%
  filter(!is.na(prop_initiated)) %>%
  group_by(year_joined.bucket) %>% 
  summarize(mean_prop_initiated = mean(prop_initiated),
            n = n())

custom.summary

# Create a scatter plot of the price/carat ratio
# of diamonds. The variable x should be
# assigned to cut. The points should be colored
# by diamond color, and the plot should be
# faceted by clarity.

# The plot should look something like this.
# http://i.imgur.com/YzbWkHT.jpg.

# Note: In the link, a color palette of type
# 'div' was used to color the histogram using
# scale_color_brewer(type = 'div')

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ===========================================
df <- diamonds
#preço do quilate no eixo y
ggplot(df, aes(x=cut, y=price/carat)) + 
  geom_point(aes(color=color)) + 
  facet_wrap(~clarity)

#olhando o preço individualmente não há uma relação clara com cor, clareza ou corte
# mas ao analisar o preço por quilate, a relação fica óbvia
# só olhar o preço sozinho não é possível analisar 
# o que implica que provavelmente há uma correlação negativa entre as qualidades do diamante
# e o peso em quilates. quanto mais bruto o diamante, maior o número de quilates
# o que se confirma olhando o gráfico individual
?diamonds
