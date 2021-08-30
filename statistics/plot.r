library(ggplot2)

coinfiles = c("ETH.csv", "LINK.csv", "LTC.csv", "XMR.csv")

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
		geom_density() +
		ggtitle(coinfile)

	varplot = ggplot(, aes(x=variance)) +
		geom_density() +
		ggtitle(coinfile)

	print(meanplot)
	print(varplot)
}