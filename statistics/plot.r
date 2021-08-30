library(ggplot2)
library(reshape)
library(plyr)

set.seed(5)

coinfiles = c("ETH.csv", "LINK.csv", "LTC.csv", "XMR.csv")

sampleSize = 50
numSamples = 400

meansmatrix = matrix(, nrow=numSamples, ncol=4)
stdnormmatrix = matrix(, nrow=numSamples, ncol=4)

for(index in c(1:4)) {
	coinfile = coinfiles[index]
	df = read.csv(coinfile, header=FALSE)

	names(df) = c("x")

	x = df$x


	samples = matrix(, nrow = numSamples, ncol = sampleSize)

	for(i in seq_len(numSamples)) {
		sample_row = sample(x, size=sampleSize, replace=TRUE)
		samples[i,] = sample_row
	}

	means = apply(samples, 1, mean)
	std = apply(samples, 1, sd)
	stdnorm = (std - mean(std)) / sd(std)

	meansmatrix[,index] = means
	stdnormmatrix[,index] = stdnorm
}

meansmatrix = data.frame(meansmatrix)
names(meansmatrix) = coinfiles
mdata = melt(meansmatrix)

mu = ddply(mdata, "variable", summarise, grp.mean=mean(value))

mplot = ggplot(mdata, aes(x=value, fill=variable)) +
	geom_density(alpha=0.7) + 
	geom_vline(data=mu, aes(xintercept=grp.mean),
		alpha=0.7, linetype="dashed") +
	xlab("mean of %gain") +
	ggtitle("Distribution of the mean profit across coins") +
	theme_bw()

stdnormmatrix = data.frame(stdnormmatrix)
names(stdnormmatrix) = coinfiles
sdata = melt(stdnormmatrix)

splot = ggplot(sdata, aes(x=value, fill=variable)) +
	geom_density(alpha=0.6) +
	xlab("standardized sd of the distribution of %gain") +
	theme_bw()

print(mplot)
print(splot)