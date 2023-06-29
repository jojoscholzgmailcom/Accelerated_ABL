library(ggplot2)
library(plyr)
library(dplyr)
library(tidyverse)

bp.data <- read.csv("C:/Users/jojos/OneDrive/Dokumente/Universität/Year3/Bachelor Project/Code/end-results.csv")
bp.data <- bp.data %>% mutate(otherDependencies = (totalDependencies - decisionDependencies))
bp.data$accuracy<-100*(bp.data$accuracy)
bp.model <- lm(bp.data$accuracy ~ bp.data$decisionDependencies * bp.data$totalNodes * bp.data$otherDependencies)
summary(bp.model)
bp.model.res <- resid(bp.model)
plot(fitted(bp.model), bp.model.res)
abline(0, 0)

qqnorm(bp.model.res)
qqline(bp.model.res)

plot(density(bp.model.res))

bp.data.step <- read.csv("C:/Users/jojos/OneDrive/Dokumente/Universität/Year3/Bachelor Project/Code/Backup Data/attempt-results-first-real.csv")
bp.data.step$accuracy<-(200*(bp.data.step$accuracy))/(bp.data.step$attempt + 1)
bp.data.step$accuracy<-100*(bp.data.step$accuracy)
bp.data.step <- bp.data.step %>% group_by(type, combination, totalNodes, totalDependencies, decisionDependencies, attempt) %>% summarise_at(vars(accuracy), list(mean))
bp.data.step <- bp.data.step[bp.data.step$type %in% c(0,1), ]

bp.data.step.nn <- read.csv("C:/Users/jojos/OneDrive/Dokumente/Universität/Year3/Bachelor Project/Code/Backup Data/attempt-results-nn.csv")
bp.data.step.nn$accuracy<-100*(bp.data.step.nn$accuracy)
bp.data.step.nn <- bp.data.step.nn %>% group_by(type, combination, totalNodes, totalDependencies, decisionDependencies, attempt) %>% summarise_at(vars(accuracy), list(mean))

bp.data.step.dt <- read.csv("C:/Users/jojos/OneDrive/Dokumente/Universität/Year3/Bachelor Project/Code/Backup Data/attempt-results-dt.csv")
bp.data.step.dt$accuracy<-100*(bp.data.step.dt$accuracy)
bp.data.step.dt <- bp.data.step.dt %>% group_by(type, combination, totalNodes, totalDependencies, decisionDependencies, attempt) %>% summarise_at(vars(accuracy), list(mean))


display.data <- function(type, decisionDeps) {
  tmp.data <- bp.data.step[bp.data.step$type == type, ]
  tmp.data <- tmp.data[tmp.data$totalNodes %in% decisionDeps, ]
  print(ggplot(data = tmp.data, aes(x = attempt, y = accuracy, color = factor(totalNodes))) + geom_line() + ylim(0, 100) + labs(color='Number of Nodes', x = "samples") )
}

display.data.comp <- function(type, decisionDep) {
  tmp.data <- bp.data.step[bp.data.step$type == type, ]
  tmp.data <- tmp.data[tmp.data$totalNodes == decisionDep, ]
  tmp.data <- tmp.data %>% add_column(mltype = "AABL")
  
  tmp.data.nn <- bp.data.step.nn[bp.data.step.nn$type == type, ]
  tmp.data.nn <- tmp.data.nn[tmp.data.nn$totalNodes == decisionDep, ]
  tmp.data.nn <- tmp.data.nn %>% add_column(mltype = "NN")
  
  tmp.data.dt <- bp.data.step.dt[bp.data.step.dt$type == type, ]
  tmp.data.dt <- tmp.data.dt[tmp.data.dt$totalNodes == decisionDep, ]
  tmp.data.dt <- tmp.data.dt %>% add_column(mltype = "DT")
  
  tmp.data.all = rbind(tmp.data,tmp.data.nn, tmp.data.dt)
  
  print(ggplot(data = tmp.data.all, aes(x = attempt, y = accuracy, color = factor(mltype))) + geom_line() + ylim(0, 100) + labs(color='ML algorithm type', x = "samples") )
}

data_summary <- function(data, varname, groupnames){
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm=TRUE),
      sd = sd(x[[col]], na.rm=TRUE))
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  print(data_sum)
  #data_sum <- rename(data_sum, c("mean" = varname))
  return(data_sum)
}

bp.data <- read.csv("C:/Users/jojos/OneDrive/Dokumente/Universität/Year3/Bachelor Project/Code/Backup Data/end-results-time-max-6min.csv")
bp.data <- bp.data %>% mutate(otherDependencies = (totalDependencies - decisionDependencies))
bp.data$accuracy<-100*(bp.data$accuracy)
bp.data <- bp.data %>% add_column(mltype = "AABL")
bp.data <- data_summary(bp.data, varname="runtime", groupnames = c("type", "mltype", "decisionDependencies"))

bp.data.nn <- read.csv("C:/Users/jojos/OneDrive/Dokumente/Universität/Year3/Bachelor Project/Code/Backup Data/end-results-nn-time-max-6min.csv")
bp.data.nn <- bp.data.nn %>% mutate(otherDependencies = (totalDependencies - decisionDependencies))
bp.data.nn$accuracy<-100*(bp.data.nn$accuracy)
bp.data.nn <- bp.data.nn %>% add_column(mltype = "NN")
bp.data.nn <- data_summary(bp.data.nn, varname="runtime", groupnames = c("type", "mltype", "decisionDependencies"))

bp.data.dt <- read.csv("C:/Users/jojos/OneDrive/Dokumente/Universität/Year3/Bachelor Project/Code/Backup Data/end-results-dt-time-max-6min.csv")
bp.data.dt <- bp.data.dt %>% mutate(otherDependencies = (totalDependencies - decisionDependencies))
bp.data.dt$accuracy<-100*(bp.data.dt$accuracy)
bp.data.dt <- bp.data.dt %>% add_column(mltype = "DT")
bp.data.dt <- data_summary(bp.data.dt, varname="runtime", groupnames = c("type", "mltype", "decisionDependencies"))

bp.data.all = rbind(bp.data,bp.data.nn, bp.data.dt)

#bp.data <- bp.data %>% group_by(type, combination, totalNodes, totalDependencies, decisionDependencies) %>% summarise_at(vars(runtime), list(mean))
bp.data.filter <- bp.data.all[bp.data.all$type == 1, ]
bp.data.filter <- bp.data.filter[bp.data.filter$decisionDependencies <= 17, ]
ggplot(data = bp.data.filter, aes(x = decisionDependencies, y = mean, color = mltype)) + geom_line() + geom_point() + geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), width=.2) + labs(x = 'Dependencies', y = 'Runtime in seconds', color = 'ML Type') 

display.data.comp(1, 3)
display.data.comp(1, 4)
display.data.comp(1, 6)
display.data.comp(1, 8)
display.data.comp(1, 10)
display.data.comp(1, 12)
display.data.comp(1, 14)
display.data.comp(1, 16)
display.data.comp(1, 18)
display.data.comp(1, 20)
display.data.comp(1, 22)

display.data(1, c(3,4,6,8,10,12,14,16,18,20,22))
display.data(0, c(3,4,6,8,10,12,14,16,18,20,22))
