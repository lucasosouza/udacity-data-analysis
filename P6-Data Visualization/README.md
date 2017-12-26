### Summary

The visualization conveys the story of the relationship between unemployment and economic performance. The aim is to show the audience there is no exact correlation between both, so they can think of unemployment from a different perspective from what is taught in the schools and outdated economic courses.

The data is from Gapminder. I have downloaded both aggregated data, and separated by gender and age, to allow the user some interaction. Only 27 countries had data available on inequality.

### Design

It is a martini-glass shaped visualization, with an initial visualization showing the average of all countries, an overall trend, and them the next visualization in similar fashion, but allowing the user to tweak some parameters.

Ideally the user should be able to select his own country, but there is limited data available. I've also avoided using a map as a selector since there are only a few countries available.

### Feedback

#### 1.List feedback given by colleagues:

##### Comment A
*It's quite easy to understand as of now. My suggestion is that you add another graph where you can compare gdp/unemployment of countries with each other, where you can select/deselect gdp and unemployment. Maybe it can show us how changes in one country affects other countries.﻿*

takeaways: 
- select/deselect gdp unemployment: choose or not to show the line
- compare countries

##### Comment B

 
*Hi Lucas.*

*1. I actually think the simplicity of the visualization is an asset. It looks elegant and conveys the comparison between gdp per capita and unemployment through time in an effective way.
I think dots to mark years should be put on both lines. A map could be a first user option to select the country, and then the user can select the other two demographic variables. However I think a better improvement could be to replace the initial statement with an initial visualization that conveys the main relationship you are trying to show; for instance, an average for all countries in unemployment and gdp, in order to show, in avg., this relationship. As I understand it, the story in the data should be told from the visualization and not from an initial statement.*

*2. No questions about the data.*

*3. The relationship bet. gdp per capita and unemployment varies quite a bit bet. countries. As stated above, it would be nice to have an introductory visualization for all countries before allowing user interaction. (Kind of martini glass visualization story)*

*4. The initial statement is maybe a bit too long and ambitious given the visualizations that the data gives. The relationship bet. unemployment and policies is not something that I can link directly with gdp per capita. My takeaway is that unemployment and gdp don't seem to have a clear relationship, and I think that is a valid takeaway on its own.*

*5. I think the visualization and interactivity are really good. Just replace the initial statement with an initial visualization, or make it shorter and more relevant to the actual visualization, and add dots to both lines.﻿*

takeaway:
- simplicity is good
- dots to mark the years on both lines. 
- map as the first option to select the country
- replace initial statement with an initial visualization that conveys the relationship trying to show. the story must be told from the visualization. can use averages
- make the statement shorter and relevant to the actual visualization

#### 2. Evaluate what you want to incorporate fom these comments into your project. Add the changes you want to make and come up with a final list

- replace initial statement with an initial visualization that conveys the relationship trying to show. the story must be told from the visualization. can use averages
- make the statement shorter and relevant to the actual visualization
- dots to mark the years on both lines. 

### Resources

I've used Dimple.js for visualization, a little bit of D3.js in selections and dimple parametes, Angular.js to organize the code and do the controller-view communication and Bootstrap for formatting. I've referred to Dimple.js API for instructions.