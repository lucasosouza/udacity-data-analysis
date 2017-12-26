library(reshape2)

#run from unemployment-csv-folder
full.df <- NULL
for (file in list.files()) {
  df <- read.csv(file, header=TRUE, sep= ";")
  print(file)
  
  #fix column headers
  names(df) <- gsub(names(df), pattern="X", replacement="")
  names(df)[1] <- "Country"
  
  #melt
  df <- melt(df, id="Country", variable.name="Year", value.name="Unemployment Rate")
  
  #get age and gender
  gender <- substr(file, 11, 11)
  age <- substr(file, 13, 13)
  if (age == 'a') {
    full.age <- 'above 55'
  } else if (age == 'b') {
    full.age <- 'All (above 15)'
  } else if (age == '1') {
    full.age <- '15-24'
  } else if (age == '2') {
    full.age <- '25-54'
  }
  df['Gender'] <- gender
  df['Age'] <- full.age
  
  #merge to existing. create if frist
  if (is.null(full.df)) full.df <- df
  full.df <- rbind(full.df, df)
  tail(full.df)
}

#remove lines with NULL value in country
full.df <- subset(full.df, Country != '')

#fix commas
#full.df['Unemployment Rate'] <- gsub(full.df['Unemployment Rate'], pattern=",", replacement=".")

#save file
#write.csv(full.df, file=('consolidated_unemployment.csv'), sep=';', row.names=FALSE)

############ fix and add gdp

#gdp should be melted in a similar format and merged with above results, since dimple will only take one dataset

#load file from 
gdp.df <- read.csv("../gdp-xls-csv/GDPpercapitaconstant2000US.csv", header=TRUE, sep=";")

#fix column headers
names(gdp.df) <- gsub(names(gdp.df), pattern="X", replacement="")
names(gdp.df)[1] <- "Country"

#melt
gdp.df <- melt(gdp.df, id="Country", variable.name="Year", value.name="Per Capita GDP")

#merge with full df
total.df <- merge(full.df, gdp.df, by=c("Country", "Year"))

############ fix and add population

#load file from 
population.df <- read.csv("../population-xls-csv/indicator gapminder population.xlsx - Data.csv", header=TRUE, sep=",")

#fix column headers
names(population.df) <- gsub(names(population.df), pattern="X", replacement="")
names(population.df)[1] <- "Country"

#melt
population.df <- melt(population.df, id="Country", variable.name="Year", value.name="Population")

#merge with full df
total.df <- merge(total.df, population.df, by=c("Country", "Year"))

str(total.df)
  
#save file
write.csv(total.df, file=('../consolidated_unemployment_gdp.csv'), sep=';', row.names=FALSE)


