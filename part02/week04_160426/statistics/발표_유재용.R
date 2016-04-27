install.packages("robust")
library(robust)
data(breslow.dat, package="robust")
summary(breslow.dat[c(6,7,8,10)])
?breslow.dat

attach(breslow.dat)

hist(sumY, breaks=20, freq=FALSE, col="salmon", main="Distribution of seizures")

lines(density(sumY), col="blue", lwd=2)

plot(sumY~Trt, main="Group Comparison")

mean(sumY)
var(sumY)

fit1=glm(sumY~Base+Age+Trt, family=poisson, data=breslow.dat)

summary(fit1)

install.packages("moonBook")
require(moonBook)

extractOR(fit1, digits=3)
ORplot(fit1, type=3, show.OR=FALSE, show.CI=TRUE, main="Result of Poisson Regression")

#나이가 한살 많아지면 다른 변수가 일정할 때 seizure의 횟수가 1.023배 증가하는 것을 알 수 있다. 
#또한 위약 대신 progabide를 투여하면 seiure횟수가 0.858배, 즉 14.2% 감소하는 것을 알 수 있다.


install.packages("qcc")
require(qcc)

??qcc
qcc.overdispersion.test(breslow.dat$sumY, type="poisson")

#family=quasipoisson을 사용하여야 한다.

fit2=glm(sumY~Base+Age+Trt, family=quasipoisson, data=breslow.dat)

summary(fit2)


extractOR(fit2, digits=3)
ORplot(fit2, type=3, show.CI=TRUE, main="Result of Quasipoisson Regression")


#or negative binomial
fit3=glm.nb(sumY~Base+Age+Trt, data=breslow.dat)
summary(fit3)


extractOR(fit3, digits=3)
ORplot(fit3, type=3, show.CI=TRUE, main="Result of negative binomial Regression")





#non linear curve fit

t <- 0:10
y <- rnorm(11, mean=5*exp(-t/5), sd=.2)
plot(y ~ t)

nlsout <- nls(y ~ A*exp(-alpha*t), start=c(A=2, alpha=0.05))
summary(nlsout)


#Finding starting values
library(ISwR)
attach(subset(juul2, age<20 & age>5 & sex==1))
plot(height ~ age)

#there is some levelling off at the right end and
#of course it is basic human biology that we stop growing at some point in the later teens.



plot(log(5.3-log(height))~age)
lm(log(5.3-log(height))~age)


fit <- nls(height~alpha*exp(-beta*exp(-gamma*age)),
            start=c(alpha=exp(5.3),beta=exp(0.42),gamma=0.15))
summary(fit)


plot(age, height)
newage <- seq(5,20,length=500)
lines(newage, predict(fit,newdata=data.frame(age=newage)),lwd=2)


#there is a tendency for the dispersion to increase
#with increasing fitted values, so we attempt a log-scale fit. This can be
#done expediently by transforming both sides of the model formula.


fit <- nls(log(height)~log(alpha*exp(-beta*exp(-gamma*age))),
            start=c(alpha=exp(5.3),beta=exp(.12),gamma=.12))
summary(fit)

plot(age, log(height))
lines(newage, predict(fit,newdata=data.frame(age=newage)),lwd=2)







#self-starting model
summary(nls(height~SSgompertz(age, Asym, b2, b3)))

nls(log(height) ~ log(SSgompertz(age, Asym, b2, b3)))
cf <- coef(nls(height ~ SSgompertz(age, Asym, b2, b3)))


summary(nls(log(height) ~
               log(as.vector(SSgompertz(age,Asym, b2, b3))),
             start=as.list(cf)))



#Profiling

par(mfrow=c(3,1))
plot(profile(fit))
confint(fit)

?profile
