png('waterfall.png', width = 1280, height = 720)
temp_par = par()

par(mar = c(6, 5, 5, 4)+0.1)

par(xpd = TRUE)

data = read.csv('ebay_timing.csv', header=TRUE)

barplot(t(as.matrix(data[2:9])), 
        horiz=TRUE,
        names.arg=as.matrix(data[1]),
        col=c('white', 'gray', 'white', 'darkgoldenrod1', 'goldenrod4', 'darkslategray2', 'white', 'darkslategray4'),
        border=NA,
        yaxt='n',
        xlim=c(0, 35),
        xlab='Load time(s)',
        cex.main=1.5)

labs = as.matrix(data[1])
text(x=0, 
     y=c(0.7, 1.9, 3.1, 4.3, 5.5,
         6.7, 7.9, 9.1, 10.3, 11.5, 12.7),
     labs)

legend(x="topright", inset = 0.015, 
       legend=c('', 'DNS', '', 'Connect', 'SecureConnect', 
                'Request', '', 'Response'), 
       fill =c('white', 'gray', 'white', 'darkgoldenrod1', 'goldenrod4', 'darkslategray2', 'white', 'darkslategray4'))

par = temp_par
dev.off()
