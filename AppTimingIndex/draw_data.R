data = read.csv('loadtime2.csv', header=TRUE)


png('sitdt.png', width = 720, height = 720)
temp_par = par()
par(mar = c(6, 5, 5, 4)+0.1)
par(xpd = TRUE)

all_data = as.matrix(data[c('si', 'sidata')])
plot(all_data,
     xlab='Speed Index (s)',
     ylab='SI - Data (s)',
     ylim=c(-5, 5),
     cex.main=2,
     cex.axis=1.5,
     cex.lab=2)
lines(c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0), col='black')
lines(seq(0, 9*0.1, 1*0.1), col='green')
lines(seq(0, 9*0.25, 1*0.25), col='brown')
lines(seq(0, 9*0.5, 1*0.5), col='red')
lines(seq(0, -9*0.1, -1*0.1), col='green')
lines(seq(0, -9*0.25, -1*0.25), col='brown')
lines(seq(0, -9*0.5, -1*0.5), col='red')

legend(x='topleft', inset=0.015,
      legend=c('10%', '25%', '50%'),
      col=c('green', 'brown', 'red'),
      lty=1,
      cex=1.25)





par = temp_par
dev.off()
