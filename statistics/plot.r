library(ggplot2)

coinfiles = c("ETH.csv", "LINK.csv", "LTC.csv", "XMR.csv")

# results = matrix(means)

for(coinfile in coinfiles) {
	df = read.csv(coinfile, header=FALSE)

	names(df) = c("x")

	x = df$x

	sampleSize = 20
	numSamples = 400

	samples = matrix(, nrow = numSamples, ncol = sampleSize)

	for(i in seq_len(numSamples)) {
		sample_row = sample(x, size=sampleSize, replace=TRUE)
		samples[i,] = sample_row
	}

	means = apply(samples, 1, mean)
	variance = apply(samples, 1, var)

	meanplot = ggplot(, aes(x=means)) +
		geom_density(fill="gray", alpha=0.8) +
		geom_vline(aes(xintercept=mean(means)), color="black",
             linetype="dashed") +
		ggtitle(coinfile) +
		xlab("mean %gain") +
		theme_bw()

	varplot = ggplot(, aes(x=sqrt(variance))) +
		geom_density(fill="gray", alpha=0.8) +
		geom_vline(aes(xintercept=mean(sqrt(variance))), color="black",
             linetype="dashed") +
		ggtitle(coinfile) +
		xlab("standard deviation") +
		theme_bw()

	print(meanplot)
	print(varplot)
}