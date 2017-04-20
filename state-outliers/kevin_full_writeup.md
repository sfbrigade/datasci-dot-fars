## Analysis 1: Interrupted Time Series

The dependent variables in my analysis are total deaths. Totals deaths are stratified by age and type of death. In total, five regressions were estimated. The results are shown in two tables for readability sake. From the regression results, we can conclude that 2015 was not an abnormal year for deaths, when compared to the average trend of deaths in the prior years.

My empirical strategy is an interrupted time series design, also known as a segmented regression. The regression estimate is plain vanilla segmented regression with the addition of state level fixed effect. 

The canonical segmented regression with a fixed effect takes the following form. 

$$Y_{s, t} = \beta_0 + \beta_1 Year_{s} + \beta_{2} Post_{s, t} + \beta_3 Year_{s} * Post_{s,t}+ \alpha_{s} + \epsilon_{s,t}$$

The variable $$Y$$ is the dependent variable of interest. $$Year$$ represents the time elapsed since the starting year. $$Post$$ is an indicator variable that is 0 for time period before and 1 for years 2015 and after. The intercept $$\beta_0$$ represents the baseline level at time 0. $$\beta_1$$ is the pre-2015 trend of the dependent variable. $$\beta_2$$ is the change following 2015 and $$\beta_3$$ is the change in the slope following 2015. Lastly, $$\alpha$$ is the state-level fixed effect. The subscripts $$s$$ and $$t$$ represent state and year respectively.

Our data does not contain subsequent years for 2015, making the interaction term unnecessary. In my analysis, I instead estimate the following regression.

$$y_{s, t} = \beta_0 + \beta_1 Year_{s} + \beta_2 Post_{s, t} + \alpha_{s} + \epsilon_{s,t}$$

The variable of interest here is the coefficient on the $$Post$$ variable. The coefficient tells us if 2015 is deviant in terms of the dependent variable. If 2015 is deviant, then the sign will be positive and significant. In all the regressions estimated, none of the coefficients are significant. This suggests that 2015 is not abnormal. 

The state-level fixed effect embeds unobservable heterogeneity that is assumed to fixed over time. For example, the regression does not control for demographics even though demographics may be an omitted variable. Demographics tend to evolve slowly so the assumption that it is fixed is reasonable. With the state-level fixed effect all unobserved heterogeneity in demographics at the state level is embedded in $$\alpha$$.