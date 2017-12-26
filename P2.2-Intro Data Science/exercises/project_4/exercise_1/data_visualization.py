from pandas import *
from ggplot import *
def plot_weather_data(df):
    ggplot(df, aes(x='ENTRIESn_hourly',colour='rain')) + \
        geom_histogram() + \
        scale_colour_manual(values=['red','blue'])

plot_weather_data = read_csv('turnstile_weather_v2.csv')

if __name__ == "__main__":
    image = "plot.png"
    input_filename=" "
    with open(image, "wb") as f:
        turnstile_weather = read_csv(input_filename)
        turnstile_weather['datetime'] = turnstile_weather['DATEn'] + ' ' + turnstile_weather['TIMEn']
        gg =  plot_weather_data(turnstile_weather)
        ggsave(f, gg)

        #geom_line() + \
