# setup
setwd("~/Columbia MSBA/Spring 2019/E4524 - Analytics in Practice/Data/Csv")
df = read.csv("a_test.csv")
df$X = NULL
df = na.omit(df)
set.seed(1)
library(leaps)
library(glmnet)
library("tree")
library("ISLR")
library("pls")
library(randomForest)
library(tree)
library(MASS)
library(ISLR)
library(rpart)
df$Treatment.. = log1p(df$Treatment..)
colnames(df)
##################### Linear Regression - LASSO ####################################################
train = sample(1:nrow(df),0.75*nrow(df)) 
test = -train
df_train=df[train,]
df_test=df[test,]

p = 8
k=10

x=model.matrix(Treatment.Success...~.,df )
y=df$Treatment.Success...
grid= c(0,0.001,0.01,0.1,1,10,100,1000)
cv.out = cv.glmnet(x[train,], y[train], alpha=1, lambda=grid, nfolds=k) 
bestlam = cv.out$lambda.min
lasso.mod = glmnet(x[train,], y[train], alpha=1, lambda=bestlam)
coef(lasso.mod)
pred_lasso = predict(lasso.mod, x[test,])
actual_lasso = y[test]


RMSE = function(m, o){
  sqrt(mean((m - o)^2))
}

RMSE(pred_lasso,actual_lasso) #2.00 for Treatment$   |   #0.199 for Treatment%


##################### Partial Least Squares (PLS) Using 10-fold-CV #################################
train = sample(1:nrow(df),0.75*nrow(df)) 
test = -train
training=df[train,]
validation=df[test,]

y=df$Treatment.Success...
y.validation = y[test]

pls.fit = plsr(Treatment.Success...~., data=training, scale=T, validation="CV", segments=10)
validationplot(pls.fit,val.type="MSEP")
pls.pred = predict(pls.fit,validation,ncomp=3)
RMSE = function(m, o){
  sqrt(mean((m - o)^2))
}
RMSE(pls.pred,y.validation) #2.01 for Treatment$   | 0.192 for Treatment%  


pls.fit = plsr(Treatment..~., data=df_train, scale=T, validation="CV", segments=10)
validationplot(pls.fit,val.type="MSEP")
pls.pred = predict(pls.fit,df_test,ncomp=3)

##################### Decision Tree ###############################################################
tree.pldg=tree(Treatment.Success...~.,training)
cv.pldg=cv.tree(tree.pldg)
plot(cv.pldg$size,cv.pldg$dev,type='b')
prune.pldg=prune.tree(tree.pldg,best=cv.pldg$size[which.min(cv.pldg$dev)])

# Prediction
yhat=predict(prune.pldg,newdata=validation)
RMSE(yhat,y.validation) #1.38 for Treatment$   |   0.062 for Treatment%

##################### Random Forest ###############################################################
rf.pldg=randomForest(Treatment.Success...~.,data=training, mtry=6, ntree=10, importance=TRUE)

# Prediction
yhat.rf = predict(rf.pldg,newdata=validation)
RMSE(yhat.rf,y.validation) #1.17 fro Treatment$   |   0.03 for Treatment%

# Most important predictor
importance(rf.pldg)
varImpPlot(rf.pldg)





